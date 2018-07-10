#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:14:04 2018

@author: siva
"""

import pandas as pd

score = pd.read_pickle('score_pkl')


def b_score(bio_res):
    bio_score = []
    score_bio = score[score["Domain"] == "BIO"]
    score_bio["Category"] = score_bio["Category"].str.capitalize()
    score_bio["Subcategory"] = score_bio["Subcategory"].str.strip()
    for k,v in bio_res.items():
        v = v.strip()
        ind = score_bio[(score_bio['Category'] == k) & (score_bio['Subcategory'] == v)].index
        bio_score.append(score_bio["Score"].values[ind[0]])
    return sum(bio_score)


'''b_res = {'Eyebrows': 'Straight', 'Eyes': 'Small Eyes in comparison to overall face size',
         'Cheaks': 'Meaty / Fleshy', 'Chin': 'Square', 'Nose': 'Thick Aquiline Nose with Tip Pointing Up / High (Front + Side View)', 
         'Ears': 'Vertical Ears', 'Lips': 'Heart Shaped Lips', 'Face': 'Square'}'''

# sc = b_score(b_res)



