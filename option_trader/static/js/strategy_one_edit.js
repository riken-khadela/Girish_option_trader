// this is for Ajax CSRF_TOKEN ((((((  DO NOT CHANGE IT/ REMOVE  ))))))

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

// END AJAX CSRF_TOKEN 

$(document).on('click', '#edit_save_btn', function () { 
    var select_index = $('#select_index').val();
    var start_time = $('#start_time').val();
    var end_time = $('#end_time').val();
    var day_monday = $('#day_monday').is(":checked");
    var day_tuseday = $('#day_tuseday').is(":checked");
    var day_wednesday = $('#day_wednesday').is(":checked");
    var day_thursday = $('#day_thursday').is(":checked");
    var day_friday = $('#day_friday').is(":checked");
    var sell_twce_price = $('#sell_twce_price').val();
    var sell_twce_profit_type = $('#sell_twce_profit_type').val();
    var sell_twce_profit_value = $('#sell_twce_profit_value').val();
    var sell_twce_sl_type = $('#sell_twce_sl_type').val();
    var sell_twce_sl_value = $('#sell_twce_sl_value').val();
    var sell_twpe_price = $('#sell_twpe_price').val();
    var sell_twpe_profit_type = $('#sell_twpe_profit_type').val();
    var sell_twpe_profit_value = $('#sell_twpe_profit_value').val();
    var sell_twpe_sl_type = $('#sell_twpe_sl_type').val();
    var sell_twpe_sl_value = $('#sell_twpe_sl_value').val();
    var buy_twce_price = $('#buy_twce_price').val();
    var buy_twpe_price = $('#buy_twpe_price').val();
    var buy_nwce_price = $('#buy_nwce_price').val();
    var buy_nwpe_price = $('#buy_nwpe_price').val();

    var repeat_order_type = $('#repeat_order_type').val();
    var expiry_selecter = $('#expiry_selecter').val();
    var sell_twce_lot = $('#sell_twce_lot').val();
    var sell_twpe_lot = $('#sell_twpe_lot').val();
    var buy_twce_lot = $('#buy_twce_lot').val();
    var buy_twpe_lot = $('#buy_twpe_lot').val();
    var buy_nwce_lot = $('#buy_nwce_lot').val();
    var buy_nwpe_lot = $('#buy_nwpe_lot').val();


    // console.log("select_index",select_index);
    // console.log("start_time",start_time);
    // console.log("end_time",end_time);
    // console.log("day_monday",day_monday);
    // console.log("day_tuseday",day_tuseday);
    // console.log("day_wednesday",day_wednesday);
    // console.log("day_thursday",day_thursday);
    // console.log("day_friday",day_friday);
    // console.log("sell_twce_price",sell_twce_price);
    // console.log("sell_twce_profit_type",sell_twce_profit_type);
    // console.log("sell_twce_profit_value",sell_twce_profit_value);
    // console.log("sell_twce_sl_type",sell_twce_sl_type);
    // console.log("sell_twce_sl_value",sell_twce_sl_value);
    // console.log("sell_twpe_price",sell_twpe_price);
    // console.log("sell_twpe_profit_type",sell_twpe_profit_type);
    // console.log("sell_twpe_profit_value",sell_twpe_profit_value);
    // console.log("sell_twpe_sl_type",sell_twpe_sl_type);
    // console.log("sell_twpe_sl_value",sell_twpe_sl_value);
    // console.log("buy_twce_price",buy_twce_price);
    // console.log("buy_twpe_price",buy_twpe_price);
    // console.log("buy_nwce_price",buy_nwce_price);
    // console.log("buy_nwpe_price",buy_nwpe_price);



        
    $.ajax({
        url: `/edit_st_one/`,
        type: "POST",
        data:{
            "select_index":select_index,
            "start_time":start_time,
            "end_time":end_time,
            "day_monday":day_monday,
            "day_tuseday":day_tuseday,
            "day_wednesday":day_wednesday,
            "day_thursday":day_thursday,
            "day_friday":day_friday,
            "sell_twce_price":sell_twce_price,
            "sell_twce_profit_type":sell_twce_profit_type,
            "sell_twce_profit_value":sell_twce_profit_value,
            "sell_twce_sl_type":sell_twce_sl_type,
            "sell_twce_sl_value":sell_twce_sl_value,
            "sell_twpe_price":sell_twpe_price,
            "sell_twpe_profit_type":sell_twpe_profit_type,
            "sell_twpe_profit_value":sell_twpe_profit_value,
            "sell_twpe_sl_type":sell_twpe_sl_type,
            "sell_twpe_sl_value":sell_twpe_sl_value,
            "buy_twce_price":buy_twce_price,
            "buy_twpe_price":buy_twpe_price,
            "buy_nwce_price":buy_nwce_price,
            "buy_nwpe_price":buy_nwpe_price,
            "repeat_order_type":repeat_order_type,
            "expiry_selecter":expiry_selecter,
            "sell_twce_lot":sell_twce_lot,
            "sell_twpe_lot":sell_twpe_lot,
            "buy_twce_lot":buy_twce_lot,
            "buy_twpe_lot":buy_twpe_lot,
            "buy_nwce_lot":buy_nwce_lot,
            "buy_nwpe_lot":buy_nwpe_lot,

        },
        // contentType: false,
        // processData: false,
        success: function(data){
            if(data['error_bool'] == "False"){
                console.log("::--->",data); 
                // redirect show data page
                new_url = window.location.origin + "/stratedy_one"
                window.location.replace(new_url);
            }
            else{
                console.log(data); 
            }
        }
    });
     

});

$(document).on('click', '#edit_close_btn', function () { 
// redirect show data page
new_url = window.location.origin + "/stratedy_one"
window.location.replace(new_url);
});

