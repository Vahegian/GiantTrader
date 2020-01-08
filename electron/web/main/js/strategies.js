var strategies_log_list = document.getElementById("strategies_log_list");
var strategies_strategy_selector = document.getElementById("strategies_strategy_selector");
var strategies_pair_selector = document.getElementById("strategies_pair_selector");
var strategies_start_button = document.getElementById("strategies_start_button");
var strategies_stop_button = document.getElementById("strategies_stop_button");
var strategies_log_button = document.getElementById("strategies_log_button");
var strategies_running_list = document.getElementById("strategies_running_list");

var update_pairs_for_strategies = true
var update_strategies_selector = true

var user_strategies = null;
var start_stop_button_pressed = false;
var running_strategies = {}

function pop_strategies_selector(data, code) {
    user_strategies = data
    populate_options_object(strategies_strategy_selector, data);
}


function update_strategies() {
    if (logged_in_user_name != null) {
        if (sorted_pairs != null) {
            if (update_pairs_for_strategies) {
                populate_options_object(strategies_pair_selector, sorted_pairs)
                update_pairs_for_strategies = false
            }
        }

        if (update_strategies_selector) {
            get_all_strategies(pop_strategies_selector)
            update_strategies_selector = false
        }
    }
}

function populate_running_list(data, code){
    strategies_running_list.innerHTML = ''
    for (var key in data){
        strategies_running_list.innerHTML+= ` <li class="text-success">${key} : ${data[key]} </li>`
    }
}

function show_running_strategies(data, code){
    if (data["status"] == 1){
        console.log(data);
        get_running_strategies(populate_running_list)
    }
}

function show_strategy_log(data, code){
    strategies_log_list.innerHTML=''
    for (var index in data){
        strategies_log_list.innerHTML+= ` <li class="text-info">${data[index]}</li>`
    }
}

strategies_start_button.addEventListener("click", function(){
    var strategy = strategies_strategy_selector.value;
    var pair = strategies_pair_selector.value;
    start_strategy(show_running_strategies, strategy, pair);
});

strategies_stop_button.addEventListener("click", function(){
    var strategy = strategies_strategy_selector.value;
    var pair = strategies_pair_selector.value;
    stop_strategy(show_running_strategies, strategy, pair);
});

strategies_log_button.addEventListener("click", function(){
    var strategy = strategies_strategy_selector.value;
    var pair = strategies_pair_selector.value;
    get_strategy_log(show_strategy_log, strategy, pair);
});

var strategies_update_interval = setInterval(update_strategies, 2000);