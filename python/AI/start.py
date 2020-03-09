import time
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import tensorflow as tf
import json
from percentDiff.percent_cnn import PCNNResNet50
# import logging
# logging.basicConfig
# logger = logging.getLogger(__name__)

models = {
            "PCNNResNet50" : [PCNNResNet50, "percentDiff/model_weights.h5"]    
        }

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
            print(str(e.with_traceback(None)))
            return {"message": str(e)}, 400
    return inner

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
            model = models[model_name][0]()
            # logger.debug(model)
            resnet = model.get_resnet_50(weights=models[model_name][1])
            # model.init_model()
            preds = model.predict(resnet, data)
            return {"status":1,
                    "preds": preds}, 201

class GetAvailableModels(Resource):
    @wrap_with_try
    def get(self):
        return {"models": list(models.keys())}

api.add_resource(GetNNBatchPred, '/getnnbatchpred')
api.add_resource(GetAvailableModels, '/getmodels')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

