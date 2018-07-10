#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:08:44 2018

@author: siva
"""

import psycopg2 as pg
import pandas.io.sql as psql

try:
    conn = pg.connect("dbname='CommonConfig' user='pgAdmin@atl-ditenv' host='atl-ditenv.postgres.database.azure.com' password='Postgres12'")
except:
    print "I am unable to connect to the database"
    
    

dataframe = psql.read_sql("SELECT * FROM configurationvalues", conn)
df_cities = psql.read_sql("SELECT * FROM cities", conn)
df_states = psql.read_sql("SELECT * FROM states", conn)

config_pkl = dataframe.to_pickle("config_pkl")
cities_pkl = df_cities.to_pickle("cities_pkl")
states_pkl = df_states.to_pickle("states_pkl")




