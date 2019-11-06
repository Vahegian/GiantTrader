var login_butt = "top_user_login_button";
var uname_text = document.getElementById("top_username_input");
var pass_text = document.getElementById("top_user_password_input");
var ulist = document.getElementById("top_logged_users_list");
var user_wallet_table = document.getElementById("user_wallet_table");
var user_open_orders_table = document.getElementById("user_open_orders_table");
var user_wallet_table_total = document.getElementById("user_wallet_table_total");

var user_Limit_order_amount_text = document.getElementById("user_Limit_order_amount_text");
var user_Limit_order_price_text = document.getElementById("user_Limit_order_price_text");
var user_Limit_sell_select_button = document.getElementById("user_Limit_sell_select_button");
var user_Limit_buy_select_button = document.getElementById("user_Limit_buy_select_button");
var user_Limit_place_order_button = document.getElementById("user_Limit_place_order_button");
var user_Limit_order_pair_options = document.getElementById("user_Limit_order_pair_options");


var default_asset = "USDT";

var logged_in_user_name = null;
var can_update_user_data = false;
var user_update_interval = null;
var started_update_timer = false;

var last_prices = null;
var last_open_orders = null;
var last_wallet_state = null;
var sorted_pairs = null;
var pairs_fees = null;

var total_money_in_wallet = 0.0;

var open_orders_cancel_button_listeners = {} // remember to clear this when user is changed 

var user_Limit_order_side = 0; // 0-buy, 1-sell

function update_pair_fees(data, code) {
    if (pairs_fees == null) {
        pairs_fees = {};
        pairs_fees[data.symbol] = data.taker
    } else {
        pairs_fees[data.symbol] = data.taker
    }
}

function update_user_limit_order_side(side) {
    if (side == 0) {
        user_Limit_sell_select_button.setAttribute("class", "btn bg-white");
        user_Limit_buy_select_button.setAttribute("class", "btn btn-success");
    } else if (side == 1) {
        user_Limit_sell_select_button.setAttribute("class", "btn btn-danger");
        user_Limit_buy_select_button.setAttribute("class", "btn bg-white");
    }
}

function update_user_data_if_success(data, code){
    if (data["status"]==1){
        update_user_data();
    }
}

function set_user_limit_order_side_button_listeners() {
    user_Limit_order_pair_options.addEventListener("click", function () {
        if (last_prices != null) {
            if (sorted_pairs == null) {
                alert("Getting pairs might take a while. Please wait!")
                var pairs = Object.keys(last_prices)
                sorted_pairs = []
                for (var index in pairs) {
                    if (pairs[index].substr(pairs[index].length - 4) == "USDT") {
                        sorted_pairs.push(pairs[index])
                        get_pair_fee(update_pair_fees, pairs[index])
                    }
                }
                sorted_pairs.sort();
                alert("Pairs are ready!")
            }
            for (var index in sorted_pairs) {
                var option_item = document.createElement("option");
                var text_item = document.createTextNode(sorted_pairs[index]);
                option_item.appendChild(text_item);
                user_Limit_order_pair_options.appendChild(option_item)
            }
        }
    });

    user_Limit_sell_select_button.addEventListener("click", function () {
        user_Limit_order_side = 1;
        update_user_limit_order_side(user_Limit_order_side)
    });

    user_Limit_buy_select_button.addEventListener("click", function () {
        user_Limit_order_side = 0;
        update_user_limit_order_side(user_Limit_order_side)
    });

    user_Limit_place_order_button.addEventListener("click", function () {
        try {
            var order_pair = user_Limit_order_pair_options.value
            var order_amount = parseFloat(user_Limit_order_amount_text.value)
            var order_price = parseFloat(user_Limit_order_price_text.value)
            if (order_amount * order_price >= 10.0) {
                if (user_Limit_order_side==1){
                    sell_limit(update_user_data_if_success, order_pair, order_amount, order_price, pairs_fees[order_pair])
                }else if(user_Limit_order_side==0){
                    buy_limit(update_user_data_if_success, order_pair, order_amount, order_price, pairs_fees[order_pair])                    
                }
                user_Limit_order_amount_text.value =''
                user_Limit_order_price_text.value=''
            }
        } catch{
            alert("Limit order: typed data is inaccurate!")
        }
    });
}

function on_login_clicked(callback) {
    $(document).on('click', "#" + login_butt, function () {
        var uname = uname_text.value
        var upass = pass_text.value
        callback(uname, upass, show_user)
    });
}

function show_user(data, code) {
    if (data.status == 1) {
        ulist.innerHTML = `
        <li class="list-inline-item">`+ data.uname + `</li>`
        logged_in_user_name = data.uname
    } else {
        alert("Login failed!")
    }
}

