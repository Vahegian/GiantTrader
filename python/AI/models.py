from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout, Input
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.utils import to_categorical

def DNN9_T512_B2(weights=None, train=False):
    LR = 1e-5
    EPOCHS = 50
    DECAY = LR/EPOCHS
    
    model = Sequential()
    model.add(Dense(512, input_dim=120, activation='relu'))
    model.add(BatchNormalization())
    if train:
        model.add(Dropout(0.5))
    model.add(Dense(256, activation='relu'))
    model.add(BatchNormalization())
    if train:
        model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    if train:
        model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(BatchNormalization())
    if train:
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

    optimizer = Adam(lr=LR, decay=DECAY)
    # optimizer = Adam(lr=LR)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    print(model.summary())
    if weights != None:
        model.load_weights(weights)
    return model, EPOCHS