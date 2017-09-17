# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 16:44:19 2017

@author: ndoannguyen
"""


import Constants, Group, Question, Current

from pymongo import MongoClient

def fetchPlayer(series, player_name):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    rs = DB[series + "__" + Constants.PLAYER_SUFFIX].find_one({"_id": player_name})
    mongo_client.close()
    return rs

def fetchAllPlayers(current):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    rs = list( DB[current["series"] + "__" + Constants.PLAYER_SUFFIX].find({"_id": {"$in" : current["players"] }}) )
    mongo_client.close()
    rs = sorted(rs, key=lambda x: -x["point"])
    return rs
    
def updatePlayers(series, player_names_str):
    groups = Group.fetchGroups(series)
    questions = Question.fetchQuestions(series)
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[series + "__" + Constants.PLAYER_SUFFIX]
    
    PlayerCollection.drop()
    
    player_names_str = player_names_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" ", "_")
    player_names = player_names_str.split(",")
    
    players = {}

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
                if int(question["_id"][3:]) < group["group_nb_questions"]:
                    players[player][question["_id"] + "_answer"] = -1
                    players[player][question["_id"] + "_time"] = -1.0
                    players[player][question["_id"] + "_point"] = 0     
    
    for pl in players.keys():
        PlayerCollection.update_one({"_id": players[pl]["_id"]}, {"$set": players[pl]}, upsert=True)
        
    mongo_client.close()

def dropPlayerCollection(series):
    mongo_client = MongoClient('localhost', 27017)
    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[series + "__" + Constants.PLAYER_SUFFIX]
    
    PlayerCollection.drop()
    mongo_client.close()
    
def updatePartialPlayers(current, player_names_str, old_player_names):
    groups = Group.fetchGroups(current["series"])
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    
    player_names_str = player_names_str.replace(" , ", ",").replace(", ", ",").replace(" ,", ",").replace(" ", "_")
    player_names = player_names_str.split(",")
    players = {}

    for player in old_player_names:
        players[player] = {}
        players[player]["_id"] = player
        players[player]["star_chosen"] = 0
        if player in player_names:
            players[player]["G" + str(current["group"]) + "_active"] = 1
        else:
            players[player]["G" + str(current["group"]) + "_active"] = 0
            players[player]["G" + str(current["group"]) + "_nb_stars"] = groups[current["group"]]["group_nb_stars"]
    
    for pl in players.keys():
        PlayerCollection.update_one({"_id": players[pl]["_id"]}, {"$set": players[pl]}, upsert=True)
    
    mongo_client.close()


def updateAnswer(current, player_name, answer):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer" : answer}}, upsert=True)
    mongo_client.close()

def updateTime(current, player_name, timestamp, beginning_timestamp):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_time" : (timestamp - beginning_timestamp)/1000.}}, upsert=True)
    mongo_client.close()

def updateStarChosen(current, player_name, star_chosen):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]    
    
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"star_chosen": star_chosen}}, upsert=True)
    PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_nb_stars": -star_chosen} }, upsert=True)
    mongo_client.close()

def haveRightToAnswer(current, player_name):
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    player = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX].find_one({"_id": player_name})
    res = Current.isActive(current) and player["G" + str(current["group"]) + "_active"] == 1 and player["G" + str(current["group"]) + "Q" + str(current["question"]) + "_answer"] == -1
    if not res:
        mongo_client.close()
        return False
    GroupCollection = DB[current["series"] + "__" + Constants.GROUP_SUFFIX]
    group = GroupCollection.find_one({"_id": "G" + str(current["group"])})
    QuestionCollection = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX]
    question = QuestionCollection.find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
    mongo_client.close()
    if group["group_answer_mode"] == 0:
        current_answers = question["question_answers_from_player"]
        if len(current_answers) > 0:            
            return False
    if group["group_answer_mode"] == 1:
        current_answers = question["question_answers_from_player"]
        if "question_answer" in question.keys() and question["question_answer"] in current_answers:
            return False
    return True
   
def loseTurnInNextQuestion(DB, current, player_name):
    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]
    PlayerCollection.update_one({"_id": player_name}, {"$set": {"G" + str(current["group"]) + "Q" + str(current["question"] + 1) + "_answer" : Constants.NO_ANSWER}}, upsert=True)
   
def answer(current, player_name, answer, timestamp):
    hRTA = haveRightToAnswer(current, player_name)
    mongo_client = MongoClient('localhost', 27017)

    DB = mongo_client[Constants.DBNAME]
    GroupCollection = DB[current["series"] + "__" + Constants.GROUP_SUFFIX]
    QuestionCollection = DB[current["series"] + "__" + Constants.QUESTION_SUFFIX]
    question = QuestionCollection.find_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])})
    beginning_timestamp = question["question_start_timestamp"]
    current_answers = question["question_answers_from_player"] + [answer]
    current_times = question["question_times_from_player"] + [round((timestamp - question["question_start_timestamp"])/1000., 2)]
    answered_players = question["question_answered_players"] + [player_name]
    QuestionCollection.update_one({"_id": "G" + str(current["group"]) + "Q" + str(current["question"])}, {"$set": {"question_answers_from_player": current_answers, "question_times_from_player": current_times, "question_answered_players": answered_players}}, upsert=True)


    PlayerCollection = DB[current["series"] + "__" + Constants.PLAYER_SUFFIX]

    player = PlayerCollection.find_one({"_id": player_name})
    group = GroupCollection.find_one({"_id": "G" + str(current["group"])})
    mongo_client.close()
    updateAnswer(current, player_name, answer)
    updateTime(current, player_name, timestamp, beginning_timestamp) 
        
    if group["group_answer_mode"] == 0:
        Current.updateCurrentStatus(Constants.WAITING_Q)
            
    elif group["group_answer_mode"] == 1 and answer == question["question_answer"]:
        Current.updateCurrentStatus(Constants.WAITING_Q)
    
    if hRTA:  
        mongo_client = MongoClient('localhost', 27017)

        DB = mongo_client[Constants.DBNAME]
        if answer == question["question_answer"]:
            if player["star_chosen"] == 1:
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_point": question["question_star_bonus"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_star_bonus"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_star_bonus"]} }, upsert=True)
            else:
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_point": question["question_bonus"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": question["question_bonus"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": question["question_bonus"]} }, upsert=True)
    
        else:
            if player["star_chosen"] == 1:
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_point": 0 - question["question_star_penalty"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": 0 - question["question_star_penalty"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": 0 - question["question_star_penalty"]} }, upsert=True)
                if group["group_star_lose_turn"] == 1 or group["group_lose_turn"] == 1:
                    loseTurnInNextQuestion(DB, current, player_name)
            else:
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "Q" + str(current["question"]) + "_point": 0 - question["question_penalty"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"G" + str(current["group"]) + "_point": 0 - question["question_penalty"]} }, upsert=True)
                PlayerCollection.update_one({"_id": player_name}, {"$inc": {"point": 0 - question["question_penalty"]} }, upsert=True)
                if group["group_lose_turn"] == 1:
                    loseTurnInNextQuestion(DB, current, player_name)
        mongo_client.close()
        
    updateStarChosen(current, player_name, 0)