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

def close(xxx, ooii, mng_id):
	cid = xxx
	uid = xxx
	text_cnf = dopf.readJs("text.json")
	data = db_cmd.get_user_data(uid)
	if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
	    order_id = ooii
	    config = dopf.readJs()
	    data_order = db_cmd.get_order_by_order_id(order_id)
	    if uid == data_order[7]:
	        if data[6] == 8:
	            cidx = config["telegram"]["сourier_channel"]
	            type = 12
	        else:
	            cidx = config["telegram"]["pickup_channel"]
	            type = 22
	        data_orderx = ast.literal_eval(data_order[5])
	        grm = 0
	        for product in data_orderx["product"]:
	            if product[1] != "שקל":
	                grm += product[0]
	        try:
	            if grm <= 60:
	                data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[2]
	            else:
	                data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[3]
	        except:
	            data_orderx["courier"] = 0
	        chx = True
	        try:
	            if "correct_product" in data_orderx:
	                if not dopf.conformity(data_orderx["product"], data_orderx["correct_product"]):
	                    data_orderx["correct_product"], chx = dopf.calibration(
	                        data_orderx["product"], data_order[7])
	                    print(1)
	            else:
	                data_orderx["correct_product"], chx = dopf.calibration(
	                    data_orderx["product"], data_order[7])
	        except Exception as e:
	            print(e)
	            data_orderx["correct_product"], chx = dopf.calibration(
	                data_orderx["product"], data_order[7])
	        if dopf.check_cur_and_order(data_orderx["correct_product"], ast.literal_eval(db_cmd.get_user_data(uid)[5])["product"]) and chx:
	            if type == 12:
	                print(text_cnf["order_confirm_all2"].format(
	                                             data_orderx["courier"]))
	            else:
	                print(text_cnf["order_confirm_all"].format(
	                                             data_orderx["courier"]))
	            db_cmd.update_order(order_id, 'status_order', 3)
	            db_cmd.update_order(order_id, 'data', str(data_orderx))
	            db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
	            dopf.take_courier_and_storage(db_cmd.get_order_by_order_id(order_id))
	            dopf.update_price()
	            if data_order[4] in [33, 38]:
	                dopf.take_courier_and_storage2(db_cmd.get_order_by_order_id(order_id))
	                dopf.update_price()
	            text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
                bot.send_message(chat_id=mng_id, text=text_cnf["complete_order_confirm"], reply_markup=markup.main_sm())
	            bot.edit_message_caption(chat_id=cidx,
	                                     message_id=data_order[1],
	                                     caption=text,
	                                     parse_mode=None,
	                                     reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))
            else:
                bot.send_message(mng_id, text=text_cnf["no_products_curier"], reply_markup=markup.main_sm())
close(1311769743, 17742)