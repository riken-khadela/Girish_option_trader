from django.db import models
from django.db.models.base import Model, ModelBase
# from .models import enums
from django.db.models.fields import CharField
from django.core.validators import validate_comma_separated_integer_list
from django.db.models.fields.related import ForeignKey
from django.contrib.postgres.fields import ArrayField

# Create your models here.

POSITION_TYPE = (
    ('BUY','BUY'),
    ('SELL','SELL'),
)

OPTION_TYPE = (
    ('CALL','CALL'),
    ('PUT','PUT'),
)

EXPITY_TYPE = (
    ('WEEKLY','WEEKLY'),
    ('NEXT WEEKLY','NEXT WEEKLY'),
    ('MONTHLY','MONTHLY'),
)

STRIKE_CRITERIA_TYPE = (
    ('STRIKE TYPE','STRIKE TYPE'),
    ('PREMIUM RANGE','PREMIUM RANGE'),
    ('CLOSEST PREMIUM','CLOSEST PREMIUM'),
)

TAKE_PROFIT_TYPE = (
    ('POINTS','POINTS'),
    ('PERCENTAGE','PERCENTAGE'),
)

STOP_LOSS_TYPE = (
    ('POINTS','POINTS'),
    ('PERCENTAGE','PERCENTAGE'),
)

TRAIL_STOP_LOSS_TYPE = (
    ('POINTS','POINTS'),
    ('PERCENTAGE','PERCENTAGE'),
)

SELECT_INDEX = (
    ('BANKNIFTY','BANKNIFTY'),
    ('NIFTY','NIFTY'),
    ('FINNIFTY','FINNIFTY'),
)

SELECT_REPEAT_TYPE = (
    ('REPEAT', 'REPEAT'),
    ('NO REPEAT','NO REPEAT'),
)
SELECT_POSITION_CLOSE = (
    ('TRUE', 'TRUE'),
    ('FALSE','FALSE'),
)

class Strategymain(models.Model):
    select_index = models.CharField(choices=SELECT_INDEX, max_length=100, null=False)
    strategy_start_time = models.CharField(max_length=255, null=False)
    strategy_end_time = models.CharField(max_length=255, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

class Strategy(models.Model):
    total_lot = models.IntegerField(null=False)
    position = models.CharField(choices=POSITION_TYPE, max_length=100, null=False)
    option_type = models.CharField(choices=OPTION_TYPE, max_length=100, null=False)
    expiry = models.CharField(choices=EXPITY_TYPE, max_length=100, null=False)
    strike_criteria_type = models.CharField(choices=STRIKE_CRITERIA_TYPE, max_length=100, null=False)
    strike_criteria_lower_range = models.IntegerField(null=True)
    strike_criteria_upper_range = models.IntegerField(null=True)
    strike_criteria_strike_type = models.CharField(max_length=100, null=True)
    strike_criteria_premium = models.IntegerField(null=True)
    take_profit_type = models.CharField(choices=TAKE_PROFIT_TYPE, max_length=100, null=False)
    take_profit_value = models.IntegerField(null=False)
    stop_loss_type = models.CharField(choices=STOP_LOSS_TYPE, max_length=100, null=False)
    stop_loss_value = models.IntegerField(null=False)
    trail_stop_loss_type = models.CharField(choices=TRAIL_STOP_LOSS_TYPE, max_length=100, null=False)
    trail_stop_loss_value_one = models.IntegerField(null=False)
    trail_stop_loss_value_two = models.IntegerField(null=False)
    strategy_data = ForeignKey(Strategymain, on_delete=models.CASCADE, related_name="strategy_data_id", null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

class StrategyOne(models.Model):    
    select_index = models.CharField(choices=SELECT_INDEX, max_length=100, null=False)
    which_days = ArrayField(models.CharField(max_length=20, blank=True),size=8,)
    which_time_start = models.CharField(max_length=20, blank=True)
    which_time_end = models.CharField(max_length=20, blank=True)
    repeat_order_type = models.CharField(choices=SELECT_REPEAT_TYPE, max_length=255, null=False)
    current_expiry_date = models.CharField(max_length=255, blank=True)
    # this_week_expiry_stike _type = models.CharField(max_length=255, blank=True)
    sell_ce_price = models.CharField(max_length=255, blank=True)
    sell_pe_price = models.CharField(max_length=255, blank=True)
    sell_ce_lot = models.CharField(max_length=255, blank=True)
    sell_pe_lot = models.CharField(max_length=255, blank=True)
    ce_sell_profit_type = models.CharField(choices=TAKE_PROFIT_TYPE, max_length=255, null=False)
    ce_sell_profit_value = models.CharField(max_length=255, blank=True)
    pe_sell_profit_type = models.CharField(choices=TAKE_PROFIT_TYPE, max_length=255, null=False)
    pe_sell_profit_value = models.CharField(max_length=255, blank=True)
    ce_sell_sl_type = models.CharField(choices=STOP_LOSS_TYPE, max_length=255, null=False)
    ce_sell_sl_value = models.CharField(max_length=255, blank=True)
    pe_sell_sl_type = models.CharField(choices=STOP_LOSS_TYPE, max_length=255, null=False)
    pe_sell_sl_value = models.CharField(max_length=255, blank=True)
    ce_buy_price = models.CharField(max_length=255, blank=True)
    pe_buy_price = models.CharField(max_length=255, blank=True)
    ce_buy_lot = models.CharField(max_length=255, blank=True)
    pe_buy_lot = models.CharField(max_length=255, blank=True)
    nw_ce_buy_price = models.CharField(max_length=255, blank=True)
    nw_pe_buy_price = models.CharField(max_length=255, blank=True)
    nw_ce_buy_lot = models.CharField(max_length=255, blank=True)
    nw_pe_buy_lot = models.CharField(max_length=255, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)



class paper_orders(models.Model):
    order_id = models.TextField(unique=True)
    name_of_index = models.CharField(max_length=255)
    variety = models.CharField(max_length=255)
    tradingsymbol = models.CharField(max_length=255)
    symboltoken = models.CharField(max_length=255)
    transactiontype = models.CharField(max_length=255)
    exchange = models.CharField(max_length=255)
    ordertype = models.CharField(max_length=255)
    producttype = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    squareoff = models.CharField(max_length=255)
    stoploss = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    position_close = models.CharField(choices=SELECT_POSITION_CLOSE, max_length=100, default="FALSE")
    match_id = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


# class paper_position(models.Model):
#     order = ForeignKey(paper_orders, on_delete=models.CASCADE, related_name='order_position_id', blank=True, null=True)


class paper_accounts(models.Model):
    account_id = models.TextField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    account_balance = models.CharField(max_length=255)
    possition = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)