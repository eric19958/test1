#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json
import ast
import time
import db_cmd
import markup
import datetime
from datetime import timedelta
import logging
import dopf
import threading

config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])
TEXT = """*12 המחסומים שיוצבו הערב ובכל ערב מ-19:00 עד חצות בכבישים הבין



כביש 65 צומת נחל חדרה

מרכז: 

יש מחסום ביציאה מפת לכביש 5 איפה שדרך אם המושבות וגם בדרך אם המושבות בכניסה לפת יש מחסום בודקים

כביש 2 מחלף ינאי.
כביש 1 מחלף חמד.
כביש 431 מחלף ראשונים.
כביש 5 מחלף גלילות.

דרום:

כביש 4 מחלף אשדוד."""


cur = db_cmd.get_user_data_by_role(8)
pickup = db_cmd.get_user_data_by_role(9)
for i in cur:
	bot.send_message(i[0], TEXT)