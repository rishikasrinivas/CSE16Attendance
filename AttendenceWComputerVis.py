"""
Idea:
Scan id using computer vision
The scan goes into a pandas df
Df holds all students names and id’s
If id from scan matches id in a list mark that student as present
Go through column and print absents
    ex: Df[df[‘quiz3attendence’] == absent]
"""

import cv2
from pyzbar.pyzbar import decode
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)

while True:
    success, img = capture.read() # read the images and save it to var frame
    print(decode(img))
    for barcode in decode(img):
        x,y,w,h = barcode.rect
        cv2.rectangle(img, (x,y), (x+w, y+h), 0 , 0, 255,4)
        name = barcode.data.decode('utf-8')
        # bounding box around barcode
        cv2.putText(img,name, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255), 2)
    cv2.imshow('ID Scanner',img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break





