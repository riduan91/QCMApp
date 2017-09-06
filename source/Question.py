# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 16:52:07 2017

@author: ndoannguyen
"""

import Constants, Group
from Constants import convertInt

from pymongo import MongoClient
mongo_client = MongoClient('localhost', 27017)

DB = mongo_client[Constants.DBNAME]
CurrentCollection = DB[Constants.CURRENT]

def updateQuestions(series, query):    
    QuestionCollection = DB[series + "__" + Constants.QUESTION_SUFFIX]
    
    groups = Group.fetchGroups(series)
    
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
    groups = Group.fetchGroups(series)
    
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
            questions[gr][q][key] = value
    
    return questions       
    
def fetchOneQuestion(series, group, question):
    QuestionCollection = DB[series + "__" + Constants.QUESTION_SUFFIX]
    return QuestionCollection.find_one({"_id": "G" + str(group) + "Q" + str(question)})

def nextQuestion(question_id):
    return question_id[:3] + str(int(question_id[3:]) + 1)