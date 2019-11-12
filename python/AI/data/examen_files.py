import numpy as np
import cv2

mfile = "data/private/train1.npy"
mfile = np.load(mfile, allow_pickle=True)
# print(mfile, len(mfile))
counts = [0,0]
for img in mfile:
    if img[1]==0:
        # print("SELL")
        counts[0]+=1
    else:
        counts[1]+=1
        # print("BUY")
        
    # print(img[0])
    # cv2.imshow("win", img[0])
    # cv2.waitKey(1000)
print(counts)