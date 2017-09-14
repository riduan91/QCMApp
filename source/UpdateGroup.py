# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 18:31:23 2017

@author: ndoannguyen
"""

import Constants

from pymongo import MongoClient
mongo_client = MongoClient('localhost', 27017)

DB = mongo_client[Constants.DBNAME]
Group = DB[Constants.GROUP]    

def chooseRandom(mylist, nb):
    random.shuffle(mylist)
    return mylist[:nb]

def chooseRandomQuestions(nb_questions):
    HistoryQCM = mongo_client[Constants.HISTORY_QCM_DATABASE]
    QuestionCollection = HistoryQCM[Constants.QUESTION_COLLECTION]
    
    total_nb_questions = QuestionCollection.count()
    if nb_questions > total_nb_questions:
        nb_questions = total_nb_questions
        
    raw_question_list = range(1, total_nb_questions + 1)
    random.shuffle(raw_question_list)
    question_id_list = raw_question_list[:nb_questions]
    
    questions = []
    
    for question_id in question_id_list:
        try:
            my_question = QuestionCollection.find_one({ "_id": Constants.QUESTION_PREFIX + str(question_id).zfill(6) })
            questions.append(   {   "_id":      my_question["_id"], 
                                    "zone":     my_question["zone"], 
                                    "period":   my_question["period"], 
                                    "question": my_question["question"], 
                                    "A":        my_question["A"], 
                                    "B":        my_question["B"], 
                                    "C":        my_question["C"], 
                                    "D":        my_question["D"] } )
        except TypeError:
            print "[Error] Question \"%s\" not found in dictionary." % question_id

    return questions

def getResult(question_id):
    HistoryQCM = mongo_client['HistoryQCM']
    QuestionCollection = HistoryQCM['Questions']
    
    my_question = QuestionCollection.find_one({ "_id": question_id })
    res = {   "_id":      my_question["_id"], 
                                    "zone":     my_question["zone"], 
                                    "period":   my_question["period"], 
                                    "question": my_question["question"], 
                                    "A":        my_question["A"], 
                                    "B":        my_question["B"], 
                                    "C":        my_question["C"], 
                                    "D":        my_question["D"],
                                    "answer":   my_question["answer"] }
    return res