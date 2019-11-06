var u_login_url = "/inuser"
var u_get_wallet_url = "/ud/wallet"
var u_get_open_orders_url = "/ud/oorders"
var u_get_last_prices_url = "/lastprices"
var u_cancel_open_order_url = "/ocancel"
var u_sell_limit_url = "/lsell"
var u_buy_limit_url = "/lbuy"
var u_get_pair_fee_url = "/pairfee"

function post(url, data, callback) {
    $.post(url, data, function (resp, code) {
        callback(resp, code)
    });
}

function loginUser(uname, pass, callback){
    var udata = {"uname": uname,
    "upass": pass};
    post(u_login_url, udata, callback);
}

function print(msg, code){
    console.log(msg)
}

function get_user_wallet(callback){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name}
        post(u_get_wallet_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function get_user_open_orders(callback){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name}
        post(u_get_open_orders_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function get_last_prices(callback){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name}
        post(u_get_last_prices_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function cancel_open_order(callback, orderid, pair, amount, price, fee){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name,
                     "pair":pair,
                     "orderId":orderid,
                     "amount":amount,
                     "price":price,
                     "fee":fee}
        post(u_cancel_open_order_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function sell_limit(callback, pair, amount, price, fee){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name,
                     "pair":pair,
                     "amount":amount,
                     "price":price,
                     "fee":fee}
        post(u_sell_limit_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function buy_limit(callback, pair, amount, price, fee){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name,
                     "pair":pair,
                     "amount":amount,
                     "price":price,
                     "fee":fee}
        post(u_buy_limit_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}

function get_pair_fee(callback, pair){
    if (logged_in_user_name !=null){
        var udata = {"uname":logged_in_user_name, "pair":pair}
        post(u_get_pair_fee_url, udata, callback)
    }else{
        alert("User is not Logged in!")
    }
}