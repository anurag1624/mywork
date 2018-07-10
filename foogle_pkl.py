#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 12:34:01 2018

@author: siva
"""

from pymongo import MongoClient
import pandas as pd

def foogle_func():
    uri = "mongodb://atlmongo:KcNrtLOiTlz3J7UEgzUl978r3GK8ycJu9d3iPYnQ0yr4hYwpQwVatiFOt6NYJurpq4Q4Odmdl0AcSSo6vYkftw==@atlmongo.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
    cli = MongoClient(uri)    
    db = cli.LOBOT
    return db

def read_mongo(db):
    cursor = db.Foogle.find()
    df =  pd.DataFrame(list(cursor))
    return df

db  = foogle_func()
foogle = read_mongo(db)

foogle_pkl = foogle.to_pickle("foogle_pkl")