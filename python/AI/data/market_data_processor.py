import pandas as pd
import os
import numpy as np

BASE_DIR = "data/private/markets"
cur_dir = os.listdir(BASE_DIR)
print(cur_dir)
all_data = []
for mfile in cur_dir:
    data = pd.read_csv(BASE_DIR+"/"+mfile)
    name = mfile.split('.')
    all_data.append([name[0], data])

all_data = np.array(all_data)
np.save("data/private/markets.npy", all_data)
print(all_data)