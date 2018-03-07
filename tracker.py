#!/usr/bin/env python


import cv2
import numpy as np

WINDOW_NAME = 'TopTakip' 

def tracker(image):

    blur = cv2.GaussianBlur(image, (5,5),0)

  
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    # green
    lower = np.array([40,70,70])
    upper = np.array([80,200,200])

    # blue
    #lower = np.array([110,50,50])
    #upper = np.array([130,255,255])

    # yellow
    #lower = np.array([25,50,50])
    #upper = np.array([32,255,255])

    # red
    #lower = np.array([30,150,50])
    #upper = np.array([255,255,180])

    
    mask = cv2.inRange(hsv, lower, upper)
    
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    ctr = (-1,-1)

    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        cv2.circle(image, ctr, 4, (0,0,0))

    cv2.imshow(WINDOW_NAME, image)

    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    return ctr

if __name__ == '__main__':

    capture = cv2.VideoCapture(0)

    while True:

        result, image = capture.read()

        if result:

            if not tracker(image):
                break
          
            # 27 === ESC
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('hata')
           break
