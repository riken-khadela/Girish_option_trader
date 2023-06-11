from core.models import Strategymain, Strategy, StrategyOne, paper_orders
from datetime import datetime
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)
from smartapi.smartWebSocketV2 import SmartWebSocketV2
import pyotp, requests
import json, time
from datetime import datetime
import pandas as pd
import uuid




class Fetch_liveData:
    def __init__(self) -> None:
        self.api_key ="zb1uzu8p"
        self.client_code = "P342447"
        self.password = "2188"
        self.totp = pyotp.TOTP("KVZPGMGGHAILAMGFPRCB2YI5LA").now()
        self.obj=SmartConnect(api_key=self.api_key)
        data = self.obj.generateSession(self.client_code,self.password,self.totp)
        self.refreshToken= data['data']['refreshToken']
        self.jwtToken= data['data']['jwtToken']
        self.index_data = [{'exch_seg':'NSE','symbol':'BANKNIFTY','token':'26009','check_name':'BANKNIFTY'},{'exch_seg':'CDS','symbol':'NIFTY50','token':'2','check_name':'NIFTY'},{'exch_seg':'NSE','symbol':'Nifty Fin Service','token':'99926037','check_name':'FINNIFTY'}]
       
    
    def get_Open_Api_Data(self):
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)
        data = json.loads(response.content)
        table = pd.DataFrame(data)
        return table
      
    def get_ltp_data(self,exchange,symbol,token):
        data = self.obj.ltpData(str(exchange),str(symbol),str(token))
        return data['data']['ltp']

    def log_out(self):
        try:
            logout=self.obj.terminateSession('P342447')
            print("Logout Successfull")
        except Exception as e:
            print("Logout failed: {}".format(e.message))
    
    def convert_date(self,date_str):
        return datetime.strptime(date_str, '%d%b%Y')

    def get_current_exp(self,data,index_type=None):
        df = data
        if index_type == 'future':
            df = df[(df['name'] == 'NIFTY') & (df['exch_seg'] == 'NFO') & (df['instrumenttype'] == 'FUTIDX')]
            dates = list(df['expiry'].unique())
        else:
            df = df[(df['name'] == 'NIFTY') & (df['exch_seg'] == 'NFO') & (df['instrumenttype'] == 'OPTIDX')]
            dates = list(df['expiry'].unique())
        sorted_dates = sorted(dates, key=self.convert_date)
        current_exp = sorted_dates[0]
        next_exp = sorted_dates[1]
        return current_exp, next_exp


    def option_price_and_type(self,options):
        # # Extract the option type
        option_type = options[-2:]
        # Remove the last two words
        words = options[:-2]
        # Extract the last five words
        strike_price = "".join(words[-5:])
        return option_type, strike_price
    

    def get_strike_price_by_optionType(self, expiry, data, nameOfindex, strike_price_ltp, strike_price_ltp_two):
        df = data
        if nameOfindex == 'BANKNIFTY':
            index = self.index_data[0]
            index_exchange = index['exch_seg']
            index_symbol = index['symbol']
            index_token = index['token']
        elif nameOfindex == 'NIFTY':
            index = self.index_data[1]
            index_exchange = index['exch_seg']
            index_symbol = index['symbol']
            index_token = index['token']
        else:
            index = self.index_data[2]
            index_exchange = index['exch_seg']
            index_symbol = index['symbol']
            index_token = index['token']


        filtered_df = df[(df['name'] == str(nameOfindex)) & (df['exch_seg'] == 'NFO') & (df['expiry'] == str(expiry)) & (df['instrumenttype'] == "OPTIDX")]
        ce_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'CE')
        ce_df = filtered_df[ce_mask]
        ce_df = filtered_df[ce_mask].copy()
        ce_df = ce_df.assign(**{
            'Option_type': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        # 'exch_seg':'NSE','symbol':'BANKNIFTY','token':'26009'
        
        index_ltp_price = self.get_ltp_data(exchange=index_exchange,symbol=index_symbol,token=index_token)
        ce_df = ce_df[ce_df['Strike_price'].astype(float) >= float(index_ltp_price)]
        ce_token = ce_df['token'].astype(str).tolist()
        
        pe_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'PE')
        pe_df = filtered_df[pe_mask]
        pe_df = filtered_df[pe_mask].copy()
        pe_df = pe_df.assign(**{
            'Option_type': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        pe_df = pe_df[pe_df['Strike_price'].astype(float) <= float(index_ltp_price)]
        pe_token = pe_df['token'].astype(str).tolist()
        sorted_ce_options = ce_df.sort_values(by='Strike_price').to_dict(orient='records')
        sorted_pe_options = pe_df.sort_values(by='Strike_price').to_dict(orient='records')
        sorted_ce_options_new_df = [{'exch_seg':d['exch_seg'],'token':d['token'], 'symbol':d['symbol'], 'Option_type':d['Option_type'], 'Strike_price':d['Strike_price']}for d in sorted_ce_options]
        sorted_pe_options_new_df = [{'exch_seg':d['exch_seg'],'token':d['token'], 'symbol':d['symbol'], 'Option_type':d['Option_type'], 'Strike_price':d['Strike_price']}for d in sorted_pe_options]
        sorted_ce_options_new_df = pd.DataFrame(sorted_ce_options_new_df)
        

        sorted_ce_options_new_df = sorted_ce_options_new_df.assign(**{
            'ltp':sorted_ce_options_new_df.apply(lambda sorted_ce_options_new_df : self.get_ltp_data(sorted_ce_options_new_df['exch_seg'],sorted_ce_options_new_df['symbol'],sorted_ce_options_new_df['token']), axis = 1)
        })
        sorted_pe_options_new_df = pd.DataFrame(sorted_pe_options_new_df)
        sorted_pe_options_new_df = sorted_pe_options_new_df.assign(**{
            'ltp':sorted_pe_options_new_df.apply(lambda sorted_pe_options_new_df : self.get_ltp_data(sorted_pe_options_new_df['exch_seg'],sorted_pe_options_new_df['symbol'],sorted_pe_options_new_df['token']), axis = 1)
        })
        ce_ltp_option = sorted_ce_options_new_df.loc[sorted_ce_options_new_df['ltp'].apply(lambda x: abs(x - strike_price_ltp) if x >= strike_price_ltp else float('inf')).idxmin()]
        pe_ltp_option = sorted_pe_options_new_df.loc[sorted_pe_options_new_df['ltp'].apply(lambda x: abs(x - strike_price_ltp) if x >= strike_price_ltp else float('inf')).idxmin()]
        
        
        if ce_ltp_option['ltp'] >= strike_price_ltp and pe_ltp_option['ltp'] >= strike_price_ltp:
            buy_ce_ltp_option = sorted_ce_options_new_df.loc[sorted_ce_options_new_df['ltp'].apply(lambda x: abs(x - strike_price_ltp_two) if x >= strike_price_ltp_two else float('inf')).idxmin()]
            buy_pe_ltp_option = sorted_pe_options_new_df.loc[sorted_pe_options_new_df['ltp'].apply(lambda x: abs(x - strike_price_ltp_two) if x >= strike_price_ltp_two else float('inf')).idxmin()]
            return ce_ltp_option, pe_ltp_option, buy_ce_ltp_option, buy_pe_ltp_option
        else:
            return None, None
        

def strategyone():
    all_st_data = StrategyOne.objects.all().first()

    select_index = all_st_data.select_index
    which_days = all_st_data.which_days
    which_time_start = all_st_data.which_time_start
    which_time_end = all_st_data.which_time_end
    # this_week_expiry_stike_type = all_st_data.this_week_expiry_stike_type
    sell_ce_price = all_st_data.sell_ce_price
    sell_pe_price = all_st_data.sell_pe_price
    ce_sell_profit_type = all_st_data.ce_sell_profit_type
    ce_sell_profit_value = all_st_data.ce_sell_profit_value
    pe_sell_profit_type = all_st_data.pe_sell_profit_type
    pe_sell_profit_value = all_st_data.pe_sell_profit_value
    ce_sell_sl_type = all_st_data.ce_sell_sl_type
    ce_sell_sl_value = all_st_data.ce_sell_sl_value
    pe_sell_sl_type = all_st_data.pe_sell_sl_type
    pe_sell_sl_value = all_st_data.pe_sell_sl_value
    ce_buy_price = all_st_data.ce_buy_price
    pe_buy_price = all_st_data.pe_buy_price
    nw_ce_buy_price = all_st_data.nw_ce_buy_price
    nw_pe_buy_price = all_st_data.nw_pe_buy_price

    dt = datetime.now()
    today_day = dt.strftime('%A')
    print(today_day)

    check_days_is_valid = False
    check_starttime_is_valid = False

    for i in which_days:
        if str(today_day).upper() == str(i).upper():
            check_days_is_valid = True

    converted_date = dt.year+'-'+dt.month+'-'+dt.day+' '+which_time_start+':'+'00'
    datem = datetime.strptime(converted_date, "%Y-%m-%d %H:%M:%S")

    print('Datetime is:', dt)
    print('day Name:', dt.strftime('%A'))
    
    if dt >= datem:
        check_starttime_is_valid = True 

    if check_days_is_valid == True and check_starttime_is_valid == True:
        live_data = Fetch_liveData()
        data = live_data.get_Open_Api_Data()
        IndexName = 'BANKNIFTY'
        current_exp, next_exp = live_data.get_current_exp(data=data,index_type=IndexName)

        st_data = StrategyOne.objects.all().first()

        sellce_strike_price_ltp = st_data.sell_ce_price
        sellpe_strike_price_ltp = st_data.sell_pe_price
        buyce_strike_price_ltp = st_data.ce_buy_price
        buype_strike_price_ltp = st_data.pe_buy_price
        nw_buyce_strike_price_ltp = st_data.nw_ce_buy_price
        nw_buype_strike_price_ltp = st_data.nw_pe_buy_price


        strike_price_ltp = 150
        strike_price_ltp_two = 15
        nw_strike_price_ltp_two = 150

        option = live_data.get_strike_price_by_optionType(expiry=current_exp, data=data, nameOfindex=IndexName,strike_price_ltp=strike_price_ltp,strike_price_ltp_two=strike_price_ltp_two)
        nwoption = live_data.get_strike_price_by_optionType(expiry=next_exp, data=data, nameOfindex=IndexName,strike_price_ltp=nw_strike_price_ltp_two,strike_price_ltp_two=None)
        
        ce_option = option[0]
        pe_option = option[1]
        buy_ce_option = option[2]
        buy_pe_option = option[3]

        nw_buy_ce_option = nwoption[0]
        nw_buy_pe_option = nwoption[1]
        if str(ce_option) != "None" and str(pe_option) != "None" and str(buy_ce_option) != "None" and str(buy_pe_option) != "None" and str(nw_buy_ce_option) != "None" and str(nw_buy_pe_option) != "None":
            print("ce_option---->",ce_option)
            print("pe_option---->",pe_option)
            print("buy_ce_option---->",buy_ce_option)
            print("buy_pe_option---->",buy_pe_option)
            print("nw_buy_ce_option---->",nw_buy_ce_option)
            print("nw_buy_pe_option---->",nw_buy_pe_option)

            order_id_one = uuid.uuid1()
            order_id_two = uuid.uuid1()
            order_id_three = uuid.uuid1()
            order_id_four = uuid.uuid1()
            order_id_five = uuid.uuid1()
            order_id_six = uuid.uuid1()

            order_id = order_id_one,
            variety = "NORMAL",
            tradingsymbol = ce_option['symbol'],
            symboltoken = ce_option['token'],
            transactiontype = "SELL",
            exchange = ce_option['exch_seg'],
            ordertype = "MARKET",
            producttype = "INTRADAY",
            duration = "DAY",
            price = ce_option['ltp'],
            squareoff = "0",
            stoploss = "0",
            quantity = "25",

            paper_orders.objects.create(order_id=order_id_one, variety="NORMAL", tradingsymbol=ce_option['symbol'],)

            pass

    pass