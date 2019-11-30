import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, Input
from keras.layers.normalization import BatchNormalization
from keras.callbacks import TensorBoard, ModelCheckpoint, Callback
from keras.optimizers import Adam
from keras.utils import to_categorical
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")
import cv2

class ShowValStats(Callback):
    def __init__(self, hist_dir=None):
        super().__init__()
        self.__hdir = hist_dir
            
    def on_train_begin(self, logs={}):
        if self.__hdir==None:
            print("No previous history is found.")
        else:
            try:
                hfile = np.load(self.__hdir, allow_pickle=True)
                self.acc = list(hfile[0])
                self.loss = list(hfile[1])
                self.vacc = list(hfile[2])
                self.vloss = list(hfile[3])
            except:
                self.acc = []
                self.loss = []
                self.vacc = []
                self.vloss = []

    def on_epoch_end(self, batch, logs={}):
        self.vacc.append(logs.get('val_acc'))
        self.vloss.append(logs.get('val_loss'))
        self.acc.append(logs.get('acc'))
        self.loss.append(logs.get('loss'))
        fig = plt.figure()    
        plt.plot(self.acc)
        plt.plot(self.vacc)
        plt.plot(self.loss)
        plt.plot(self.vloss)
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['acc', 'val_acc', 'loss', 'val_loss'], loc='upper left')
        
        fig.canvas.draw()
        convas = fig.canvas.renderer.buffer_rgba()
        img = np.array(convas)
        cv2.imshow("model stats", img)
        cv2.waitKey(1000)
        plt.close(fig=fig)
        if self.__hdir !=None:
            np.save(self.__hdir, np.array([self.acc, self.loss, self.vacc, self.vloss]))

show_val_stats = ShowValStats("data/private/train_hist.npy")

def balance_data(data):
    # balance data
    print(f"file size before balancing '{len(data)}'")
    buy_list = []
    sell_list = []
    for item in data:
        if item[1][0] == 0:
            sell_list.append(item)
        elif item[1][0] == 1:
            buy_list.append(item)
    min_amount = np.min([len(sell_list), len(buy_list)])
    print(f"class qty. Buy '{len(buy_list)}' :: Sell '{len(sell_list)}' :: min={min_amount}")
    data = np.vstack((np.array(buy_list[:min_amount]), np.array(sell_list[:min_amount])))
    print(f"file size after balancing '{len(data)}'")
    # shuffle data
    print("first img before shuffle \n",data[0])
    np.random.shuffle(data)
    print("first img after shuffle \n",data[0])
    return data
    
_TRAIN_FILE = "data/private/train.npy"
_VAL_FILE = "data/private/val.npy"

_TRAIN_FILE = np.load(_TRAIN_FILE, allow_pickle=True)
_VAL_FILE = np.load(_VAL_FILE, allow_pickle=True)
# print(_TRAIN_FILE)
# exit(0)

_TRAIN_FILE = balance_data(_TRAIN_FILE)

train_x, train_y = _TRAIN_FILE[:, 0] ,_TRAIN_FILE[:, 1]
# print(train_x[0][0][0], train_x.shape)
# exit(0)
train_x = np.array([np.reshape(img, (len(img[0][0])*4)) for img in train_x])
train_y = np.array([label for label in train_y])
print(f"x- l:{len(train_x)}, d:{train_x[0]}, y- l:{len(train_y)}, d:{train_y[0]}")
# exit(0)
assert len(train_x)==len(train_y)
val_x, val_y = _VAL_FILE[:, 0], _VAL_FILE[:, 1]
val_x = np.array([np.reshape(img, (len(img[0][0])*4)) for img in val_x])
print("\nBEFORE \n",val_y)
val_y = np.array([label for label in val_y])
assert len(val_x)==len(val_y)
print("\nAFTER \n",val_y)

def my_model():
    model = Sequential()
    # model.add(Conv2D(32, kernel_size=(3,3), padding="same", input_shape=(1, 4, 7), activation='relu'))
    # # model.add(Conv2D(64, kernel_size=(3,3), padding="same", activation='relu'))
    # model.add(Flatten())
    model.add(Dense(512, input_dim=len(train_x[0]), activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(32, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(8, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(4, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(2, activation='softmax'))
    return model
    
LR = 1e-5
EPOCHS = 50
DECAY = LR/EPOCHS
# _ = 4

model = my_model()
optimizer = Adam(lr=LR, decay=DECAY)
# optimizer = Adam(lr=LR)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
# print(model.summary())


# tensorboard = TensorBoard(log_dir="data/private/tf_log")
model.load_weights("data/private/weights/11-e07-a0.747-l0.513-va0.750-vl0.510.hdf5")
# history = []
for _ in range(15):
    checkpoint = ModelCheckpoint("data/private/weights/"+str(_)+"-e{epoch:02d}-a{acc:.3f}-l{loss:.3f}-va{val_acc:.3f}-vl{val_loss:.3f}.hdf5",
                                monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    history = model.fit(train_x, train_y, epochs=EPOCHS, verbose=1, validation_data=(val_x, val_y), 
                        callbacks=[checkpoint, show_val_stats], batch_size=256)

