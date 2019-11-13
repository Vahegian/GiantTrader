'''
This script takes one 'npy' file that contains market data 
of multiple markets and produces a file.
These file contains 4x7 images of the markets (each image holds 7 days of OHLC data)
and buy or sell signals associated with the images. 
'''

import numpy as np

# market_data_file = str(input("please specify relative path to the markets file '.npy' > \n"))
coins_data_file = "data/private/coins.npy"
market_data_file = "data/private/markets.npy"

coins_data_file = np.load(coins_data_file, allow_pickle=True)
market_data_file = np.load(market_data_file, allow_pickle=True)

data = np.vstack((coins_data_file, market_data_file))

# randomly shuffle tha data 
print(data[0][0])
np.random.shuffle(data)
print(data[0][0])
# if len(market_data_file) > 0 :
#     try:
#         data = np.load(market_data_file, allow_pickle=True)
#     except Exception as e:
#         print("e")
#         exit(1)

'''
    Removes All Not A Number rows
'''
print("Starting cleaning")

for market_data in data:
    print(f"Cleaning {market_data[0]}")
    market_data[1].dropna(inplace=True)

# print("train", train[0][0], len(train))
# print("test", test[0][0], len(test))
# print("val", val[0][0], len(val))

import os
from time import sleep
from multiprocessing import Process

def num_map(x, in_min, in_max, out_min=0, out_max=1):
    if in_max == in_min:
        return 0
    y = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if y<0:
        return 0
    return y

# all_new_data = np.array()

def get_OHLC_bin_images(data, file_to_save, days=7, dec_days=3): # des_days - decision days to determine if price is up or down
    ohlc_bin_imgs = []
    for market_data in data:
        market_name = market_data[0]
        if market_name=="tether" or market_name=="^N225":
            continue
        print(os.getpid(), f"working on {market_data[0]}")
        market_data = market_data[1] # get dataframe [0] will be tha market name
        low, ope_n, close, high = market_data["Low"], market_data["Open"], market_data["Close"], market_data["High"] # OHLC datasets
        for i in range(len(low)):
            max_of_the_market = market_data["High"][i:i+days].max() # get max value of the given range
            min_of_the_market = market_data["Low"][i:i+days].min() # get min value of the given range
            image = np.zeros((4,days)) # tamplate image
            save_img = False
            try:
                if i+days+dec_days < len(low): 
                    for x in range(image.shape[1]): # iterate through 'x axis' of the image 
                        image[0][x] = num_map(high[i+x], min_of_the_market, max_of_the_market) # convert market value to be between 0 and 1
                        image[1][x] = num_map(close[i+x], min_of_the_market, max_of_the_market) # [0] - top row of image, [3] bottom row of image.
                        image[2][x] = num_map(ope_n[i+x], min_of_the_market, max_of_the_market)
                        image[3][x] = num_map(low[i+x], min_of_the_market, max_of_the_market)
                        save_img = True
                    
                    pre = np.average(close[(i+days)-dec_days:i+days])
                    post = np.average(close[i+days:i+days+dec_days])
                    
                    decision = np.array([0]) # [1]-buy, [0]-sell                    
                    if pre < post:
                        decision[0]=1
                        
                    if save_img:
                        ohlc_bin_imgs.append(np.array([image, decision]))
                else:
                    break
            except Exception as e:
                print(str(e), market_name)
                
    np.save(file_to_save, np.array(ohlc_bin_imgs))
    print(os.getpid(), f"saved file '{file_to_save}' file length={len(ohlc_bin_imgs)}")


# # create 3 processes to prepare data in parallel to save time. 
# p1 = Process(target=get_OHLC_bin_images, args=(train, "data/private/train.npy"))
# p2 = Process(target=get_OHLC_bin_images, args=(test, "data/private/test.npy"))
# p3 = Process(target=get_OHLC_bin_images, args=(val, "data/private/val.npy"))
  
# p1.start()
# p2.start()
# p3.start()
# p1.join()
# p2.join()
# p3.join()        
get_OHLC_bin_images(data, "data/private/cnn_data.npy")