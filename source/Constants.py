# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 16:11:33 2017

@author: ndoannguyen
"""

AUTONEXT = 1
ADMINCLICK = 0

UNTIL_FASTEST = 0
UNTIL_RIGHT_AND_FASTEST = 1
ALL = 2

DBNAME = "QCM";
GROUP_SUFFIX = "group";
QUESTION_SUFFIX = "question";
PLAYER_SUFFIX = "player";
CURRENT = "Current";

RESET = 0
START_G = 1
ACTIVE_Q = 2
WAITING_Q = 3
END_G = 4
END = 5 

NO_ANSWER = -2


def convertInt(s):
    try:
        return int(s)
    except ValueError:
        return s
