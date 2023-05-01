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

orders = [24184]
cidx = -1001146969799
for order_id in orders:
    data = db_cmd.get_order_warehouse_by_id(order_id)
    if data[3] == 6:
        text = dopf.get_text_by_warehouse_order_next3(
            db_cmd.get_order_warehouse_by_id(order_id))
        try:
            bot.edit_message_text(
                chat_id=cidx, message_id=data[1], text=text, parse_mode=None, reply_markup=None)
        except:
            print(1)
    elif data[3] == 3:
        text2 = dopf.get_text_by_warehouse_order_next2(
            db_cmd.get_order_warehouse_by_id(order_id))
        bot.edit_message_text(
            chat_id=cidx, message_id=data[1], text=text2, parse_mode=None, reply_markup=None)
