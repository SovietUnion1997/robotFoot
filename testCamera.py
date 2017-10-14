# -*- coding: UTF-8 -*-
import time
import vision_definitions
import cv2
from naoqi import ALProxy
import numpy as np

IP = "169.254.50.227"  # Replace here with your NaoQi's IP address.
PORT = 9559
## 测试代码
## 试试摄像头能不能运行

camProxy = ALProxy("ALVideoDevice",IP,PORT)
resolution = vision_definitions.kQVGA
colorSpace = vision_definitions.kRGBColorSpace
fps = 5
nameId = camProxy.subscribeCamera("test",1,resolution,colorSpace,fps)
# naoimg = camProxy.getImageLocal(nameId)
naoimg = camProxy.getImageRemote(nameId)
imgWidth = naoimg[1]
imgHeight = naoimg[0]
array = naoimg[6]
cv2.namedWindow('face')
while 1:
    image = np.fromstring(array,np.uint8).reshape(imgWidth,imgHeight,3)
    image2 = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    cv2.imshow('face',image2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    naoimg = camProxy.getImageRemote(nameId)
    array = naoimg[6]
    
## 这里需要从array创建图像
# camProxy.releaseImage(nameId)
camProxy.unsubscribe("test")

