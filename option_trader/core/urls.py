from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('stratedy_one_edit/', views.stratedy_one_edit, name='stratedy_one_edit'),
    path('stratedy_one/', views.stratedy_one, name='stratedy_one'),
    path('trade_hst/', views.trade_history, name='trade_hst'),
    path('edit_st_one/', csrf_exempt(views.StrategyOneSave.as_view()), name='edit_st_one'),
    path('get-trad-history/', views.getPaperOrders, name='get_trad_history'),

]