import numpy as np
from keras.callbacks import TensorBoard, ModelCheckpoint
import sys
# sys.path.append("../../../../../")
from models import DNN9_T512_B2_D60r1

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
    
_TRAIN_FILE = "data/private/model_data/DNN9_T512_B2_D60r1/train.npy"
_VAL_FILE = "data/private/model_data/DNN9_T512_B2_D60r1/val.npy"

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


model, EPOCHS = DNN9_T512_B2_D60r1(train=True)
# show_val_stats = ShowValStats("data/private/model_data/DNN_T512_B2/train_hist.npy")

for _ in range(15):
    checkpoint = ModelCheckpoint("data/private/model_data/DNN9_T512_B2_D60r1/weights/"+str(_)+"-e{epoch:02d}-a{acc:.3f}-l{loss:.3f}-va{val_acc:.3f}-vl{val_loss:.3f}.hdf5",
                                monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    
    my_callbacks = [checkpoint]

    if len(sys.argv)>1:
        if sys.argv[1]=="gui": 
            from callbacks import ShowValStats
            show_val_stats = ShowValStats("data/private/model_data/DNN9_T512_B2_D60r1/train_hist.npy")
            my_callbacks = [show_val_stats, checkpoint]
        

    history = model.fit(train_x, train_y, epochs=EPOCHS, verbose=1, validation_data=(val_x, val_y), 
                        callbacks=my_callbacks, batch_size=1024)

