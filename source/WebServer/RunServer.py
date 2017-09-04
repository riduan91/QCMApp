#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request
app = Flask(__name__)

SOURCE_DIR = "../"
import sys
sys.path.append(SOURCE_DIR)
import Group, Current

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
        res1 = Group.fetchGroups(parameters["series"])        
        return render_template("admin_group_information.html", result = (len(res1), res1, parameters["series"]))
        

@app.route("/view_meta", methods = ['POST'])
def view_meta():
    if request.method == 'POST':
        parameters = request.form
        res1 = Group.fetchGroups(parameters["series"])    
        return render_template("admin_group_information.html", result = (len(res1), res1, parameters["series"]))


#---------------------PREPARATION-QUESTION---------------------

@app.route("/send_questions", methods = ['POST'])
def send_questions():
    if request.method == 'POST':
        parameters = request.form
        res1 = Group.fetchGroups(parameters["series"])
        Group.updateQuestions(parameters["series"], parameters)
        res2 = Group.fetchQuestions(parameters["series"])
        #res = parameters
        return render_template("admin_question_information.html", result = (len(res1), res1, res2, parameters["series"]))

@app.route("/view_general", methods = ['GET'])
def view_general():
    res = Group.getSeries();
    return render_template("admin_all_series.html", result = res)


@app.route("/view_questions", methods = ['POST'])
def view_questions():
    if request.method == 'POST':
        parameters = request.form
        res1 = Group.fetchGroups(parameters["series"])   
        res2 = Group.fetchQuestions(parameters["series"])    
        return render_template("admin_question_information.html", result = (len(res1), res1, res2, parameters["series"]))


#---------------------ADMIN-START---------------------

@app.route("/admin_start", methods = ['GET', 'POST'])
def admin_start():
    if request.method == 'POST':
        parameters = request.form
        series = parameters["series"]
        res1 = Group.getSeries();
        
        Current.updateCurrentSeriesName(series)
        Current.updateCurrentGroup(0)
        Current.updateCurrentPlayers(parameters["players"])        
        
        res2 = Current.fetchCurrent()
        return render_template("admin_start.html", result = (res1, res2))
    else:
        res1 = Group.getSeries();
        res2 = Current.fetchCurrent()
        return render_template("admin_start.html", result = (res1, res2))


HOST = '0.0.0.0'
PORT = 8803

if __name__ == '__main__':
    app.run(host = HOST, port = PORT , debug=True)