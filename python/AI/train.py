from percentDiff.percent_cnn import PCNNResNet50

if __name__ == "__main__":
    # import random
    # data = ["{"+f"\"open\":\"{x*random.random()}\",\"high\":\"{x*random.random()}\",\"low\":\"{x/random.random()}\",\"close\":\"{x*random.random()}\""+"}" for x in range(1,32)]
    # print(data,len(data))
    filepath="percentDiff/model_weights.h5"
    pdnn = PCNNResNet50()
    model = pdnn.get_resnet_50(weights=filepath)
    pdnn.train(model, weights_out=filepath, gui=True)
    # print(create_data(9,10,14,20))
    # preds = pdnn.predict_batch(data)
    # print(preds, len(preds))