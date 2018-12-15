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
from multiprocessing import Process, Queue
isAlive = False


def write_image(que):
    while True:
        obj = que.get()
        im = obj[0]
        rect = obj[1]
        identifier = obj[2]
        x,y,w,h = rect
        centerX, centerY = obj[3]
        upper_bound, lower_bound = obj[4]
        cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255,0), 2)
        cv2.circle(im, (centerX, centerY),  5, (0, 0,255))
        cv2.circle(im, (centerX, int(lower_bound)), 10, (0, 0, 255))
        cv2.circle(im, (centerX, int(upper_bound)), 10, (0,0,255))
        #print("Image saved")
        cv2.imwrite("feed%03d.png" % identifier, im)


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

def start_flight():
    # make my bebop object
    bebop = Bebop()
    queue = Queue()
    # connect to the bebop
    p = Process(target=write_image, args=(queue,))
    p.start()
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
            inc = 0
            while (now - then).total_seconds() < 20:
                try:
                    im = bebopVision.get_latest_valid_picture()
                    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
                    dimensions = im.shape
                    #print(dimensions)
                    height = dimensions[0]
                    width = dimensions[1]
                    left_bound = width/3
                    right_bound = (width/3) * 2
                    upper_bound = height/5
                    lower_bound = (height/5) * 4
                    #upper_bound -= 50
                    #lower_bound -= 50
                    #Green color in HSV
                    #low = np.array([40, 50, 50])
                    #high = np.array([80, 255, 255])
                    #Pink color in GBR
                    #low = np.array([72, 33, 195])
                    #high = np.array([203, 192, 255])
                    #Blue color in GBR
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
                        #print("Rectangle area", biggestRectArea)
                        #Area range, 9000-13000
                        #Below 9000, move forward
                        #Above 13000, move backward

                        centerX = int(x + w/2)
                        centerY = int(y + h/2)
                        queue.put((im, biggestRect, inc, (centerX, centerY), (upper_bound, lower_bound)))
                        #print("Center X:", centerX)
                        #print("Center Y:", centerY)
                        
                        #if biggestRect is not None:
                        #print("here")
                        
                        if centerY < upper_bound:
                            move_up(bebop, 20, 0.5)
                            print("Moving up")
                            time.sleep(0.5)
                            inc += 1


                        elif centerY > lower_bound:
                            move_down(bebop, 20, 0.5)
                            print("Moving down")
                            time.sleep(0.5)
                            inc += 1


                        elif biggestRectArea < 8000 and centerX < left_bound:
                            move_right(bebop, 20, 1)
                            print("Moving right")
                            time.sleep(1)
                            inc += 1


                        elif biggestRectArea > 8000 and centerX > right_bound:
                            move_left(bebop, 20, 1)
                            print("Moving left")
                            time.sleep(1)
                            inc += 1


                        elif biggestRectArea < 8000:
                            print("Moving forward")
                            move_forward(bebop, 20, 1)
                            time.sleep(1)
                            inc += 1


                        elif biggestRectArea > 15000:
                            move_backward(bebop, 20, 1)
                            print("Moving backward")
                            #move_backward(bebop, 20, 2)
                            time.sleep(1)
                            inc += 1


                        elif centerX < left_bound:
                            move_right(bebop, 20, 1)
                            print("Moving right")
                            time.sleep(1)
                            inc += 1


                        elif centerX > right_bound:
                            move_left(bebop, 20, 1)
                            print("Moving left")
                            time.sleep(1)
                            inc += 1

                    


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
        #bebop.disconnect()
    else:
        print("Error connecting to bebop.  Retry")

if __name__ == "__main__":
    start_flight()