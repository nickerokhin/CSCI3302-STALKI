"""
Code based on demoBebopVision.py in pyparrot/examples
"""
from pyparrot.Bebop import Bebop
from pyparrot.DroneVision import DroneVision
import threading
import cv2
import time
import numpy as np
import os
import datetime
from movements import *
isAlive = False


def clear_images():
    path = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pyparrot/images/"
    images = [image for image in os.listdir(path) if "image" in image]

    for im in images:
        os.remove(path + im)

    print(len(images), "images cleared")

    
    



class UserVision:
    def __init__(self, vision):
        self.index = 0
        self.vision = vision

    def save_pictures(self, args):
        #print("saving picture")
        img = self.vision.get_latest_valid_picture()

        if (img is not None):
            filename = "test_image_%06d.png" % self.index
            #cv2.imwrite(filename, img)
            self.index +=1


# make my bebop object
bebop = Bebop()

# connect to the bebop
success = bebop.connect(5)
clear_images()
if (success):
    # start up the video
    bebopVision = DroneVision(bebop, is_bebop=True)

    userVision = UserVision(bebopVision)
    bebopVision.set_user_callback_function(userVision.save_pictures, user_callback_args=None)
    success = bebopVision.open_video()

    if (success):
        print("Vision successfully started!")
        #removed the user call to this function (it now happens in open_video())
        #bebopVision.start_video_buffering()

        # skipping actually flying for safety purposes indoors - if you want
        # different pictures, move the bebop around by hand
        print("Fly me around by hand!")
        #bebop.smart_sleep(5)

        then = datetime.datetime.now()
        now = datetime.datetime.now()
        bebop.safe_takeoff(10)
        while (now - then).total_seconds() < 20:
            try:
                im = bebopVision.get_latest_valid_picture()
                hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
                dimensions = im.shape
                height = dimensions[0]
                width = dimensions[1]
                left_bound = width/3
                right_bound = (width/3) * 2
                #Green color in HSV
                #low = np.array([40, 50, 50])
                #high = np.array([80, 255, 255])
                #Blue color in HSV
                low = np.array([100, 50, 50])
                high = np.array([140, 255, 255])
                image_mask = cv2.inRange(hsv, low, high)
                kern = np.ones((9,9), np.uint8)
                mask = cv2.morphologyEx(image_mask, cv2.MORPH_OPEN, kern)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kern)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                biggestRect = None
                biggestRectArea = 0
                for c in cnts:
                    rect = cv2.boundingRect(c)
                    x,y,w,h = rect
                    area = w*h
                    if area > biggestRectArea:
                        biggestRect = rect
                        biggestRectArea = area
                if biggestRect is not None:
                    x, y, w, h = biggestRect
                    print(biggestRectArea)
                    #Area range, 9000-13000
                    #Below 9000, move forward
                    #Above 13000, move backward

                    centerX = int(x + w/2)
                    centerY = int(y + h/2)
                    '''
                    if biggestRect is not None:
                        cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255,0), 2)
                        cv2.circle(im, (centerX, centerY),  5, (0, 0,255))
                        print("Image saved")
                        cv2.imwrite("feed%03d.png" % (now - then).total_seconds(), im)
                    '''

                    if biggestRectArea < 8000 and centerX < left_bound:
                        move_right(bebop, 20, 1)
                        print("Moving right")
                        time.sleep(1)
                        continue

                    if biggestRectArea > 8000 and centerX > right_bound:
                        move_left(bebop, 20, 1)
                        print("Moving left")
                        time.sleep(1)
                        continue

                    elif biggestRectArea < 8000:
                        print("Moving forward")
                        move_forward(bebop, 20, 1)
                        time.sleep(1)
                        continue

                    elif biggestRectArea > 15000:
                        move_backward(bebop, 20, 1)
                        print("Moving backward")
                        #move_backward(bebop, 20, 2)
                        time.sleep(1)
                        continue

                    elif centerX < left_bound:
                        move_right(bebop, 20, 1)
                        print("Moving right")
                        time.sleep(1)
                        continue

                    elif centerX > right_bound:
                        move_left(bebop, 20, 1)
                        print("Moving left")
                        time.sleep(1)
                        continue
                


                now = datetime.datetime.now()
            except KeyboardInterrupt:
                print("Emergency landing...")
                bebop.emergency_land()
                exit()
            except Exception as e:
                print(e)
                bebop.emergency_land()
                exit()
        print("Moving the camera using velocity")
        #bebop.pan_tilt_camera_velocity(pan_velocity=0, tilt_velocity=-2, duration=4)
        #bebop.smart_sleep(25)
        print("Finishing demo and stopping vision")
        #bebopVision.close_video()


    # disconnect nicely so we don't need a reboot
    print("Finishing demo, landing....")
    bebop.safe_land(20)
    bebop.disconnect()
else:
    print("Error connecting to bebop.  Retry")

