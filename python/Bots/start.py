import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
from master import Master

master = Master()
app = Flask(__name__)
api = Api(app)
CORS(app) # every body can send request

parser = reqparse.RequestParser()
parser.add_argument('bot')
parser.add_argument('pair')
parser.add_argument('action')
parser.add_argument('min_amount')

def wrap_with_try(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 400
    return inner

class GetAvailableBots(Resource):
    @wrap_with_try
    def get(self):
        return master.get_all_bots(), 201

class GetRunningBots(Resource):
    @wrap_with_try
    def get(self):
        return master.get_running_bots(), 201

class Start_Stop_Log_Bot(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        pair = args['pair']
        bot = args['bot']
        action = args['action']
        if not pair or not bot or not action:
            return {"message": "Please provide 'pair', 'bot', and 'action'"}, 400
        else:
            if action == "start":
                if master.start_bot(pair, bot):
                    return {"status": 1}, 201
            elif action == "stop":
                if master.start_bot(pair, bot):
                    return {"status": 1}, 201
            elif action == "log":
                return master.get_running_bot_info(pair, bot), 201
            return {"message": "operation start/stop bot failed!"}, 400


api.add_resource(GetAvailableBots, '/getavalbots')
api.add_resource(GetRunningBots, '/getrunningbots')
api.add_resource(Start_Stop_Log_Bot, '/start_stop_log_bot')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

