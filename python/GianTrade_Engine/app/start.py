from workers.master import Master
import time
from flask import Flask
from flask_restful import Resource, Api, reqparse

master = None

app = Flask(__name__, static_url_path='', 
            static_folder='web')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('uname')
parser.add_argument('upass')
parser.add_argument('apiKey')
parser.add_argument('apiSecret')
parser.add_argument('pair')
parser.add_argument('days')
parser.add_argument('amount')
parser.add_argument('price')
parser.add_argument('orderId')
parser.add_argument('fee')
parser.add_argument('strategy_name')
parser.add_argument('strategy_option')


def wrap_with_try(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 400
    return inner

class LogUser(Resource):
    '''
        'post' to log in a user, 'get' to see all logged in users 
    '''
    @wrap_with_try
    def get(self):
        return {"users": f'{master.get_all_users()}'}
    
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        upass = args['upass']
        if not uname or not upass:
            return {"message":"add user name and password"}, 400
        else:
            udata = master.get_user_data(uname, upass)
            print(udata)
            master.open_user_account(udata[1], udata[3], udata[4])
            return {"message":"user logged in",
                    "status":1,
                    "uname":uname}, 201

class GetUwallet(Resource):
    '''
        'post' logged in "user name" to get user's wallet info.
    '''
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        if not uname:
            return {"message":"add user name"}, 400
        else:
            return master.get_user_wallet(uname), 201

class GetUOpenOrders(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        if not uname:
            return {"message":"add user name and password"}, 400
        else:
            return master.get_user_open_orders(uname), 201

class AddUser(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        upass = args['upass']
        apikey = args['apiKey']
        apiSecret = args['apiSecret']
        if not uname or not upass or not apikey or not apiSecret:
            return {"message":"add user name, password, apiKey and apiSecret"}, 400
        else:
            master.add_user(uname,upass,apikey, apiSecret)
            return {"message":f"user {uname} added"}, 201

class GetLprices(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        if not uname:
            return {"message":"add user name "}, 400
        else:
            return master.get_user_last_prices(uname), 201

class GetOHLCV(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        days = int(args['days'])
        if not uname or not pair:
            return {"message":"add user name and pair "}, 400
        elif days:
            return master.get_user_ohlcv(uname, pair, days), 201
        else:
            return master.get_user_ohlcv(uname, pair), 201

class BuyLimit(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        amount = args['amount']
        price = args['price']
        fee = args['fee']

        if not uname or not pair or not amount or not price:
            return {"message":"add user name, pair, amount, fee and price "}, 400
        else:
            master.buy_lim_user(uname,pair,float(amount),float(price), fee)
            return {"message": f"Buy order for {pair} is placed", 
                    "status":1}, 201

class SellLimit(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        amount = args['amount']
        price = args['price']
        fee = args['fee']
        if not uname or not pair or not amount or not price:
            return {"message":"add user name, pair, amount, fee and price "}, 400
        else:
            master.sell_lim_user(uname,pair,float(amount),float(price), fee)
            return {"message": f"Sell order for {pair} is placed", 
                    "status":1}, 201

class CancelOrder(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        orderid = args['orderId']
        amount = args['amount']
        price = args['price']
        fee = args['fee']

        if not uname or not pair or not orderid or not amount or not price:
            return {"message":"add user name, pair, amount, price, fee and orderid "}, 400
        else:
            master.cancel_user_order(uname, pair, orderid, amount, price, fee)
            return {"message": f"Cancelled order for {pair}", 
                    "status":1,
                    "orderID":orderid}, 201

class GetPairFees(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        
        if not uname or not pair:
            return {"message":"add user name, pair and orderid "}, 400
        else:
            return master.get_user_pair_fee(uname, pair), 201

class Strategies(Resource):
    @wrap_with_try
    def get(self):
        return master.get_all_strategies(), 201

    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        s_name = args['strategy_name']
        s_option = args['strategy_option']
        
        if not uname or not pair or not s_name or not s_option:
            return {"message" : "add 'uname', 'pair', 'strategy_option' and 'strategy_name'"}, 400
        else:
            if s_option == "start":
                if master.start_strategy(s_name, uname, pair):
                    return {"message" : f"strategy with id {s_name} started", "status":1}, 201
            elif s_option == "stop":
                if master.stop_strategy(s_name, uname, pair):
                    return {"message" : f"strategy with id {s_name} stopped", "status":1}, 201
            elif s_option == "log":
                return master.get_strategy_log(s_name, uname, pair), 201
            elif s_option == "running":
                return master.get_running_strategies(uname), 201
            else:
                return {"message" : f"s_option '{s_option}' is not available", "status":0}, 400

api.add_resource(LogUser, '/inuser')
api.add_resource(GetUwallet, '/ud/wallet')
api.add_resource(GetUOpenOrders, '/ud/oorders')
api.add_resource(AddUser, '/au/new')
api.add_resource(GetLprices, '/lastprices')
api.add_resource(GetOHLCV, '/ohlcv')
api.add_resource(BuyLimit, '/lbuy')
api.add_resource(SellLimit, '/lsell')
api.add_resource(CancelOrder, '/ocancel')
api.add_resource(GetPairFees, '/pairfee')
api.add_resource(Strategies, '/strategies')


if __name__ == "__main__":
    with open("./private/private.csv") as pfile:
        data = (pfile.readline()).split(",")
    
    master = Master(data[0], data[1])
    app.run(debug=True, port=5000, host='0.0.0.0')
