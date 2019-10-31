from workers.master import Master
import time
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
api.add_resource(HelloWorld, '/')


if __name__ == "__main__":
    # with open("./private/private.csv") as pfile:
    #     data = (pfile.readline()).split(",")
    # m = Master(data[0], data[1])

    # udata = m.get_user_data("vahe2nd", "vahe2nd")
    # print(udata)
    # m.open_user_account(udata[1], udata[3], udata[4])
    # print(m.get_user_wallet(udata[1]))
    # print(m.get_user_open_orders(udata[1]))
    # print(m.get_user_ohlcv(udata[1], "XRPUSDT"))
    # time.sleep(5)
    # print(m.get_user_last_prices(udata[1]))   

    app.run(debug=True, port=5000, host='0.0.0.0')
