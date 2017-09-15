#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/delete_collection", methods = ['POST'])
def delete_collection():
    if request.method == 'POST':
        parameters = request.form
        current_series = parameters["series"]
        Group.dropGroupCollection(current_series)
        Question.dropQuestionCollection(current_series)
        Player.dropPlayerCollection(current_series)
        series = Group.getSeries()
        return render_template("admin_all_series.html", result = series)

#---------------------ADMIN-START---------------------

@app.route("/admin_start", methods = ['GET', 'POST'])
def admin_start():
    if request.method == 'POST':
        parameters = request.form
        series = parameters["series"]
        series_list = Group.getSeries()
        
        Current.updateCurrentSeriesName(series)
        Current.updateCurrentGroup(0)
        Current.updateCurrentPlayers(parameters["players"])
        
        groups = Group.fetchGroups(parameters["series"]) 
        Current.updateCurrentNbGroups(len(groups))
        
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
    players = Player.fetchAllPlayers(current)
    if current["status"] == Constants.START_G and current["group"] > 0 and group["group_nb_players_max"] > 0:
        player_name_strings = ",".join([ players[i]["_id"] for i in range(len(players)) if i < group["group_nb_players_max"] ])
    else:
        player_name_strings = ",".join([ pl["_id"] for pl in players])
    ttmp = time.time()*1000
    time_to_display = -1
    if current["status"] == Constants.ACTIVE_Q and question["question_duration"] > 0:
        time_to_display = min(max(round(question['question_start_timestamp']/1000 + question['question_duration'] - ttmp/1000, 2), 0), question['question_duration'])
        if int(time_to_display) == 0:
            Current.updateCurrentStatus(Constants.WAITING_Q)
    if current["status"] == Constants.ACTIVE_Q and question["question_duration"] <= 0:
        Current.updateCurrentStatus(Constants.WAITING_Q)
    return render_template("admin_games.html", result = (current, series, group, question, players, Constants.ALPHABET, time_to_display, player_name_strings))

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
        return redirect(url_for('admin_games'))
    else:
        return redirect(url_for('admin_games'))

@app.route("/admin_start_question", methods = ['GET', 'POST'])
def admin_start_question():
    # START G --> ACTIVE Q
    # WAITING Q --> ACTIVE Q
    if request.method == "POST":
        parameters = request.form
        question_index = int(parameters["next_question_index"])
        Current.updateCurrentQuestion(question_index)
        current = Current.fetchCurrent()
        timestamp = int(time.time()*1000) + 2000
        Current.updateQuestionTimestamp(current, timestamp)
        Current.activateQuestion(current)
        if question_index == 0:
            Current.updateGroupTimestamp(current, timestamp)
        Current.updateCurrentStatus(Constants.ACTIVE_Q)
        return redirect(url_for('admin_games'))
    else:
        return redirect(url_for('admin_games'))

@app.route("/admin_waiting_question", methods = ['GET', 'POST'])
def admin_waiting_question():
    # ACTIVE Q --> WAITING Q
    if request.method == "POST":
        Current.updateCurrentStatus(Constants.WAITING_Q)
        return redirect(url_for('admin_games'))
    else:
        return redirect(url_for('admin_games'))

@app.route("/admin_end_group", methods = ['GET', 'POST'])
def admin_end_group():
    # ACTIVE Q --> WAITING Q
    if request.method == "POST":
        Current.updateCurrentStatus(Constants.END_G)
        return redirect(url_for('admin_games'))
    else:
        return redirect(url_for('admin_games'))

@app.route("/admin_reset", methods = ['GET', 'POST'])
def admin_reset():
    if request.method == 'POST':
        current = Current.fetchCurrent()
        series = current["series"]
        series_list = Group.getSeries()
        players = ",".join(Current["players"])
        Current.updateCurrentSeriesName(series)
        Current.updateCurrentGroup(0)
        Current.updateCurrentPlayers(players)
        
        Player.updatePlayers(series, players)
        
        current = Current.fetchCurrent()
        return render_template("admin_start.html", result = (series_list, current))
    else:
        series_list = Group.getSeries();
        current = Current.fetchCurrent()
        return render_template("admin_start.html", result = (series_list, current))

@app.route("/admin_partial_reset", methods = ['GET', 'POST'])
def admin_partial_reset():
    if request.method == 'POST':
        current = Current.fetchCurrent()
        current_players = current["players"]
        
        parameters = request.form
        players = parameters["players"]
        Current.updateCurrentPlayers(players)

        Player.updatePartialPlayers(current, players, current_players)
        
        current = Current.fetchCurrent()
        return redirect(url_for('admin_games'))
    else:
        return redirect(url_for('admin_games'))

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
        players = Player.fetchAllPlayers(current)
        ttmp = time.time()*1000
        time_to_display = -1
        if current["status"] == Constants.ACTIVE_Q and question["question_duration"] > 0:
            time_to_display = min(max(round(question['question_start_timestamp']/1000 + question['question_duration'] - ttmp/1000, 2), 0), question['question_duration'])
        if len(player) > 0:
            return render_template("player_games.html", result = (current, series, group, question, players, Constants.ALPHABET, time_to_display, player))
        else:
            render_template("player_login.html", result = 1)
    else:
        return render_template("player_login.html", result = 1)

@app.route("/player_login", methods = ['GET', 'POST'])
def player_login():
    return render_template("player_login.html", result = 1)

@app.route("/player_choose_star", methods = ['GET', 'POST'])
def player_choose_star():
    if request.method == "POST":
        parameters = request.form
        player_name = request.cookies["player_name"]    
        star_chosen = int(parameters["star_chosen"])
        current = Current.fetchCurrent()
        Player.updateStarChosen(current, player_name, star_chosen)
        return redirect(url_for('player_games'))
    else:
        return redirect(url_for('player_games'))

@app.route("/player_answer", methods = ['GET', 'POST'])
def player_answer():
    if request.method == "POST":
        parameters = request.form
        player_name = request.cookies["player_name"]
        current = Current.fetchCurrent()
        answer = int(parameters["answer"])
        current = Current.fetchCurrent()
        timestamp = int(time.time()*1000)
        Player.answer(current, player_name, answer, timestamp)
        return redirect(url_for('player_games'))
    else:
        return redirect(url_for('player_games'))

HOST = '0.0.0.0'
PORT = 8803

if __name__ == '__main__':
    app.run(host = HOST, port = PORT , debug = True)