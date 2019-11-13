'''
This script takes one 'npy' file that contains market data 
of multiple markets and produces 3 files "train.npy", "test.npy", "val.npy".
The script calculates the mean image of the dataset and substracts it from 
each image. 
'''

import numpy as np

def save_file(dir, data):
    np.save(dir, data)
    print(f"saved file '{dir}' file length={len(data)}")

_FILE = "data/private/cnn_data.npy"

_FILE = np.load(_FILE, allow_pickle=True)

mean_img = np.mean(_FILE, axis=0)[0]
print(f"Total data length is '{len(_FILE)}', and 'mean img' is '{mean_img}'")

for i in range(len(_FILE)):
    _FILE[i][0] -= mean_img


'''
    split data for train, test and validation sets
'''

train_size, test_size = int((90/100)*len(_FILE)), int((5/100)*len(_FILE)) # 90%, 5%
train, test, val = _FILE[:train_size], _FILE[train_size:train_size+test_size], _FILE[train_size+test_size:]

save_file("data/private/train.npy",train)
save_file("data/private/test.npy", test)
save_file("data/private/val.npy", val)

# print(train)