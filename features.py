#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:33:36 2018

@author: siva
"""

5#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 20:02:54 2018

@author: siva
"""

# This script detects the face(s) in the image, specifies the bounding box, detects the facial landmarks, and extracts the features for training

import numpy as np
import cv2
import dlib
#import matplotlib.pyplot as plt
import math



def get_lum(image, x, y, w, h, k, gray):
    if gray == 1: image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    i1 = range(int(-w / 2), int(w / 2))
    j1 = range(0, h)

    lumar = np.zeros((len(i1), len(j1)))
    for i in i1:
        for j in j1:
            lum = np.min(image[y + k * h, x + i])
            lumar[i][j] = lum

    return np.min(lumar)



def d(landmarks, index1, index2):
    # get distance between i1 and i2

    x1 = landmarks[int(index1)][0]
    y1 = landmarks[int(index1)][1]
    x2 = landmarks[int(index2)][0]
    y2 = landmarks[int(index2)][1]

    x_diff = (x1 - x2) ** 2
    y_diff = (y1 - y2) ** 2

    dist = math.sqrt(x_diff + y_diff)

    return dist


def que(landmarks, index1, index2):
    # get angle between a i1 and i2

    x1 = landmarks[int(index1)][0]
    y1 = landmarks[int(index1)][1]
    x2 = landmarks[int(index2)][0]
    y2 = landmarks[int(index2)][1]

    x_diff = float(x1 - x2)

    if (y1 == y2): y_diff = 0.1
    if (y1 < y2): y_diff = float(np.absolute(y1 - y2))
    if (y1 > y2):
        y_diff = 0.1
        #print("Error: Facial feature located below chin.")

    return np.absolute(math.atan(x_diff / y_diff))


# image_dir should contain sub-folders containing the images where features need to be extracted
# only one face should be present in each image
# if multiple faces are detected by OpenCV, image must be manually edited; the parameters of the face-detection routine can also be changed

def Extract_features(image_dir):

    cascade_path = "haarcascade_frontalface_default.xml"
    predictor_path = "shape_predictor_68_face_landmarks.dat"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascade_path)

    # create the landmark predictor
    predictor = dlib.shape_predictor(predictor_path)

    #features = []

    image = cv2.imread(image_dir)
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image1 = image.copy()
    
    # convert the image to grayscale
    gray = cv2.imread(image_dir, 0)
    gray1 = cv2.imread(image_dir, 0)
    # Detect faces in the image; you can change the parameters if multiple faces are detected for most images; otherwie, it is easier to edit the images if only a couple have multiple face detections
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,  # 1.1
        minNeighbors=9,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    if len(faces)>1:
        raise ImportError("Too Many Faces Found")
    elif len(faces) == 0:
        raise ImportError("No Faces Found")


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)

        # Converting the OpenCV rectangle coordinates to Dlib rectangle
        dlib_rect = dlib.rectangle(int(x), int(0.95 * y), int(x + w), int(y + 1.05 * h))

        detected_landmarks = predictor(image, dlib_rect).parts()
        landmarks = np.matrix([[p.x, p.y] for p in detected_landmarks])

        # copying the image so we can see side-by-side
        image_copy = image.copy()
        

        for idx, point in enumerate(landmarks):
