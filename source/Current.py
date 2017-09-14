# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 18:31:23 2017

@author: ndoannguyen
"""

import Constants

from pymongo import MongoClient

    
def fetchCurrent():
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    rs = CurrentCollection.find_one({"_id": "current"})
    mongo_client.close()
    return rs

def fetchCurrentGroup(current):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    rs = DB[current["series"] + "__" + Constants.GROUP_SUFFIX].find_one({"_id": "G" + str(current["group"])})
    mongo_client.close()
    return rs
    
def fetchCurrentQuestion(current):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    rs = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
    mongo_client.close()
    return rs
    
def updateCurrentSeriesName(series):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"series": series}}, upsert=True)
    mongo_client.close()
    
def updateCurrentPlayers(players_str):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    players_str = players_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" ", "_")
    players = players_str.split(",")
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"players": players}}, upsert=True)
    mongo_client.close()
    
def updateCurrentStatus(status):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"status": status}}, upsert=True)
    mongo_client.close()
    
def updateCurrentGroup(group):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"group": group}}, upsert=True)
    mongo_client.close()
    
def updateCurrentQuestion(question):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"question": question}}, upsert=True)
    mongo_client.close()
    
def updateCurrentNbGroups(nb):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    CurrentCollection = DB[Constants.CURRENT]
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"nb_groups": nb}}, upsert=True)
    mongo_client.close()
    
def activateQuestion(current):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"active": 1}}, upsert=True)
    mongo_client.close()
    
def deactivateQuestion(current):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"active": 0}}, upsert=True)
    mongo_client.close()
    
def isActive(current):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    active = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})["active"]
    mongo_client.close()
    return active == 1

def updateQuestionTimestamp(current, timestamp):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"question_start_timestamp": timestamp}}, upsert=True)
    mongo_client.close()

def updateGroupTimestamp(current, timestamp):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    DB[current["series"] + "__" + Constants.GROUP_SUFFIX].update_one({"_id": "G" + str(current["group"])}, {"$set": {"group_start_timestamp": timestamp}}, upsert=True)
    mongo_client.close()

def resetCurrent():
    updateCurrentPlayers("")
    updateCurrentStatus(Constants.RESET)
    updateCurrentGroup(0)
    updateCurrentQuestion(0)