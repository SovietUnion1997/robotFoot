# -*- coding: UTF-8 -*-
import time
import cv2
from naoqi import ALProxy

class Robot(object):
    '''the definition of the robot class'''
    def __init__(self,IP,PORT):
        # Create a proxy to ALFaceDetection
        try:
            self.faceProxy = ALProxy("ALFaceDetection", IP, PORT)
        except Exception, e:
            print "Error when creating face detection proxy:"
            print str(e)
            exit(1)
        # Create a proxy to ALMemory
        try:
            self.memoryProxy = ALProxy("ALMemory", IP, PORT)
        except Exception, e:
            print "Error when creating memory proxy:"
            print str(e)
            exit(1)
        self.tts = ALProxy("ALTextToSpeech", IP, PORT)
        # self.tts.setLanguage('Chinese')
        self.tts.say("你好")
        self.camProxy = ALProxy("ALVideoDevice",IP,PORT)
        # Subscribe to the ALFaceDetection proxy
        # This means that the module will write in ALMemory with
        # the given period below
        period = 1000
        self.faceProxy.subscribe("Test_Face", period, 0.0 )

    def learnFace(self,name):
        #print '请输入姓名:'
        #self.tts.say('请输入你的名字')
        #name = raw_input()
        print('正在进行学习...')
        self.tts.say('正在进行学习...')
        for i in range(10):
            time.sleep(0.05)
            self.faceProxy.learnFace(name)
        # self.tts.say('learning is OK')
        self.tts.say(name)
        self.tts.say('学习成功')

    def recogFace(self):
        memValue = "FaceDetected"
        self.tts.say('正在进行识别')
        val = self.memoryProxy.getData(memValue)
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
                self.tts.say('我检测到了有'+str(len(faceInfoArray)-1)+'张脸')
                for j in range( len(faceInfoArray)-1 ):
                    faceInfo = faceInfoArray[j]
                    # First Field = Shape info.
                    faceShapeInfo = faceInfo[0]
                    # Second Field = Extra info (empty for now).
                    faceExtraInfo = faceInfo[1]
                    return faceExtraInfo[2]
                   # if faceExtraInfo[2]:
                    #    print '是'
                     #   print faceExtraInfo[2]
                      #  if faceExtraInfo[2] in Name0:
                       #     tts.say(faceExtraInfo[2])
                        #    tts.say('success')
                         #   Name1.append(faceExtraInfo[2])
                          #  Name0.remove(faceExtraInfo[2])
                        # tts.say(faceExtraInfo[2])
                    #else:
                     #   print 'fuck'
                      #  s = 'who are you'
                       # tts.say(s)
                
            except Exception, e:
                pass
            #print "faces detected, but it seems getData is invalid. ALValue ="
            #print val
            #print "Error msg %s" % (str(e))
        else:
            print "No face detected"
            s = '没有检测到脸'
            self.tts.say(s)
            return '没有脸'



if __name__ == '__main__':
    IP = "169.254.50.227"  # Replace here with your NaoQi's IP address.
    PORT = 9559
    robot = Robot(IP,PORT)
    robot.tts.say('欢迎使用签到系统')
    Name0 = ['魏凌枫','李一曼','帅青']
    Name1 = []
    Meet = {'魏凌枫':0,'李一曼':0,'帅青':0}
    for people in Name0:
        robot.tts.say(people)
        robot.tts.say('还没有学习')
        robot.tts.say('是否进行学习')
        if raw_input() == 'y':
            robot.learnFace(people)
    ####################################
    robot.tts.say('开始签到')
    while Name0:
        time.sleep(1)
        people = robot.recogFace()
        if people and people!='没有脸':
            robot.tts.say(people)
            if people in Name0:
                robot.tts.say('签到成功')
                Name0.remove(people)
                Name1.append(people)
                Meet[people]+=1
            else:
                Meet[people]+=1
                robot.tts.say('第'+str(Meet[people])+'次见到你')
        elif people == '没有脸':
            robot.tts.say('这里没有人')
        else:
            robot.tts.say('我不认识')
    robot.tts.say('所有人都来齐了')
    robot.faceProxy.clearDatabase()
    robot.faceProxy.unsubscribe("Test_Face")