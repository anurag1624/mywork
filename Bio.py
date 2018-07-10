#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:03:17 2018

@author: siva
"""

import features as feat
import ear
import numpy as np
import pickle

# ---------------Face unpickling-----------------
clf_read = open('clf_pickle.pkl', 'rb')
clf = pickle.load(clf_read)

ss_read = open('ss_pickle.pkl', 'rb')
ss = pickle.load(ss_read)

# ----- Chin Unpickling------------------
ss_chin_read = open('chinss_pickle.pkl', 'rb')
ss_chin = pickle.load(ss_chin_read)

chin_clf_read = open('chin_pickle.pkl', 'rb')
clf_chin = pickle.load(chin_clf_read)


class BioInfo:

    def __init__(self, front_file_path, side_file_path):
        # ------------Ear Feature -------------------
        self.ear_feat = ear.Ear_feat(side_file_path)
        self.ear_height = self.ear_feat[0]
        self.ear_width = self.ear_feat[1]
    
        # ---------------self.features Extraction----------------
        self.features = feat.Extract_features(front_file_path)
    
        # ----------Predicting Face----------------
        self.X_test = self.features[:26]
        self.X_test = np.array(self.X_test)
        self.X_test = np.reshape(self.X_test,(1,-1))
        self.X_test  = ss.transform(self.X_test)
        self.face_result1 = clf.predict(self.X_test)
        self.face_result = int(self.face_result1[0])
    
        # ---------------------predicting chin------
        self.X_test_c = self.features[41:43]
        self.X_test_c = np.array(self.X_test_c)
        self.X_test_c = np.reshape(self.X_test_c,(1,-1))
        self.X_test_c  = ss_chin.transform(self.X_test_c)
        self.chin_result1 = clf_chin.predict(self.X_test_c)
        self.chin_result = int(self.chin_result1[0])

        self.face = {}

    def face_func(self, face_result):

        jaw_width = self.features[27]
        fh_width = self.features[26]
        face_hwratio = self.features[0]

        if face_result == 0:
            if fh_width > jaw_width:
                faceshape = "Inverted Triangle"
            else:
                faceshape = "Diamond"
        elif face_result == 1:
            faceshape = "Oblong"
        elif face_result == 2:
            faceshape = "Oval"
        elif face_result == 4 or self.chin_result == 2:
            if fh_width < (3*jaw_width):
                if face_hwratio > 1.4:
                    faceshape = "Rectangular"
                else:
                    faceshape = "Square"
            else:
                faceshape = "Triangular"
        else:
            faceshape = "Round"
        return faceshape

    # ----Co-ordinates from 28 to 31-------

    def eye_func(self):
        if max(self.features[28],self.features[29])<0.04 or max(self.features[28],self.features[29])<0.25*self.features[30]:
            eye_shape = "Small Eyes in comparison to overall face size"
        elif self.features[31] > (1.5*self.features[30]):
            eye_shape = "Big Space Between both Eyes"
        elif max(self.features[28],self.features[29])>0.05 or max(self.features[28],self.features[29])>0.33*self.features[30]:
            eye_shape = "Large Round Eyes"
        else:
            eye_shape = "Big Space Between both Eyes"
        return eye_shape

    # ----Co-ordinates from 32 to 40-------

    def lip_func(self, fs):
        tight_list = min(self.features[32], self.features[33], self.features[34])
        if fs == "Square" and tight_list <= 1 and self.features[37] >= 3.5:
            shape = "Tight Lip with Square Jaw"
        elif self.features[40][1] < self.features[40][0]:
            shape = "Lips Pointing Down"
        elif self.features[38] < (self.features[39]*0.8) and tight_list > 1 and self.features[37]<4 and tight_list < (0.2*self.features[39]):
            shape = "Heart Shaped Lips"
        elif self.features[36] < 1:
            shape = "Upper Lip Covers small part of Lower Lip"
        elif tight_list >= 1  and self.features[37] > 3.2 < (0.2 * self.features[39]):
            shape = "Small Lips"
        else:
            shape = "Lower lip slightly thicker than upper"
        return shape

    def chin_func(self):
        if self.chin_result == 0:
            if self.features[0] < 1.3:
                chin_shape = "Sharp"
            else:
                chin_shape = "Bony"
        elif self.chin_result == 1:
            chin_shape = "Round"
        elif self.chin_result == 2:
            chin_shape = "Square"

        return chin_shape

    #  ------Cheek Coordinates 41 to 44-------------------

    def cheek_func(self, fs, chs):
        if chs == "Bony":
            if self.features[44] < 0.95 and self.features[0] > 1.5:  # standard >1.34
                cheek = "Sunken Cheak"
            elif self.features[44] < 0.95 and self.features[0] < 1.5:
                cheek = "100% Round & Full Cheak"
            else:
                cheek = "Meaty / Fleshy"

        elif chs == "Round" or chs == "Sharp" :
            if self.features[0] < 1.3 and fs != "Square" and fs != "Rectangle":
                if self.features[44] > 0.97 :
                    cheek = "Cheak Raised to Eye (Front / Side View)"
                else:
                    cheek = "Meaty / Fleshy"
            elif self.features[0] > 1.35 and fs!="Square" and fs != "Rectangle":
                cheek = "Meaty / Fleshy"
            else:
                cheek = "100% Round & Full Cheak"

        elif chs == "Square" :
            if fs == "Rectangle" :
                if self.features[0]<1.47:
                    cheek = "100% Round & Full Cheak"
                else:
                    cheek = "Meaty / Fleshy"
            else:
                if self.features[0]>1.35:
                    if self.features[0]<1.4:
                        cheek = "100% Round & Full Cheak"
                else:
                    cheek = "Meaty / Fleshy"
        return cheek

    # ------ Nose Co-ordinates  45 to 47-------------

    def nose_func(self):
        if self.features[45] >= 0.65 and self.features[46] <= 0.25:
            nose = "Snub Nose (Side View)"
        elif self.features[45] <= 0.45 :
            nose = "Narrow Acquiline Nose (Front + Side View)"
        elif 0.55 >= self.features[45] >= 0.45 >= self.features[47]:
            nose = "Acquiline Nose with Tip curved Down (Front & Side View)"
        elif self.features[47]>=1.2 and self.features[45]<=0.55:
            nose = "Straight Well Formed Nose"
        elif self.features[45]>=0.55 and self.features[46]>0.25:
            if self.features[47]<=0.60:
                nose = "Thick Aquiline Nose with Tip Bent Down (Front + Side View)"
            else:
                nose = "Thick Aquiline Nose with Tip Pointing Up / High (Front + Side View)"
        else:
            nose= "Straight Well Formed Nose"

        return nose

    # -------------48 to 50--------------------

    def ear_func(self, ear_height, ear_width):
        if ear_height == "None" or ear_width == "None":
            ears = "Vertical Ears (Side View)"
        elif (ear_height/self.features[49]) < 0.25:
            ears = "Small Ears in comparison to overall face size  (Front + Side View)"
        elif (ear_width/self.features[50]) > 40:
            ears = "Distanced Ears from Face "
        elif (ear_width/self.features[50]) > 0.2 and ear_height > (0.85*self.features[48]):
            ears = "Big Ears with Thick Ear Lobe (Front + Side View)"
        elif ear_height > (0.95*self.features[48]):
            ears = "Ears that get / start over Eyebrows"
        elif ear_height < (0.75*self.features[48]):
            ears = "Ears don’t cross eyebrows & bottom of nose"
        else:
            ears = "Vertical Ears (Side View)"
        return ears

    # ----------------------51 to 54---------------

    def eyebrow_func(self):
        if self.features[51]<1.3:
            eyebrow = "Low Eyebrows - Near to eyes"
        elif self.features[52][2]>0.9 or self.features[52][0]==0 or self.features[52][0]<0.25:
            eyebrow = "Straight"
        elif self.features[52][2]<0.5 and self.features[52][0]!=0 :
            eyebrow = "Angled"
        elif self.features[52][2]>0.65:
            eyebrow = "Curved"
        elif self.features[51]>1.45:
            eyebrow = "High Eyebrows - Compare to nose start"
        elif min(self.features[53]) >200:
            eyebrow = "Nearly Invisible Eyebrows"

        else:
            eyebrow = "Straight"

        return eyebrow

    def main(self):
        fs = self.face_func(self.face_result)
        es = self.eye_func()
        ls = self.lip_func(fs)
        chs = self.chin_func()
        cs = self.cheek_func(fs,chs)
        ns = self.nose_func()
        ears = self.ear_func(self.ear_height,self.ear_width)
        eb = self.eyebrow_func()

        bio_features = {"Face":fs, "Chin": chs, "Cheaks": cs,
                        "Eyes": es, "Lips": ls, "Nose": ns,
                        "Ears": ears, "Eyebrows": eb}
        print (bio_features)
        return bio_features


'''bo = BioInfo("/home/siva/Desktop/Face_shape/Image/r23.jpg",
             "/home/siva/Desktop/Face_shape/Image/r23r.jpg")
res = bo.main()
'''



