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

def fetchAllPlayers(current):
    return list( DB[current["series"] + "__" + Constants.PLAYER_SUFFIX].find({"_id": {"$in" : current["players"] }}) )

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
        players[player]["star_chosen"] = 0

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

def updateAnswer(current, player_name, answer):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer" : answer}, upsert=True)

def updateTime(current, player_name, timestamp, beginning_timestamp):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_time" : timestamp - beginning_timestamp}, upsert=True)

def updateStarChosen(current, player_name, star_chosen):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]    
    
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"star_chosen": star_chosen}}, upsert=True)
    PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_nb_stars": -star_chosen} }, upsert=True)

def haveRightToAnswer(current, player_name):
    player = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX].find_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer" : 1})
    res = Current.isActive(current) and player["G" + str(current["group"]) + "_active"] == 1 and player["G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer"] == -1
    if not res:
        return False
    GroupCollection = DB[current["series"] + "__" + Constants.GROUP_SUFFIX]
    group = GroupCollection.find_one({"_id": "G" + str(current["group"])})
    QuestionCollection = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX]
    question = QuestionCollection.find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
    if group["group_answer_mode"] == 0:
        current_answers = question["question_answers_from_player"]
        if len(current_answers) > 0:
            return False
    if group["group_answer_mode"] == 1:
        current_answers = question["question_answers_from_player"]
        if question["question_answer"] in current_answers:
            return False
    return True
   
def loseTurnInNextQuestion(current, player_name):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"G" + str(current["group"]) + "Q" + str(current["question"] + 1) + "_answer" : Constants.NO_ANSWER}, upsert=True)
   
def answer(current, player_name, answer, timestamp):
    if haveRightToAnswer(current, player_name):
        PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
        GroupCollection = DB[current["series"] + "__" + Constants.GROUP_SUFFIX]
        QuestionCollection = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX]
        question = QuestionCollection.find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
        player = PlayerCollection.find_one({"_id": player_name})
        group = GroupCollection.find_one({"_id": "G" + str(current["group"])})
        beginning_timestamp = question["question_start_timestamp"]
        current_answers = question["question_answers_from_player"].append(answer)
        current_times = question["question_times_from_player"].append((timestamp - question["question_start_timestamps"])/1000.)
        answered_players = question["question_answered_players"].append(player_name)
        
        updateAnswer(current, player_name, answer)
        updateTime(current, player_name, timestamp, beginning_timestamp) 
        QuestionCollection.update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"question_current_answers": current_answers, "question_times_from_player": current_times, "question_answered_players": answered_players}}, upsert=True)
        
    if answer == question["question_answer"]:
        if player["star_chosen"] == 1:
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_star_bonus"]} }, upsert=True)
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_star_bonus"]} }, upsert=True)
        else:
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_bonus"]} }, upsert=True)
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_bonus"]} }, upsert=True)
    
    else:
        if player["star_chosen"] == 1:
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_star_bonus"]} }, upsert=True)
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_star_bonus"]} }, upsert=True)
            if group["group_star_lose_turn"] == 1 or group["group_lose_turn"] == 1:
                loseTurnInNextQuestion(current, player_name)
        else:
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_bonus"]} }, upsert=True)
            PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_bonus"]} }, upsert=True)
            if group["group_lose_turn"] == 1:
                loseTurnInNextQuestion(current, player_name)
    
    updateStarChosen(current, player_name, 0)
        