import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")
import cv2
from keras.callbacks import Callback
import numpy as np

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