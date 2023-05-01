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

msg = bot.send_message(649899870, "השלם את ההזמנה אם כבר סיימת אותה")
db_cmd.add_to_dlt_list(649899870, msg.message_id)