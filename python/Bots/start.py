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
parser.add_argument('id')
parser.add_argument('uname')


def wrap_with_try(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e.with_traceback()))
            return {"message": str(e), "status":0}, 400
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
        bot_id = args['id']
        uname = args['uname']
        print(pair,bot,action,bot_id,uname)
        if not action:
            return {"message": "Please provide 'pair', 'bot', and 'action'"}, 400
        else:
            if action == "start":
                new_id = master.start_bot(pair, bot, uname)
                if new_id:
                    return {"status": 1, "id":new_id}, 201
            elif action == "stop":
                if master.stop_bot(bot_id):
                    return {"status": 1}, 201
            elif action == "log":
                info = master.get_running_bot_info(bot_id)
                if info:
                    return {"status":1,"log":info}, 201
            # return {"message": "operation start/stop bot failed!"}, 400
            else:
                raise Exception("Start_Stop_Log_Bot failed!")


api.add_resource(GetAvailableBots, '/getavalbots')
api.add_resource(GetRunningBots, '/getrunningbots')
api.add_resource(Start_Stop_Log_Bot, '/start_stop_log_bot')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

