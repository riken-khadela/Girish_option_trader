from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
import json
from django.utils import timezone
from .models import Strategymain, Strategy, StrategyOne, paper_orders
from .strategy_one import Fetch_liveData
from datetime import datetime

# Create your views here.
class StrategyData(APIView): 

    def post(self, request):

        st_data = request.data

        select_index_bool = False
        strategy_start_time_bool = False
        strategy_end_time_bool = False
        strategy_list_bool = False

        select_index_param = request.data.get('select index')
        if select_index_param is not None:
            if str(st_data['select index']).replace(' ','') != "":
                select_index_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "select index is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "select index is Required"
            }
            return Response(get_pre)

        strategy_start_time_param = request.data.get('strategy start time')
        if strategy_start_time_param is not None:
            if str(st_data['strategy start time']).replace(' ','') != "":
                strategy_start_time_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "strategy start time is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "strategy start time is Required"
            }
            return Response(get_pre)

        strategy_end_time_param = request.data.get('strategy end time')
        if strategy_end_time_param is not None:
            if str(st_data['strategy end time']).replace(' ','') != "":
                strategy_end_time_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "strategy end time is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "strategy end time is Required"
            }
            return Response(get_pre)
    
        strategy_list_param = request.data.get('strategy list')
        if strategy_list_param is not None:
            if str(st_data['strategy list']).replace(' ','') != "":
                strategy_list_bool = True
            else :
                get_pre = {
                    "success": False,
                    "message": "strategy list is Required"
                }
                return Response(get_pre)
        else :
            get_pre = {
                "success": False,
                "message": "strategy list is Required"
            }
            return Response(get_pre)

        if select_index_bool == False and strategy_start_time_bool == False and strategy_end_time_bool == False and strategy_list_bool == False:
            print("Das")

            strategy_list = json.load(st_data['strategy list'])
            
            select_index = st_data['select index']
            strategy_start_time = st_data['strategy start time']
            strategy_end_time = st_data['strategy end time']

            std_data = Strategymain.objects.create(select_index=select_index, strategy_start_time=strategy_start_time, strategy_end_time=strategy_end_time)
            for strategy_data in strategy_list:
                if 'total lot' in strategy_data and 'position' in strategy_data and 'option type' in strategy_data and 'expiry' in strategy_data and 'select strike criteria' in strategy_data and 'take profit' in strategy_data and 'stop loss' in strategy_data and 'trail stop loss' in strategy_data:
                    

                    total_lot = strategy_data['total lot']
                    position = strategy_data['position']
                    option_type = strategy_data['option type']
                    expiry = strategy_data['expiry']
                    select_strike_criteria = strategy_data['select strike criteria']
                    take_profit = strategy_data['take profit']
                    stop_loss = strategy_data['stop loss']
                    trail_stop_loss = strategy_data['trail stop loss']
                    strike_criteria_type = select_strike_criteria['type']

                    take_profit_type = take_profit['type']
                    take_profit_value = take_profit['value']

                    stop_loss_type = stop_loss['type']
                    stop_loss_value = stop_loss['value']

                    trail_stop_loss_type = trail_stop_loss['type']
                    trail_stop_loss_value = trail_stop_loss['value']


                    if strike_criteria_type == "PREMIUM RANGE":
                        strike_criteria_lower_range = select_strike_criteria['lower range']
                        strike_criteria_upper_range = select_strike_criteria['upper range']

                        Strategy.objects.create(total_lot=total_lot, position=position, option_type=option_type, expiry=expiry, strike_criteria_type=strike_criteria_type, strike_criteria_lower_range=strike_criteria_lower_range, strike_criteria_upper_range=strike_criteria_upper_range, take_profit_type=take_profit_type, take_profit_value=take_profit_value, stop_loss_type=stop_loss_type, stop_loss_value=stop_loss_value, trail_stop_loss_type=trail_stop_loss_type, trail_stop_loss_value=trail_stop_loss_value, strategy_data_id=std_data.id)

                    elif strike_criteria_type == "STRIKE TYPE":
                        strike_criteria_strike_type = select_strike_criteria['strike type']

                        Strategy.objects.create(total_lot=total_lot, position=position, option_type=option_type, expiry=expiry, strike_criteria_type=strike_criteria_type, strike_criteria_strike_type=strike_criteria_strike_type, take_profit_type=take_profit_type, take_profit_value=take_profit_value, stop_loss_type=stop_loss_type, stop_loss_value=stop_loss_value, trail_stop_loss_type=trail_stop_loss_type, trail_stop_loss_value=trail_stop_loss_value, strategy_data_id=std_data.id)

                    elif strike_criteria_type == "CLOSEST PREMIUM":
                        strike_criteria_premium = select_strike_criteria['premium']

                        Strategy.objects.create(total_lot=total_lot, position=position, option_type=option_type, expiry=expiry, strike_criteria_type=strike_criteria_type, strike_criteria_premium=strike_criteria_premium, take_profit_type=take_profit_type, take_profit_value=take_profit_value, stop_loss_type=stop_loss_type, stop_loss_value=stop_loss_value, trail_stop_loss_type=trail_stop_loss_type, trail_stop_loss_value=trail_stop_loss_value, strategy_data_id=std_data.id)
                        
                    

                else:
                    get_pre = {
                        "success": False,
                        "message": "fileds are Required"
                    }
                    return Response(get_pre)

        else:
            get_pre = {
                "success": False,
                "message": "all fileds are Required"
            }
            return Response(get_pre)


