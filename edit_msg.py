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

order_id = 4930
config = dopf.readJs()
data_order = db_cmd.get_order_by_order_id(order_id)
uid = data_order[7]
data = db_cmd.get_user_data(uid)
if data[6] == 8:
    cidx = config["telegram"]["сourier_channel"]
    type = 12
else:
    cidx = config["telegram"]["pickup_channel"]
    type = 22
data_orderx = ast.literal_eval(data_order[5])
text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
bot.edit_message_caption(chat_id=cidx,
                         message_id=data_order[1],
                         caption=text,
                         parse_mode=None,
                         reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))