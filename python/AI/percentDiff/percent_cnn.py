import numpy as np
from keras.callbacks import ModelCheckpoint
import cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, Input, Activation
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.models import Sequential, Model
from keras import backend as K
from percentDiff.percent_data_maker import create_data, NUM_OF_DATAPOINTS
import json
# import logging


class PCNNResNet50:
    def __init__(self, weighst_in: str=None, *args, **kwargs):
        self.__model = None
        self.__EPOCHS = 5000
        # self.get_resnet_50(weights=weighst_in)
        self.__img_dim = (197,197)
        # self.__logger = logging.getLogger(__name__)
    
    def get_resnet_50(self, input_shape :tuple=(197,197,3), out_classes :int=3, weights :str=None):
        if self.__model == None:
            K.clear_session()
            print("\nInitializing The Model\n")
            LR = 0.00001
            # DECAY = LR/EPOCHS
            FC_LAYERS = [512, 512, 512]
            dropout = 0.5

            base_model = ResNet50(weights='imagenet', 
                            include_top=False, 
                            input_shape=input_shape)

            for layer in base_model.layers:
                layer.trainable = False

            x = base_model.output
            x = Flatten()(x)
            for fc in FC_LAYERS:
                # New FC layer, random init
                x = Dense(fc, activation='relu')(x) 
                x = Dropout(dropout)(x)

            # New softmax layer
            predictions = Dense(out_classes, activation='softmax')(x) 
            
            finetune_model = Model(inputs=base_model.input, outputs=predictions)

            optimizer = Adam(lr=LR)
            finetune_model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            print(finetune_model.summary())
            if weights != None:
                print(f"loading weights from {weights}")
                finetune_model.load_weights(weights)
            self.__model = finetune_model

        return self.__model

    
    def train(self, model, weights_out: str=None, gui: bool=False):
        train_datagen =  ImageDataGenerator(
        preprocessing_function=preprocess_input
        )

        train_generator = train_datagen.flow_from_directory("percentDiff/img_data", 
                                                        target_size=self.__img_dim, 
                                                        batch_size=16)
        print(f"\n prediciton indices: {train_generator.class_indices}, {train_generator.class_mode}, {train_generator.batch_index}\n")
        num_train_images = 1024

        checkpoint = ModelCheckpoint(weights_out, monitor=["acc"], verbose=1, mode='max')
        callbacks_list = [checkpoint]
        if gui:
            from callbacks import ShowValStats
            svs = ShowValStats("hist.npy")
            callbacks_list = [checkpoint, svs]

        history = model.fit_generator(train_generator, epochs=self.__EPOCHS, workers=8, 
                                        steps_per_epoch=num_train_images, #BATCH_SIZE, 
                                        shuffle=True, callbacks=callbacks_list)
    
    def predict(self, model, percent_data:list):
        # print(percent_data)
        predictions = []
        img  = []
        for item in percent_data:
            # item = json.loads(item)
            img.append(create_data(float(item["open"]), float(item["high"]), float(item["low"]), float(item["close"])))
            if len(img) == NUM_OF_DATAPOINTS:
                img_to_pred = np.array(img, dtype="float32")
                img_to_pred = cv2.resize(img_to_pred, self.__img_dim)
                # cv2.imshow("win", img_to_pred)
                # cv2.waitKey(100)
                img_to_pred = np.reshape(img_to_pred, (1, 197,197,3))
                # self.__logger.debug(f">>>>>>>>>>>>>>> {self.__model}")
                predictions.append(model.predict(img_to_pred).tolist()[0])
                img.pop(0)
            else:
                predictions.append([0,0,0])
        # print(predictions)
        return predictions
            


if __name__ == "__main__":
    # import random
    # data = ["{"+f"\"open\":\"{x*random.random()}\",\"high\":\"{x*random.random()}\",\"low\":\"{x/random.random()}\",\"close\":\"{x*random.random()}\""+"}" for x in range(1,32)]
    # print(data,len(data))
    filepath="percentDiff/model_weights.h5"
    pdnn = PCNNResNet50(filepath)
    pdnn.train(filepath, gui=True)
    # print(create_data(9,10,14,20))
    # preds = pdnn.predict_batch(data)
    # print(preds, len(preds))