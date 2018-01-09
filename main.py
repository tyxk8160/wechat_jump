#!/usr/bin/python
import time
import os
import cv2
import pylab as plt
import numpy as np
import glob


def jump(dst):
    alpha = 1.35
    times = int(1.35*dst)
    x =300 + np.random.randint(0,300)

    os.system("adb shell input swipe %d %d %d %d %d" %(x,x,x,x,times))
    print("dst=%d;times=%d"%(dst,times))
class DataFromFile(object):
    def __init__(self,path):
        self.x = glob.glob(path)
        self.index = 0

    def GetImage(self):
        img = cv2.imread(self.x[self.index])
        self.index+=1
        return img


class Data(object):
    '''
    get image
    '''
    def __init__(self,index = 0):
        self.index = index
    def GetImage(self):
        os.system("adb shell screencap -p /sdcard/autojump.png")
        os.system("adb pull /sdcard/autojump.png debug/IMAGE_%d.png" %self.index)
        img = cv2.imread("debug/IMAGE_%d.png" %self.index)
        self.index+=1
        return img

class ImageProcess(object):
    def __init__(self,chess,low,height):
        self.chess = chess
        self.low = low
        self.height = height
        
        self.H,self.W,_ = chess.shape 
    
    def GetInfo(self,image):
        # gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(image,50,150)
        max_loc=self._matchchess(image)
        P1 = (max_loc[0] + self.W//2,max_loc[1] +self.H)
        P2 = self._match(edges,max_loc)
        D = (P1[0]-P2[0])**2+(P1[1]-P2[1])**2
        dst = np.sqrt(D)
        return P1,P2,dst,edges
    def _match(self,edges,max_loc):
        max_d = -1
        x0,y0 = max_loc
        x1,y1 = (max_loc[0] + self.W,max_loc[1]+self.H)
        edges[y0:y1,x0:x1] = 0
        for y in range(self.low,self.height):
            x = np.nonzero(edges[y,:])
            if not np.any(x):
                continue
            d =  np.max(x)-np.min(x)
            print("d = %d" % d)
            if d > max_d:
                max_d = d
                x_mean =  (np.max(x)+np.min(x))//2
                y = y 
               
            else:
                # 
              
                break
        return x_mean,y
            
    def _matchchess(self,image):
        method = cv2.TM_CCOEFF_NORMED
        res = cv2.matchTemplate(image,self.chess,method)
        _,_,_,max_loc = cv2.minMaxLoc(res)
        return max_loc



def main():
    chess = cv2.imread("chess.png")
    dat = Data()
    # dat =DataFromFile("debug\\*.png")
    imp = ImageProcess(chess,600,1200)
    cnt = 0
    while True:
        image = dat.GetImage()
        # plt.imshow(image);plt.show()
        P1,P2,dst,edges = imp.GetInfo(image)
        # plt.imshow(edges,cmap = "gray");plt.show()
        cv2.circle(image,P1,5,(255,0,0),4)
        cv2.circle(image,P2,5,(255,0,0),5)
        cv2.imwrite("detect\\dect_%d.png" % cnt,image)
        cnt+=1

        # plt.imshow(image);plt.show()
        # jump(dst)
        # time.sleep(2)
        if cv2.waitKey(20) >=0:
            break


if __name__ == '__main__':
    main()
        