#            pos = (point[0, 0], point[0, 1])

            # draw points on the landmark positions
            #cv2.circle(image_copy, pos, 2, color=(255, 153, 0))

            # find hairline, p27 is upper point of nose
            # finding the hairline is done by iterating from landmark 27 (upper point of nose bridge) and looking at a significant color difference from the initial point; avoid pictures with bangs or small color differential between skin and hair color

            p27 = (landmarks[27][0, 0], landmarks[27][0, 1])
            p19 = (landmarks[19][0, 0], landmarks[19][0, 1])
            x = p27[0]
            y1 = p19[1]
            
            try:
                lim = 105
                x = p27[0]
                y1 = p19[1]
                gray = 0
                diff = get_lum(image, x, y1, 8, 2, -1, gray)
                limit = diff - lim
                while (diff > limit):                    
                    y1 = int(y1 - 1)
                    diff = get_lum(image, x, y1, 6, 2, -1, gray) 
                #cv2.circle(image_copy, (x, y1), 3, color=(255, 153, 0))
                
            except IndexError:
                try:
                    x = p27[0]
                    y1 = p19[1]
                    gray = 0                  
                    diff = get_lum(image1, x, y1, 8, 2, -1, gray)
                    limit = diff - 55
                    while (diff > limit):
                        y1 = int(y1 - 1)
                        diff = get_lum(image1, x, y1, 6, 2, -1, gray)
                except IndexError:
                    y1 = p19[1]-d(landmarks.tolist(),8,57) 
                    y1 = int(y1)
            #cv2.circle(image_copy, (x, y1), 3, color=(255, 153, 0)) 
                
        
            if (y1<=0) :
                
                y1 = p19[1]-d(landmarks.tolist(),8,57) 
                y1 = int(y1)
            
            try:
                x1 = p27[0]
                y2 = int((p27[1]+y1)/2)
                gray = 0
                diff = get_lum(image, x1, y2, 8, 2, -1, gray)
                limit = diff - 105
                while (diff > limit):                    
                    x1 = int(x1 - 1)
                    diff = get_lum(image, x1, y2, 6, 2, -1, gray) 
                #cv2.circle(image_copy, (x, y1), 3, color=(255, 153, 0))
                
            except IndexError:
                x1 = p27[0]
                y2 = int((p27[1]+y1)/2)
                gray = 0                  
                diff = get_lum(image1, x1, y2, 8, 2, -1, gray)
                limit = diff - 5
                while (diff > limit):
                    x1 = int(x1 - 1)
                    diff = get_lum(image1, x1, y2, 6, 2, -1, gray)
            #cv2.circle(image_copy, (x1, y2), 3, color=(255, 153, 0))
          
            # Show annotated image
        #plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))
        #cv2.imwrite("agreene.jpg", image_copy)
        #plt.show()
        #cv2.waitKey(0)
        lmark = landmarks.tolist()
        if (y1<=0):
            print("default taken")
            y1 = p19[1]-d(lmark,8,57)
        if(x1<=0 ):
            x1 = p19[0]
        p68 = ((x, y1))
        p69 = ((x1,y2)) 
        p70 = ((p27[0],int((p27[1]+y1)/2)))
        lmark.append(p68)
        lmark.append(p69)
        lmark.append(p70)
        f = []
        fwidth = d(lmark, 0, 16)
        fheight = d(lmark, 8, 68)
        f.append(fheight / fwidth)
        jwidth = d(lmark, 4, 12)
        f.append(jwidth / fwidth)
        hchinmouth = d(lmark, 57, 8)
        f.append(hchinmouth / fwidth)
        
        #ref = que(lmark, 27, 8)
        for k in range(0, 17):
            if k != 8:
                theta = que(lmark, k, 8)
                f.append(theta)
        for k in range(1, 8):
            dist = d(lmark, k, 16 - k)
            f.append(dist / fwidth)
        fh_width = d(lmark,69,70)
        f.append(2*fh_width)
        f.append(d(lmark,3,13))
        f.append(d(lmark,37,41)/fheight)
        f.append(d(lmark,38,40)/fheight)
        f.append(d(lmark,36,39)/fheight)
        f.append(d(lmark,42,39)/fheight)
        #----- Lips Co-ordinates--------
        u_lip_mid = d(lmark, 51, 62)
        u_lip = d(lmark, 50, 61)
        u_lip2 = d(lmark, 52, 63)
        u_lipsize = (u_lip+u_lip2)/2
        l_lip = d(lmark, 58, 67)
        l_lip1 = d(lmark, 56, 65)
        l_lipsize = (l_lip+l_lip1)/2   
        lips_height =  l_lipsize+u_lipsize 
        lips_width = d(lmark, 48, 54)
        inner1 = abs(lmark[61][1]-lmark[67][1])
        inner2 = abs(lmark[62][1]-lmark[66][1])
        inner3 = abs(lmark[63][1]-lmark[65][1])
        f.append(inner1)
        f.append(inner2)
        f.append(inner3)
        f.append(lips_height)
        f.append(l_lipsize/u_lipsize)
        f.append(lips_width/lips_height)
        f.append(u_lip_mid)        
        f.append(lips_height/2)
        f.append([lmark[48][1],lmark[58][1]])

        #--------Chin-------------------
        m1 = (lmark[8][1] - lmark[0][1]) / float(lmark[8][0] - lmark[0][0])
        m2 = (lmark[8][1] - lmark[6][1]) / float(lmark[8][0] - lmark[6][0])
        m3 = (lmark[8][1] - lmark[5][1]) / float(lmark[8][0] - lmark[5][0])
        m4 = (lmark[8][1] - lmark[7][1]) / float(lmark[8][0] - lmark[7][0])
        ang = abs((m1 - m2) / (1 + (m1 * m2)))
        ang2 = abs((m1 - m3) / (1 + (m1 * m3)))
        ang3 = abs((m1 - m4) / (1 + (m1 * m4)))
        f.append(ang)
        f.append(ang2)
        f.append(ang3)
        f.append(d(lmark,2,14)/d(lmark,0,16))
        
        #------------Nose-------------------
        # Nose width / Nose Height > 0.65 & nose height/face height <25
        f.append(d(lmark,31,35)/d(lmark,27,33))
        f.append(d(lmark,27,33)/d(lmark, 8, 68))
        mn1 = (lmark[33][1] - lmark[31][1]) / float(lmark[33][0] - lmark[31][0])
        mn2 = (lmark[33][1] - lmark[35][1]) / float(lmark[33][0] - lmark[35][0])
        n_ang = abs((mn1 - mn2) / (1 + (mn1 * mn2)))
        f.append(1.80-n_ang)
        
        #------Ear-------------------------------

        f.append(lmark[33][1]-lmark[24][1])
        f.append(fheight)
        f.append(fwidth)
        
        #=------ Eyebrows----------------------------

        d1 = lmark[33][1]-lmark[23][1]
        d2 = lmark[33][1]- lmark[43][1]
        f.append(d1/float(d2))
        me1 = (lmark[23][1] - lmark[22][1]) / float(lmark[23][0] - lmark[22][0])
        me2 = (lmark[24][1] - lmark[23][1]) / float(lmark[24][0] - lmark[23][0])
        me3 = (lmark[25][1] - lmark[24][1]) / float(lmark[25][0] - lmark[24][0])
        ange1 = abs((me1 - me2) / (1 + (me1 * me2)))
        ange2 = abs((me2 - me3) / (1 + (me3 * me2)))
        try :
            e_ang = [ange1,ange2,ange1/ange2]
        except:
            e_ang = [ange1,ange2,0]
        f.append(e_ang)
        l1 = gray1[lmark[25][0]][lmark[25][1]+2]
        l2 = gray1[lmark[24][0]][lmark[24][1]+2]
        lv = [l1,l2]
        f.append(lv)


        

        
        
        
        
        
       
    return f
#feat = Extract_features("/home/siva/Desktop/Face_shape/Image/ucl1.jpg")

# Eyes
# if max(eye_height)/fheight >0.05 or max(eye_height) > 33%*(eye_width/fheight)
# if eyediff > 1.5*eyewidth then big space b/w eyes
# if max(eye_height)/fheight >0.04 or max(eye_height) < 33%*(eye_width/fheight)

