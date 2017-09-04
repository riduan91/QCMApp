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

def getSeries():
    series_with_suffix = DB.collection_names()
    res = []
    for item in series_with_suffix:
        if ("__" + Constants.GROUP_SUFFIX in item):
            pos = item.index("__")
            res.append(item[:pos])
    return res

def updateGroups(query):
    
    series = query["series"];
    GroupCollection = DB[series + "__" + Constants.GROUP_SUFFIX]
    
    nb_groups = int(query["nb_groups"]);
    groups = []
    
    nb_groups_in_collection = GroupCollection.count()
    
    for gr in range(nb_groups):
        groups.append({})
        groups[gr]["_id"] = "G" + str(gr);
        if (not "group_star_bonus_" + str(gr) in query.keys()):
            groups[gr]["group_star_bonus"] = 0
        if (not "group_star_penalty_" + str(gr) in query.keys()):
            groups[gr]["group_star_penalty"] = 0
        if (not "group_star_lose_turn_" + str(gr) in query.keys()):
            groups[gr]["group_star_lose_turn"] = 0
        if (not "group_nb_options_" + str(gr) in query.keys()):
            groups[gr]["group_nb_options"] = 4
        if (not "group_nb_players_" + str(gr) in query.keys()):
            groups[gr]["group_nb_players"] = 0
        if (not "group_player_names_" + str(gr) in query.keys()):
            groups[gr]["group_player_names"] = []
        if (not "group_start_timestamp_" + str(gr) in query.keys()):
            groups[gr]["group_start_timestamp"] = ""
        
    for key, value in query.items():
        #parseData
        try:
            last_ = key.rfind("_")
            gr = int(key[last_ + 1 :])    
            groups[gr][key[: last_]] = convertInt(value)
        except:
            pass
    
    for gr in range(nb_groups):
        GroupCollection.update_one({"_id": "G" + str(gr)}, {"$set": groups[gr]}, upsert=True)
    
    for gr in range(nb_groups, nb_groups_in_collection):
        GroupCollection.delete_one({"_id": "G" + str(gr)})
    
    return

def fetchGroups(series):
    GroupCollection = DB[series + "__" + Constants.GROUP_SUFFIX]
    return list(GroupCollection.find({}))
    
def updateQuestions(series, query):    
    QuestionCollection = DB[series + "__" + Constants.QUESTION_SUFFIX]
    
    groups = fetchGroups(series)
    
    questions = []
    nb_questions_in_collection = QuestionCollection.count()
    
    for gr in range(len(groups)):
        questions.append([])
        nb_questions = groups[gr]["group_nb_questions"]
        for q in range(nb_questions):
            questions[gr].append({})
            questions[gr][q]["_id"] = "G" + str(gr) + "Q" + str(q) 
    
    
    for key, value in query.items():
        try:
            last_ = key.rfind("_")
            q = int(key[last_ + 1: ])
            gr = int(key[last_ - 1])
            questions[gr][q][key[: last_ - 2:]] = convertInt(value)
        except:
            pass
    
        
    for gr in range(len(groups)):
        for q in range(len(questions[gr])):
            QuestionCollection.update_one({"_id": "G" + str(gr) + "Q" + str(q)}, {"$set": questions[gr][q]}, upsert=True)
        
        for q in range(len(questions[gr]), nb_questions_in_collection):
            QuestionCollection.delete_one({"_id": "G" + str(gr) + "Q" + str(q)})
         
    return

def fetchQuestions(series):
    QuestionCollection = DB[series + "__" + Constants.QUESTION_SUFFIX]
    
    res_list = list(QuestionCollection.find({}))
    groups = fetchGroups(series)
    
    questions = []
    for gr in range(len(groups)):
        questions.append([])
        nb_questions = groups[gr]["group_nb_questions"]
        for q in range(nb_questions):
            questions[gr].append({})
    
    for item in res_list:
        _id = item["_id"]
        q = int(_id[3:])
        gr = int(_id[1])
        for key, value in item.items():
            if (key != "_id"):
                questions[gr][q][key] = value
    
    return questions       

def convertInt(s):
    try:
        return int(s)
    except ValueError:
        return s