def stratedy_one_edit(request):
    st_data = StrategyOne.objects.all().first()
    live_data = Fetch_liveData()
    data = live_data.get_Open_Api_Data()
    IndexName = 'BANKNIFTY'
    all_exp = live_data.get_all_exp(data=data,index_type=IndexName)

    if st_data != None:
        return render(request, 'strategy_one_edit.html', {"st_data":st_data,"all_exp":all_exp})
    else:
        return render(request, 'strategy_one_edit.html',{"all_exp":all_exp})

def stratedy_one(request):
    st_data = StrategyOne.objects.all().first()

    
    return render(request, 'strategy_one.html', {"st_data":st_data})
    # return render(request, 'strategy_one.html'  )

def trade_history(request):
    return render(request, 'trade_hst.html')


class StrategyOneSave(APIView):
    def post(self, request):
        if 'select_index' in request.data and 'start_time' in request.data and 'end_time' in request.data and 'day_monday' in request.data and 'day_tuseday' in request.data and 'day_wednesday' in request.data and 'day_thursday' in request.data and 'day_friday' in request.data and 'sell_twce_price' in request.data and 'sell_twce_profit_type' in request.data and 'sell_twce_profit_value' in request.data and 'sell_twce_sl_type' in request.data and 'sell_twce_sl_value' in request.data and 'sell_twpe_price' in request.data and 'sell_twpe_profit_type' in request.data and 'sell_twpe_profit_value' in request.data and 'sell_twpe_sl_type' in request.data and 'sell_twpe_sl_value' in request.data and 'buy_twce_price' in request.data and 'buy_twpe_price' in request.data and 'buy_nwce_price' in request.data and 'buy_nwpe_price' in request.data:
            select_index = request.data['select_index']
            start_time = request.data['start_time']
            end_time = request.data['end_time']
            day_monday = request.data['day_monday']
            day_tuseday = request.data['day_tuseday']
            day_wednesday = request.data['day_wednesday']
            day_thursday = request.data['day_thursday']
            day_friday = request.data['day_friday']
            sell_twce_price = request.data['sell_twce_price']
            sell_twce_profit_type = request.data['sell_twce_profit_type']
            sell_twce_profit_value = request.data['sell_twce_profit_value']
            sell_twce_sl_type = request.data['sell_twce_sl_type']
            sell_twce_sl_value = request.data['sell_twce_sl_value']
            sell_twpe_price = request.data['sell_twpe_price']
            sell_twpe_profit_type = request.data['sell_twpe_profit_type']
            sell_twpe_profit_value = request.data['sell_twpe_profit_value']
            sell_twpe_sl_type = request.data['sell_twpe_sl_type']
            sell_twpe_sl_value = request.data['sell_twpe_sl_value']
            buy_twce_price = request.data['buy_twce_price']
            buy_twpe_price = request.data['buy_twpe_price']
            buy_nwce_price = request.data['buy_nwce_price']
            buy_nwpe_price = request.data['buy_nwpe_price']

            repeat_order_type = request.data['repeat_order_type']
            expiry_selecter = request.data['expiry_selecter']
            sell_twce_lot = request.data['sell_twce_lot']
            sell_twpe_lot = request.data['sell_twpe_lot']
            buy_twce_lot = request.data['buy_twce_lot']
            buy_twpe_lot = request.data['buy_twpe_lot']
            buy_nwce_lot = request.data['buy_nwce_lot']
            buy_nwpe_lot = request.data['buy_nwpe_lot']

            check_day_bool = ["true", "false"]
            check_type_bool = ["POINTS", "PERCENTAGE"]
            check_index_bool = ["BANKNIFTY", "NIFTY", "FINNIFTY"]
            check_repeat_type_bool = ["REPEAT", "NO REPEAT"]

            if str(select_index).upper() in check_index_bool:
                if str(repeat_order_type).upper() in check_repeat_type_bool:
                    if str(start_time).strip() != "" and str(end_time).strip() != "":
                        if str(day_monday).lower() in check_day_bool and str(day_tuseday).lower() in check_day_bool and str(day_wednesday).lower() in check_day_bool and str(day_thursday).lower() in check_day_bool and str(day_friday).lower() in check_day_bool:
                            if float(sell_twce_price) != 0 and float(sell_twce_profit_value) != 0 and float(sell_twce_sl_value) != 0 and float(sell_twpe_price) != 0 and float(sell_twpe_profit_value) != 0 and float(sell_twpe_sl_value) != 0 and float(buy_twce_price) != 0 and float(buy_twpe_price) != 0 and float(buy_nwce_price) != 0 and float(buy_nwpe_price) != 0 and float(sell_twce_lot) != 0 and float(sell_twpe_lot) != 0 and float(buy_twce_lot) != 0 and float(buy_twpe_lot) != 0 and float(buy_nwce_lot) != 0 and float(buy_nwpe_lot) != 0:
                                if str(sell_twce_profit_type).upper() in check_type_bool and str(sell_twce_sl_type).upper() in check_type_bool and str(sell_twpe_profit_type).upper() in check_type_bool and str(sell_twpe_sl_type).upper() in check_type_bool:
                                    if str(expiry_selecter).strip() != "":

                                        # start_time_list = str(start_time).split(":")
                                        # start_time_hh = start_time_list[0]
                                        # start_time_mm = start_time_list[1]

                                        # end_time_list = str(end_time).split(":")
                                        # end_time_hh = end_time_list[0]
                                        # end_time_mm = end_time_list[1]

                                        all_day_list = []

                                        if day_monday == "true":
                                            all_day_list.append("MONDAY") 
                                        if day_tuseday == "true":
                                            all_day_list.append("TUESDAY")
                                        if day_wednesday == "true":
                                            all_day_list.append("WEDNESDAY")
                                        if day_thursday == "true":
                                            all_day_list.append("THURSDAY")
                                        if day_friday == "true":
                                            all_day_list.append("FRIDAY")
                                        
                                        if len(all_day_list) != 0:


                                            dbdata = StrategyOne.objects.all().first()
                                            if dbdata != None:
                                                StrategyOne.objects.filter(id=dbdata.id).update(
                                                    select_index = str(select_index).upper(),
                                                    repeat_order_type = str(repeat_order_type).upper(),
                                                    current_expiry_date = expiry_selecter,
                                                    which_days = all_day_list,
                                                    which_time_start = start_time,
                                                    which_time_end = end_time,
                                                    sell_ce_price = sell_twce_price,
                                                    sell_pe_price = sell_twpe_price,
                                                    ce_sell_profit_type = str(sell_twce_profit_type).upper(),
                                                    ce_sell_profit_value = sell_twce_profit_value,
                                                    pe_sell_profit_type = str(sell_twpe_profit_type).upper(),
                                                    pe_sell_profit_value = sell_twpe_profit_value,
                                                    ce_sell_sl_type = str(sell_twce_sl_type).upper(),
                                                    ce_sell_sl_value = sell_twce_sl_value,
                                                    pe_sell_sl_type = str(sell_twpe_sl_type).upper(),
                                                    pe_sell_sl_value = sell_twpe_sl_value,
                                                    ce_buy_price = buy_twce_price,
                                                    pe_buy_price = buy_twpe_price,
                                                    nw_ce_buy_price = buy_nwce_price,
                                                    nw_pe_buy_price = buy_nwpe_price,
                                                    sell_ce_lot = sell_twce_lot,
                                                    sell_pe_lot = sell_twpe_lot,
                                                    ce_buy_lot = buy_twce_lot,
                                                    pe_buy_lot = buy_twpe_lot,
                                                    nw_ce_buy_lot = buy_nwce_lot,
                                                    nw_pe_buy_lot = buy_nwpe_lot
                                                )
                                                
                                            else:
                                                StrategyOne.objects.create(
                                                    select_index = str(select_index).upper(),
                                                    repeat_order_type = str(repeat_order_type).upper(),
                                                    current_expiry_date = expiry_selecter,
                                                    which_days = all_day_list,
                                                    which_time_start = start_time,
                                                    which_time_end = end_time,
                                                    sell_ce_price = sell_twce_price,
                                                    sell_pe_price = sell_twpe_price,
                                                    ce_sell_profit_type = str(sell_twce_profit_type).upper(),
                                                    ce_sell_profit_value = sell_twce_profit_value,
                                                    pe_sell_profit_type = str(sell_twpe_profit_type).upper(),
                                                    pe_sell_profit_value = sell_twpe_profit_value,
                                                    ce_sell_sl_type = str(sell_twce_sl_type).upper(),
                                                    ce_sell_sl_value = sell_twce_sl_value,
                                                    pe_sell_sl_type = str(sell_twpe_sl_type).upper(),
                                                    pe_sell_sl_value = sell_twpe_sl_value,
                                                    ce_buy_price = buy_twce_price,
                                                    pe_buy_price = buy_twpe_price,
                                                    nw_ce_buy_price = buy_nwce_price,
                                                    nw_pe_buy_price = buy_nwpe_price,
                                                    sell_ce_lot = sell_twce_lot,
                                                    sell_pe_lot = sell_twpe_lot,
                                                    ce_buy_lot = buy_twce_lot,
                                                    pe_buy_lot = buy_twpe_lot,
                                                    nw_ce_buy_lot = buy_nwce_lot,
                                                    nw_pe_buy_lot = buy_nwpe_lot
                                                )
                                            response = {"data": "", "error_bool":"False", "message": "Success"}
                                            return Response(response)
                                        else:
                                            print("select at validate date")
                                            response = {"data": "", "error_bool":"True", "message": "error"}
                                            return Response(response)
                                    else:
                                        print("select at list one day")
                                        response = {"data": "", "error_bool":"True", "message": "error"}
                                        return Response(response)
                                else:
                                    print("please check select type")
                                    response = {"data": "", "error_bool":"True", "message": "error"}
                                    return Response(response)
                            else:
                                print("please check all number values")
                                response = {"data": "", "error_bool":"True", "message": "error"}
                                return Response(response)
                        else:
                            print("select valid day")
                            response = {"data": "", "error_bool":"True", "message": "error"}
                            return Response(response)
                    else:
                        print("select valid time")
                        response = {"data": "", "error_bool":"True", "message": "error"}
                        return Response(response)
                else:
                    print("select valid type")
                    response = {"data": "", "error_bool":"True", "message": "error"}
                    return Response(response)
            else:
                print("select valid index")
                response = {"data": "", "error_bool":"True", "message": "error"}
                return Response(response)
        else:
            print("select valid index")
            response = {"data": "", "error_bool":"True", "message": "error"}
            return Response(response)



def getPaperOrders(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_datetime = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date_str, "%Y-%m-%d")

    start_datetime = start_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
    end_datetime = end_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)

    start_datetime = timezone.make_aware(start_datetime)
    end_datetime = timezone.make_aware(end_datetime)

    orders = paper_orders.objects.filter(created_at__range=(start_datetime, end_datetime))
    if orders:
        data = []
        for order in orders:
            time = order.created_at.strftime('%H:%M:%S')
            order_data = {
                'order_id': order.order_id,
                'time': time,
                'tradingsymbol': order.tradingsymbol,
                'ordertype': order.transactiontype,
                'position_close':order.position_close,
                'exchange': order.exchange,
                'duration': order.duration,
                'quantity': order.quantity,
                'price': order.price,
                'squareoff': order.squareoff,
                'stoploss': order.stoploss,                             
            }
            data.append(order_data)

        return JsonResponse(data, safe=False)

