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

    
def fetchCurrent():
    return CurrentCollection.find_one({"_id": "current"})

def fetchCurrentGroup(current):
    return DB[current["series"] + "__" + Constants.GROUP_SUFFIX].find_one({"_id": "G" + str(current["group"])})

def fetchCurrentQuestion(current):
    return DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
    
def updateCurrentSeriesName(series):
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"series": series}}, upsert=True)
    
def updateCurrentPlayers(players_str):
    players_str = players_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" ", "_")
    players = players_str.split(",")
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"players": players}}, upsert=True)

def updateCurrentStatus(status):
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"status": status}}, upsert=True)

def updateCurrentGroup(group):
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"group": group}}, upsert=True)

def updateCurrentQuestion(question):
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"question": question}}, upsert=True)

def updateCurrentNbGroups(nb):
    CurrentCollection.update_one({"_id": "current"}, {"$set": {"nb_groups": nb}}, upsert=True)

def activateQuestion(current):
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"active": 1}}, upsert=True)

def deactivateQuestion(current):
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"active": 0}}, upsert=True)

def isActive(current):
    active = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})["active"]
    return active == 1

def updateQuestionTimestamp(current, timestamp):
    DB[current["series"] + "__" + Constants.QUESTION_SUFFIX].update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"question_start_timestamp": timestamp}}, upsert=True)

def updateGroupTimestamp(current, timestamp):
    DB[current["series"] + "__" + Constants.GROUP_SUFFIX].update_one({"_id": "G" + str(current["group"])}, {"$set": {"group_start_timestamp": timestamp}}, upsert=True)

def resetCurrent():
    updateCurrentPlayers("")
    updateCurrentStatus(Constants.RESET)
    updateCurrentGroup(0)
    updateCurrentQuestion(0)