#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:49:37 2018

@author: siva
"""

from pymongo import MongoClient
import pandas as pd
# from flask import jsonify

def scores():
    uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    cli = MongoClient(uri)    
    db = cli.LOBOT
    return db

def read_mongo(db):
    cursor = db.LOBOTRule.find()
    df =  pd.DataFrame(list(cursor))
    return df

db  = scores()
score = read_mongo(db)

score["Max Range"] = pd.to_numeric(score["Max Range"],errors='coerce')
score["Min Range"] = pd.to_numeric(score["Min Range"],errors='coerce')
score["Score"] = pd.to_numeric(score["Score"],errors='coerce')
score = score.fillna("Null")

score_pkl = score.to_pickle("score_pkl")
