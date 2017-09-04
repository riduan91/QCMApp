# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 18:31:23 2017

@author: ndoannguyen
"""

import Constants

from pymongo import MongoClient
mongo_client = MongoClient('localhost', 27017)

DB = mongo_client[Constants.DBNAME]
CurrentCollection = DB[Constants.CURRENT]

    
def fetchCurrent(series):
    return CurrentCollection.find_one({"_id": series})
    
def updateCurrentSeriesName(series):
    CurrentCollection.update_one({"_id": series}, {"$set": {"series": series}}, upsert=True)
    
def updateCurrentPlayers(series, players_str):
    players_str = players_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",")
    players = players_str.split(",")
    CurrentCollection.update_one({"_id": series}, {"$set": {"players": players}}, upsert=True)
    