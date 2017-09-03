#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request
app = Flask(__name__)

SOURCE_DIR = "../"
import sys
sys.path.append(SOURCE_DIR)
import Group

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/new_meta", methods = ['POST', 'GET'])
def new_meta():
    return render_template("admin_preparation.html")

@app.route("/send_meta", methods = ['POST', 'GET'])
def send_meta():
    if request.method == 'POST':
        parameters = request.form
        Group.updateGroups(parameters)
        res = Group.fetchGroups()
        
        return render_template("admin_preparation_question.html", result = (len(res), res))
    else:
        return render_template("admin_preparation.html")

@app.route("/send_questions", methods = ['POST', 'GET'])
def send_questions():
    if request.method == 'POST':
        parameters = request.form
        res1 = Group.fetchGroups()
        Group.updateQuestions(parameters)
        res2 = Group.fetchQuestions()
        #res = parameters
        return render_template("admin_question_information.html", result = (len(res1), res1, res2))
    else:
        res1 = Group.fetchGroups()
        res2 = Group.fetchQuestions()
        return render_template("admin_question_information.html")

@app.route("/view_meta", methods = ['POST', 'GET'])
def view_meta():
    if request.method == 'POST':
        parameters = request.form
        Group.updateGroups(parameters)
        res = Group.fetchGroups()
        
        return render_template("admin_get_info_group.html", result = (len(res), res))
    else:
        res = Group.fetchGroups()
        return render_template("admin_get_info_group.html", result = (len(res), res))

HOST = '0.0.0.0'
PORT = 8803

if __name__ == '__main__':
    app.run(host = HOST, port = PORT , debug=True)