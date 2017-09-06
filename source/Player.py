# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 16:44:19 2017

@author: ndoannguyen
"""


import Constants, Group, Question, Current

from pymongo import MongoClient
mongo_client = MongoClient('localhost', 27017)

DB = mongo_client[Constants.DBNAME]
CurrentCollection = DB[Constants.CURRENT]

def fetchPlayer(series, player_name):
    return DB[series + "__" + Constants.PLAYER_SUFFIX].find_one({"_id": player_name})

def updatePlayers(series, player_names_str):
    PlayerCollection = DB[series + "__" + Constants.PLAYER_SUFFIX]
    
    player_names_str = player_names_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" ", "_")
    player_names = player_names_str.split(",")
    
    players = {}
    groups = Group.fetchGroups(series)
    questions = Question.fetchQuestions(series)
    for player in player_names:
        players[player] = {}
        players[player]["_id"] = player
        players[player]["point"] = 0

        for group in groups:
            players[player][group["_id"] + "_active"] = 1
            players[player][group["_id"] + "_nb_stars"] = group["group_nb_stars"]
            players[player][group["_id"] + "_point"] = 0
            
            for question in questions[int(group["_id"][1])]:
                print question
                players[player][question["_id"] + "_answer"] = -1
                players[player][question["_id"] + "_time"] = -1.0
                players[player][question["_id"] + "_point"] = 0
            
    
    for pl in players.keys():
        PlayerCollection.update_one({"_id": players[pl]["_id"]}, {"$set": players[pl]}, upsert=True)

    return players

def updateStarChosen(current, player_name, star_chosen):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]    
    
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"star_chosen": star_chosen}}, upsert=True)
    PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_nb_stars": -star_chosen} }, upsert=True)

def haveRightToAnswer(current, player_name):
    player = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX].find_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer" : 1})
    return Current.isActive(current) and player["G" + str(current["group"]) + "_active"] == 1 and player["G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer"] == -1
    
def answer(current, player_name, answer, timestamp):
    if haveRightToAnswer(current, player_name):
        PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
        QuestionCollection = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX]
        question = QuestionCollection.find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
        
        beginning_timestamp = question["question_start_timestamp"]
        
        PlayerCollection.update_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer" : answer}, upsert=True)
        PlayerCollection.update_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_time" : timestamp - beginning_timestamp}, upsert=True)
        