#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request
app = Flask(__name__)

SOURCE_DIR = "../"
import sys
sys.path.append(SOURCE_DIR)
import Group, Question, Current, Player, Constants
import time

#############INDEX######################

@app.route("/")
def index():
    return render_template("index.html")
    

#---------------------PREPARATION-META---------------------

@app.route("/new_meta", methods = ['POST', 'GET'])
def new_meta():
    return render_template("admin_preparation.html")

@app.route("/send_meta", methods = ['POST', 'GET'])
def send_meta():
    if request.method == 'POST':
        parameters = request.form
        if " " in parameters["series"]:
            return render_template("admin_preparation.html")
        Group.updateGroups(parameters)
        res = Group.fetchGroups(parameters["series"])
        
        return render_template("admin_preparation_question.html", result = (len(res), res, parameters["series"]))
    else:
        return render_template("admin_preparation.html")
        
@app.route("/update_meta", methods = ['POST'])
def update_meta():
    if request.method == 'POST':
        parameters = request.form
        Group.updateGroups(parameters)
        groups = Group.fetchGroups(parameters["series"])        
        return render_template("admin_group_information.html", result = (len(groups), groups, parameters["series"]))
        

@app.route("/view_meta", methods = ['POST'])
def view_meta():
    if request.method == 'POST':
        parameters = request.form
        groups = Group.fetchGroups(parameters["series"])    
        return render_template("admin_group_information.html", result = (len(groups), groups, parameters["series"]))


#---------------------PREPARATION-QUESTION---------------------

@app.route("/send_questions", methods = ['POST'])
def send_questions():
    if request.method == 'POST':
        parameters = request.form
        groups = Group.fetchGroups(parameters["series"])
        Question.updateQuestions(parameters["series"], parameters)
        questions = Question.fetchQuestions(parameters["series"])
        #res = parameters
        return render_template("admin_question_information.html", result = (len(groups), groups, questions, parameters["series"]))

@app.route("/view_general", methods = ['GET'])
def view_general():
    series = Group.getSeries();
    return render_template("admin_all_series.html", result = series)


@app.route("/view_questions", methods = ['POST'])
def view_questions():
    if request.method == 'POST':
        parameters = request.form
        groups = Group.fetchGroups(parameters["series"])   
        questions = Question.fetchQuestions(parameters["series"])    
        return render_template("admin_question_information.html", result = (len(groups), groups, questions, parameters["series"]))


#---------------------ADMIN-START---------------------

@app.route("/admin_start", methods = ['GET', 'POST'])
def admin_start():
    if request.method == 'POST':
        parameters = request.form
        series = parameters["series"]
        series_list = Group.getSeries();
        
        Current.updateCurrentSeriesName(series)
        Current.updateCurrentGroup(0)
        Current.updateCurrentPlayers(parameters["players"])
        
        Player.updatePlayers(series, parameters["players"])
        
        current = Current.fetchCurrent()
        return render_template("admin_start.html", result = (series_list, current))
    else:
        series_list = Group.getSeries();
        current = Current.fetchCurrent()
        return render_template("admin_start.html", result = (series_list, current))

@app.route("/admin_game", methods = ['GET', 'POST'])
def admin_games():
    current = Current.fetchCurrent()
    series = current["series"]
    group = Current.fetchCurrentGroup(current)
    question = Current.fetchCurrentQuestion(current)
    return render_template("admin_games.html", result = (current, series, group, question))

@app.route("/admin_start_group", methods = ['GET', 'POST'])
def admin_start_group():
    # START --> START G
    # END G --> START G
    if request.method == "POST":
        parameters = request.form
        group_index = parameters["next_group_index"]
        Current.updateCurrentGroup(int(group_index))
        Current.updateCurrentQuestion(0)
        Current.updateCurrentStatus(Constants.START_G)
        return admin_games()
    else:
        return admin_games()

@app.route("/admin_start_question", methods = ['GET', 'POST'])
def admin_start_question():
    # START G --> ACTIVE Q
    # WAITING Q --> ACTIVE Q
    if request.method == "POST":
        parameters = request.form
        question_index = parameters["next_question_index"]
        Current.updateCurrentQuestion(int(question_index))
        current = Current.fetchCurrent()
        timestamp = int(time.time()*1000) + 1000
        Current.updateQuestionTimestamp(current, timestamp)
        Current.activateQuestion(current)
        if question_index == 0:
            Current.updateGroupTimestamp(current, timestamp)
        Current.updateCurrentStatus(Constants.ACTIVE_Q)
        return admin_games()
    else:
        return admin_games()

@app.route("/admin_waiting_question", methods = ['GET', 'POST'])
def admin_waiting_question():
    # ACTIVE Q --> WAITING Q
    if request.method == "POST":
        Current.updateCurrentStatus(Constants.WAITING_Q)
        return admin_games()
    else:
        return admin_games()

@app.route("/admin_end_group", methods = ['GET', 'POST'])
def admin_end_group():
    # ACTIVE Q --> WAITING Q
    if request.method == "POST":
        Current.updateCurrentStatus(Constants.END_G)
        return admin_games()
    else:
        return admin_games()

#---------------------ADMIN-START---------------------

@app.route("/player_games", methods = ['GET', 'POST'])
def player_games():
    if "player_name" in request.cookies.keys():
        player_name = request.cookies["player_name"]    
        current = Current.fetchCurrent()
        series = current["series"]
        group = Current.fetchCurrentGroup(current)
        question = Current.fetchCurrentQuestion(current)
        player = Player.fetchPlayer(series, player_name)
        return render_template("player_games.html", result = (current, series, group, question, player))
    else:
        return render_template("player_login.html", result = (current, series, group, question, player))

@app.route("/player_choose_star", methods = ['GET', 'POST'])
def player_choose_star():
    if request.method == "POST":
        parameters = request.form
        player_name = request.cookies["player_name"]    
        star_chosen = int(parameters["start_chosen"])
        current = Current.fetchCurrent()
        Player.updateStarChosen(current, player_name, star_chosen)
        return admin_games()
    else:
        return admin_games()

@app.route("/player_answer", methods = ['GET', 'POST'])
def player_answer():
    if request.method == "POST":
        parameters = request.form
        player_name = request.cookies["player_name"]    
        answer = int(parameters["answer"])
        current = Current.fetchCurrent()
        timestamp = int(time.time()*1000)
        Player.answer(current, player_name, answer, timestamp)
        return admin_games()
    else:
        return admin_games()

HOST = '0.0.0.0'
PORT = 8803

if __name__ == '__main__':
    app.run(host = HOST, port = PORT , debug=True)