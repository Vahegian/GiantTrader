from workers.master import Master
import time
from flask import Flask
from flask_restful import Resource, Api, reqparse

master = None

app = Flask(__name__)
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
            return {"message":"user logged in"}, 201

class GetUwallet(Resource):
    '''
        'post' logged in user name to get user's wallet info.
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
        if not uname or not pair or not amount or not price:
            return {"message":"add user name, pair, amount and price "}, 400
        else:
            master.buy_lim_user(uname,pair,amount,price)
            return {"message": f"Buy order for {pair} is placed"}, 201

class SellLimit(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        amount = args['amount']
        price = args['price']
        if not uname or not pair or not amount or not price:
            return {"message":"add user name, pair, amount and price "}, 400
        else:
            master.sell_lim_user(uname,pair,amount,price)
            return {"message": f"Sell order for {pair} is placed"}, 201

class CancelOrder(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        uname = args['uname']
        pair = args['pair']
        orderid = args['orderId']
        
        if not uname or not pair or not orderid:
            return {"message":"add user name, pair and orderid "}, 400
        else:
            master.cencel_user_order(uname, pair, orderid)
            return {"message": f"Cancelled order for {pair}"}, 201

api.add_resource(LogUser, '/inuser')
api.add_resource(GetUwallet, '/ud/wallet')
api.add_resource(GetUOpenOrders, '/ud/oorders')
api.add_resource(AddUser, '/au/new')
api.add_resource(GetLprices, '/lastprices')
api.add_resource(GetOHLCV, '/ohlcv')
api.add_resource(BuyLimit, '/lbuy')
api.add_resource(SellLimit, '/lsell')
api.add_resource(CancelOrder, '/ocancel')


if __name__ == "__main__":
    with open("./private/private.csv") as pfile:
        data = (pfile.readline()).split(",")
    
    master = Master(data[0], data[1])
    app.run(debug=True, port=5000, host='0.0.0.0')
