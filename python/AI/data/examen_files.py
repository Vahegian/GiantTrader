import numpy as np
import cv2
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")

def show_img(img, t=2000):
    cv2.imshow("win", img)
    cv2.waitKey(t)
    
def show_plot(x, y, c='r'):
    # # scatter the sepal_length against the sepal_width
    fig, ax = plt.subplots()
    ax.scatter(x, y, color=c)
    plt.show(fig)
    
mfile = "data/private/train.npy"
mfile = np.load(mfile, allow_pickle=True)
print(len(mfile))

data_img = []
data_side = []
means = []

for img in mfile:
    # print(img)
    data_img.append(img[0])
    data_side.append(img[1])
    means.append(np.mean(img[0]))

data_img = np.array(data_img)
data_side = np.array(data_side)

fig1, a1 = plt.subplots()
# fig2, a2 = plt.subplots()

# '0 mean' data
imgs_mean = np.mean(data_img)
print("mean before", imgs_mean)
unique_elements, counts_elements = np.unique(data_img, return_counts=True)
a1.scatter(counts_elements, unique_elements, color='r')

# data_img = data_img-imgs_mean
# print("mean after", np.mean(data_img))
# unique_elements, counts_elements = np.unique(data_img, return_counts=True)
# a2.scatter(counts_elements, unique_elements, color='g')

plt.show()

# # 'normalize' data
# img_std= np.std(data_img)
# print("std before", img_std)

# data_img/=np.std(data_img)
# print("std after", np.std(data_img))
# print("mean after std", np.mean(data_img))

# for img in data_img:
#     show_img(img, 1)

