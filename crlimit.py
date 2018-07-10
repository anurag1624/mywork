#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:14:19 2018

@author: siva
"""

def credit_limit(score, A, B):
    
    if score >= 55:
        limit = (A-B)*0.4
    elif score >= 41 and score <54:
        limit = (A-B)* 0.3
    elif score >= 31 and score <41:
        limit = (A-B)* 0.25
    elif score >= 24 and score <31:
        limit = (A-B)* 0.2
    elif score >= 16 and score <24:
        limit = (A-B)* 0.15
    elif score >= 10 and score <16:
        limit = (A-B)* 0.1
    elif score >= 5 and score < 10:
        limit = (A-B)* 0.05        
    else:
        limit = 0
    
    return limit
           
    