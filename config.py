#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 18:13:21 2018

@author: siva
"""

import pandas as pd

config = pd.read_pickle("config_pkl")
cities = pd.read_pickle("cities_pkl")
states = pd.read_pickle("states_pkl")

def conversion(num):
    for i in range(0, len(config)):
        if config["configvalueid"].values[i] == num:
            val = config["configvalue"].values[i]
    
    return val

def cities_conv(num):
    for i in range(0, len(cities)):
        if cities["id"].values[i] == num:
            val = cities["name"].values[i]
    
    return val    

def states_conv(num):
    for i in range(0, len(states)):
        if states["id"].values[i] == num:
            val = config["name"].values[i]
    
    return val      

# c= cities_conv(4460)
    


