import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from use_DNN9_T512_B2 import USE_DNN9_T512_B2
import tensorflow as tf
import json

models = {"DNN9-T512-B2-D1-Q120": USE_DNN9_T512_B2}

app = Flask(__name__)
api = Api(app)
CORS(app) # every body can send request

parser = reqparse.RequestParser()
parser.add_argument('data')
parser.add_argument('state')
parser.add_argument('model')

def wrap_with_try(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return {"message": str(e)}, 400
    return inner

class GetNNPred(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        print(data, type(data), len(data))
        if not data:
            return {"message":"add 'data'"}, 400
        else:
            model = USE_DNN9_T512_B2()
            model.init_model()
            pred = model.get_model_pred(data)
            return {"status":1,
                    "side":pred[0],
                    "conf": str(pred[1])}, 201

class GetNNBatchPred(Resource):
    @wrap_with_try
    def post(self):
        args = parser.parse_args()
        data = args['data']
        model_name = args['model']
        # print(data, len(data))
        if not data or not model_name:
            return {"message":"add 'data' and 'model'"}, 400
        else:
            data = json.loads(data)
            model = models[model_name]()
            model.init_model()
            preds = model.predict(data)
            return {"status":1,
                    "preds": preds}, 201

class GetAvailableModels(Resource):
    @wrap_with_try
    def get(self):
        return {"models": list(models.keys())}

api.add_resource(GetNNPred, '/getnnpred')
api.add_resource(GetNNBatchPred, '/getnnbatchpred')
api.add_resource(GetAvailableModels, '/getmodels')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

