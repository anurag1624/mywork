#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 18:08:22 2018

@author: siva
"""

import cv2

def Ear_feat(img_path):
    left_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_leftear.xml')
    right_ear_cascade = cv2.CascadeClassifier('haarcascade_mcs_rightear.xml')
    if left_ear_cascade.empty():
        raise IOError('Unable to load the left ear cascade classifier xml file')
    if right_ear_cascade.empty():
        raise IOError('Unable to load the right ear cascade classifier xml file')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    left_ear = left_ear_cascade.detectMultiScale(gray, 1.3, 1)
    right_ear = right_ear_cascade.detectMultiScale(gray, 1.3, 1)
    for (x,y,w,h) in left_ear:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
    for (x,y,w,h) in right_ear:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 3)
    #cv2.imshow('Ear Detector', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    ef =[]
    try:
        Ear_height = right_ear[0,3]
        Ear_width = right_ear[0,2]       
    
    except:
        try:
            Ear_height = left_ear[0,3]
            Ear_width = left_ear[0,2]
        except:
            Ear_height = "None"
            Ear_width = "None"
        
    ef.append(Ear_height)
    ef.append(Ear_width)
    return ef

#e = Ear_feat("/home/siva/Desktop/Face_shape/Image/r45l.jpg")
