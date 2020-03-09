import cv2
import numpy as np
import os


NUM_OF_DATAPOINTS = 30

def get_percent_diff(var1: float, var2: float):
    return 1.0-(min([var1, var2])/max([var1, var2]))


def get_all_combos(elem_list: list):
    elem_diff_list = []
    for item1_index in range(len(elem_list)):
        for item2_index in range(item1_index, len(elem_list)):
            if item1_index==item2_index:
                continue
            elem_diff_list.append(get_percent_diff(elem_list[item1_index], elem_list[item2_index]))
    return elem_diff_list

def create_data(ope_n, high, low, close):
    # diff_close_prevClose = get_percent_diff(prev_close, close) # diff between previous and current close
    elem_list = get_all_combos([low,ope_n,close,high])
    pixcels = []
    # dim1 = 201 # must be odd number
    # img_one_ohlc = np.zeros((dim1,dim1*6,3), dtype="float32")
    # center_x, center_y = int(((dim1-1)/2)+1), int(((dim1-1)/2)+1)
    for item in elem_list: #BGR
        base_tone = 100-(100*item)
        if close > ope_n:
            # img_one_ohlc = cv2.circle(img_one_ohlc, (center_x, center_y), int(center_y-(center_y*item)), (int(255-(255*item)), 255, 0), -1)  
            pixcels.append([base_tone, 255, base_tone])
        else:
            pixcels.append([base_tone, base_tone, 255])
            # img_one_ohlc = cv2.circle(img_one_ohlc, (center_x, center_y), int(center_y-(center_y*item)), (int(255-(255*item)), 0, 255), -1) 
        # center_x = center_x+dim1

    # max_val_to_add =1.0 - max([x[0] for x in pixcels])

    # for item in pixcels:
    #     item[0]=int((item[0]+max_val_to_add)*255)
    # return img_one_ohlc
    return [pixcels]

def create_images_from_data(data:list, out_folder:str):
    im_id = 0
    for batch in data:
        img = []
        for item in batch: # item = 'ohlc'
            ohlc_img = create_data(item[0],item[1],item[2],item[3])
            for layer in ohlc_img:
                img.append(layer) 
        
        img = cv2.resize(np.array(img, dtype="float32"),(197,197))
        im_id+=1
        # cv2.imshow("win", img)
        # cv2.waitKey(10)
        cv2.imwrite(f"{out_folder}/{im_id}.jpg", img)
        
        if im_id%150==0:
            print(f"saved {im_id}/{len(data)} images to folder {out_folder}")
    print(f"saved {im_id}/{len(data)} images to folder {out_folder}")

if __name__ == "__main__":

    coins_data_file = "private/coins.npy"
    market_data_file = "private/markets.npy"

    coins_data_file = np.load(coins_data_file, allow_pickle=True)
    market_data_file = np.load(market_data_file, allow_pickle=True)

    data = np.vstack((coins_data_file, market_data_file))
    # data = coins_data_file

    # randomly shuffle the data 
    print(f"len: {len(data)}, first before shuffle: {data[0][0]}, content: \n{data[0][1]}")
    np.random.shuffle(data)
    print(f"len: {len(data)}, first after shuffle: {data[0][0]}, content: \n{data[0][1]}")

    '''
        Removes All Not A Number rows
    '''
    print("Starting cleaning")
    skippable_markets = ["tether", "^N225"]
    data_to_use = []
    for market_data in data:
        if market_data[0] in skippable_markets:
            print(f"\t\t\tskipping {market_data[0]}")
            continue
        print(f"Cleaning {market_data[0]}")
        market_data[1].dropna(inplace=True)
        data_to_use.append(market_data)
    data = None # freeing memory 
    print(f"Cleaning completed: new data market qty. {len(data_to_use)}")

    '''
        Balancing
    '''
    side_buy=[]
    side_sell=[]
    side_hodl=[]
    for market in data_to_use:
        print(f"Counting '{market[0]}' to balance")
        low, ope_n, close, high = market[1]["Low"], market[1]["Open"], market[1]["Close"], market[1]["High"]
        data_batch = []
        for index in range(len(low)):
            data_batch.append([ope_n[index], high[index], low[index], close[index]])
            if len(data_batch)==NUM_OF_DATAPOINTS and len(close)>index+1:
                price_at_next_index = close[index+1]
                prev_max_close = max(close[index-3:index])
                
                if price_at_next_index > prev_max_close+(prev_max_close*0.01):
                    side_buy.append(data_batch)
                elif price_at_next_index < prev_max_close-(prev_max_close*0.01):
                    side_sell.append(data_batch)
                else:
                    side_hodl.append(data_batch)
                data_batch.pop(0)
        print(f"\t\t\t\tbuy: {len(side_buy)} hodl: {len(side_hodl)} sell: {len(side_sell)} Total: {len(side_buy)+len(side_hodl)+len(side_sell)}")
   
    min_qty = min(len(side_buy),len(side_hodl),len(side_sell))
   
    print(f"trimming all to minimum quantity of {min_qty}")
   
    np.random.shuffle(side_buy)
    np.random.shuffle(side_hodl)
    np.random.shuffle(side_sell)
    side_buy = side_buy[:min_qty]
    side_hodl = side_hodl[:min_qty]
    side_sell = side_sell[:min_qty]
   
    print(f"datapoints After Trimming -  buy: {len(side_buy)} hodl: {len(side_hodl)} sell: {len(side_sell)} Total: {len(side_buy)+len(side_hodl)+len(side_sell)}")

    '''
        creat all necessary folders 
    '''
    TRAIN_FOLDER = "train"
    VAL_FOLDER = "val"
    
    os.system(f"rm -r {TRAIN_FOLDER}")
    os.system(f"rm -r {VAL_FOLDER}")
    os.system(f"mkdir {TRAIN_FOLDER}")
    os.system(f"mkdir {VAL_FOLDER}")

    BUY_FOLDER = f"{TRAIN_FOLDER}/buy"
    HODL_FOLDER = f"{TRAIN_FOLDER}/hodl"
    SELL_FOLDER = f"{TRAIN_FOLDER}/sell"
    BUY_FOLDER_VAL = f"{VAL_FOLDER}/buy"
    HODL_FOLDER_VAL = f"{VAL_FOLDER}/hodl"
    SELL_FOLDER_VAL = f"{VAL_FOLDER}/sell"
    
    os.system(f"mkdir {BUY_FOLDER}")
    os.system(f"mkdir {HODL_FOLDER}")
    os.system(f"mkdir {SELL_FOLDER}")
    os.system(f"mkdir {BUY_FOLDER_VAL}")
    os.system(f"mkdir {HODL_FOLDER_VAL}")
    os.system(f"mkdir {SELL_FOLDER_VAL}")
    
    '''
        create images using multiple threads per folder
    '''
    import threading
    def process(data, folder, workers=5):
        itt_qty = int(len(data)/workers)
        for i in range(workers):
            threading.Thread(target=create_images_from_data, args=(data[itt_qty*i:itt_qty*(i+1)], folder)).start()

    train_len = int((len(side_buy)*0.8)+0.5)
    process(side_buy[:train_len], BUY_FOLDER)
    process(side_hodl[:train_len], HODL_FOLDER)
    process(side_sell[:train_len], SELL_FOLDER)

    process(side_buy[train_len:], BUY_FOLDER_VAL)
    process(side_hodl[train_len:], HODL_FOLDER_VAL)
    process(side_sell[train_len:], SELL_FOLDER_VAL)
    
    # create_images_from_data(side_buy, BUY_FOLDER, BUY_FOLDER_VAL)