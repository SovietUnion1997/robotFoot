# -*- coding: UTF-8 -*-
import time

from naoqi import ALProxy

Name0 = ['we','man','ching']
Name1 = []

IP = "169.254.50.227"  # Replace here with your NaoQi's IP address.
PORT = 9559

tts = ALProxy("ALTextToSpeech", IP, 9559)
# tts.setLanguage('English')
tts.say("Hello")

## 测试代码
## 试试摄像头能不能运行
def testImage(IP,PORT):
  import vision_definitions
  import cv2
  camProxy = ALProxy("ALVideoDevice",IP,PORT)
  resolution = vision_definitions.kQVGA
  colorSpace = vision_definitions.kRGBColorSpace
  fps = 5
  nameId = camProxy.subscribeCamera("test",1,resolution,colorSpace,fps)
  naoimg = camProxy.getImageLocal(nameId)
  camProxy.releaseImage(nameId)
  imgWidth = naoimg[0]
  imgHeight = naoimg[1]
  array = naoimg[6]
  ## 这里需要从array创建图像
  camProxy.unsubscribe("test")

# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

while raw_input('是否进入学习模式y/n:') == 'y':
    print('正在进行学习...')
    tts.say('start learning')
    tts.say('please, input the name')
   # name = raw_input('input the name:').decode('gbk').encode('utf-8')
  #  name = input('input the name:').decode('utf-8').encode('utf-8')
    name = raw_input('input the name:')
    for i in range(10):
        time.sleep(0.05)
        faceProxy.learnFace(name)
    tts.say('learning is OK')
    
# ALMemory variable where the ALFacedetection modules
# outputs its results
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 1000
faceProxy.subscribe("Test_Face", period, 0.0 )


# A simple loop that reads the memValue and checks whether faces are detected.

while len(Name1)<3:
  time.sleep(1)
  val = memoryProxy.getData(memValue)

  print ""
  print "recgonizing......"
  print ""

  # Check whether we got a valid output.
  if(val and isinstance(val, list) and len(val) >= 2):

    # We detected faces !
    # For each face, we can read its shape info and ID.

    # First Field = TimeStamp.
    timeStamp = val[0]

    # Second Field = array of face_Info's.
    faceInfoArray = val[1]

    try:
      # Browse the faceInfoArray to get info on each detected face.
      for j in range( len(faceInfoArray)-1 ):
        faceInfo = faceInfoArray[j]

        # First Field = Shape info.
        faceShapeInfo = faceInfo[0]

        # Second Field = Extra info (empty for now).
        faceExtraInfo = faceInfo[1]
        if faceExtraInfo[2]:
            print '是'
            print faceExtraInfo[2]
            if faceExtraInfo[2] in Name0:
                tts.say(faceExtraInfo[2])
                tts.say('success')
                Name1.append(faceExtraInfo[2])
                Name0.remove(faceExtraInfo[2])
            # tts.say(faceExtraInfo[2])
        else:
            print 'fuck'
            s = 'who are you'
            tts.say(s)
        
    except Exception, e:
      print "faces detected, but it seems getData is invalid. ALValue ="
      print val
      print "Error msg %s" % (str(e))
  else:
    print "No face detected"
    s = 'no face'
    tts.say(s)

tts.say('over')
tts.say('h h h h h h h')
# Unsubscribe the module.
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."

