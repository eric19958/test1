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

config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])
while True:
    for i in [1388086076]:
        msg = bot.send_message(i, "אם אתה לא תסגור אתה קנוס 300 דולר עבודה של מתכנת ‼️")
        db_cmd.add_to_dlt_list(i, msg.message_id)
    time.sleep(10)