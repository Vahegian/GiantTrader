from models import DNN9_T512_B2
import numpy as np
        
class USE_DNN9_T512_B2:
    def __init__(self):
        self.model = None

    def init_model(self):
        if self.model == None:
            self.model, _ = DNN9_T512_B2("data/private/model_data/DNN_T512_B2/weights/0-e31-a0.755-l0.499-va0.752-vl0.503.hdf5")
        else:
            print("Model is Initialized!")

    def num_map(self, x, in_min, in_max, out_min=0, out_max=1):
        if in_max == in_min:
            return 0
        y = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if y<0:
            return 0
        return y

    def get_model_pred(self, data):
        """
            supply array containing 30 days of data for OHLC
            total length = 120.
            data must be concantinated in HCOL order
        """
        data = [float(d) for d in data]
        d_max = max(data)
        d_min = min(data)
        for index in range(len(data)):
            data[index] = self.num_map(data[index], d_min, d_max)
        data = np.reshape(data, (1,120))
        pred = self.model.predict(data)
        if np.argmax(pred[0]) == 0:
            return "BUY", pred[0][0]
        else:
            return "SELL", pred[0][1]

    def run_test(self):
        test_data = np.load("data/private/model_data/DNN_T512_B2/test.npy", allow_pickle=True)
        correct, wrong, total = 0, 0, 0
        for item in test_data:
            item[0] = np.reshape(item[0], (1, 120))
            # print(item[0].shape, item[1])
            pred = self.model.predict(item[0])
            total+=1
            if np.argmax(pred[0]) == np.argmax(item[1]):
                correct+=1
            else:
                wrong+=1
            print(f"C: {correct} {((correct/total)*100):.3f}%  W: {wrong} {((wrong/total)*100):.3f}%")


if __name__ == "__main__":
    u = USE_DNN9_T512_B2()
    u.init_model()
    u.run_test()
    print(u.get_model_pred(np.random.random_sample((120))))
    print(u.get_model_pred(np.random.random_sample((120))))