function update_user_open_orders(data, code) {
    // console.log(data+"uuoo")
    last_open_orders = data
}

function update_user_wallet(data, code) {
    last_wallet_state = data;
}

function update_user_last_prices(data, code) {
    last_prices = data;
    // console.log(data)
}

function check_user_login_status() {
    if (logged_in_user_name != null) {
        can_update_user_data = true
        if (!started_update_timer) {
            update_user_data()
            user_update_interval = setInterval(update_user_data, 300000);
            started_update_timer = true
        }
    } else {
        can_update_user_data = false
        clearInterval(user_update_interval)
        started_update_timer = false
    }
}

function update_user_data() {
    if (can_update_user_data) {
        get_user_wallet(update_user_wallet)
        get_user_open_orders(update_user_open_orders)
    }
}

function get_total_price_of_asset(asset, free, locked) {
    var total_of_asset = parseFloat(free) + parseFloat(locked);
    var pair_to_check_with = ["BTC", "ETH", "BNB", "XRP"]
    if (asset == "USDT" || asset == "USDC") {
        total_money_in_wallet += total_of_asset;
        return total_of_asset;
    }
    if (last_prices[asset + default_asset]) {
        var total = total_of_asset * parseFloat(last_prices[asset + default_asset]);
        total_money_in_wallet += total;
        return total;
    } else {
        for (var index in pair_to_check_with) {
            var asset_pair_price = last_prices[asset + pair_to_check_with[index]]
            if (asset_pair_price) {
                var pair_price = last_prices[pair_to_check_with[index] + default_asset]
                var total = total_of_asset * (parseFloat(asset_pair_price) * parseFloat(pair_price))
                total_money_in_wallet += total;
                return total;
            }
        }
        return 0.0
    }
}

function cancel_and_remove_open_order(data, code) {
    // console.log(data)
    if (data["status"] == 1) {
        delete open_orders_cancel_button_listeners[data.orderID]; // uncomment to remove order item
        update_user_data();
    }
}

function get_cancel_button_for_open_orders(order) {
    var html_cancel_button = `<button id=` + order.orderId + ` class="btn btn-danger"
    type="button">Cancel</button>`;

    if (!open_orders_cancel_button_listeners[order.orderId]) {
        $(document).on('click', "#" + order.orderId, function () {
            console.log("will implement Cancel")
            cancel_open_order(cancel_and_remove_open_order, order.orderId, order.symbol,
                order.origQty, order.price, order.fee);
        });
        open_orders_cancel_button_listeners[order.orderId] = true;
    }
    return html_cancel_button;

}

function update_UI() {
    if (can_update_user_data) {
        get_last_prices(update_user_last_prices);
    }

    if (last_wallet_state != null) {
        user_wallet_table.innerHTML = '';
        total_money_in_wallet = 0.0; // to prevent adding same numbers over again
        for (var key in last_wallet_state) {
            // console.log(key+"::"+data[key])
            var values = `<tr >
            <td>`+ key + `</td>
            <td> `+ last_wallet_state[key].free + `</td>
            <td>`+ last_wallet_state[key].locked + `</td>
            <td>`+ get_total_price_of_asset(key, last_wallet_state[key].free, last_wallet_state[key].locked).toFixed(4) + `</td>
            </tr>`
            user_wallet_table.innerHTML += values;
        }
        user_wallet_table_total.innerHTML = default_asset + " " + parseFloat(total_money_in_wallet).toFixed(4)
    } else {
        user_wallet_table.innerHTML = '';
    }

    if (last_open_orders != null) {
        user_open_orders_table.innerHTML = '';
        for (var key in last_open_orders) {
            var values = `<tr >
            <td> `+ last_open_orders[key].orderId + `</td>
            <td>`+ last_open_orders[key].symbol + `</td>
            <td> `+ last_open_orders[key].side + `</td>
            <td>`+ last_open_orders[key].type + `</td>
            <td> `+ last_open_orders[key].price + `</td>
            <td>`+ last_open_orders[key].origQty + `</td>
            <td> `+ last_open_orders[key].executedQty + `</td>
            <td>`+ last_open_orders[key].stopPrice + `</td>
            <td>`+ last_open_orders[key].fee + `%</td>
            <td>`+ get_cancel_button_for_open_orders(last_open_orders[key]) + `</td>
            </tr>`
            user_open_orders_table.innerHTML += values;
        }
    } else {
        user_open_orders_table.innerHTML = '';
    }
}

update_user_limit_order_side(user_Limit_order_side);
set_user_limit_order_side_button_listeners();

var user_login_check_interval = setInterval(check_user_login_status, 1000);
var ui_update_interval = setInterval(update_UI, 2000);