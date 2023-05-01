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

uid = 1029486756
text_cnf = dopf.readJs("text.json")
config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])
data = db_cmd.get_user_data(uid)
datax = ast.literal_eval(data[4])
order_id = datax["active"]
dataxx = datax["true_order"]
data_order = db_cmd.get_order_warehouse_by_id(order_id)
dataf = ast.literal_eval(data_order[4])
dataf["true_product"] = dataxx
flag = 0
if 'order_id' in dataf:
    orderx_data = ast.literal_eval(db_cmd.get_order_by_order_id(dataf["order_id"])[5])
    for i in orderx_data["true_product"]:
        if i[1] == "שקל":
            dataxx.append(i)
            break
    orderx_data["true_product"] = dataxx
    orderx_data["stk"] = 1
    db_cmd.update_order(dataf["order_id"], 'data', str(orderx_data))
    flag = 1
true_now = []
for prx in dataf["true_product"]:
    if prx[1] != "שקל":
        true_now.append(prx)
dataf["true_product"] = true_now
db_cmd.update_order_w(order_id, 'data', str(dataf))
db_cmd.update_order_w(order_id, 'status_order', 6)
config = dopf.readJs()
cidx = config["telegram"]["warehouse_channel"]
db_cmd.update_user(uid, "state", 0)
dataxxx = ast.literal_eval(db_cmd.get_order_warehouse_by_id(order_id)[4])
summx, rez = dopf.eqal2(dataxxx["product"], dataxxx["true_product"])
###
if flag == 0 and summx >= 50:
    cur_id = data_order[2]
    text_ff = text_cnf["cur_penalty"].format(db_cmd.get_user_data(cur_id)[1], order_id, str(cidx)[
                                             4:], data_order[1], round(float(summx), 2))
    db_cmd.update_bank(
        cur_id, round(float(db_cmd.get_user_bank(cur_id)[1]), 2) - round(float(summx), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=cur_id, money=-round(float(summx), 2))
    db_cmd.update_bank(
        0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(summx - rez), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=0, money=round(float(summx - rez), 2), payer_id=cur_id)
    db_cmd.update_bank(
        1, round(float(db_cmd.get_user_bank(1)[1]), 2) + round(float(rez), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=1, money=round(float(rez), 2), payer_id=cur_id)
    bot.send_message(config["telegram"]["penalties_channel"], text=text_ff)
elif flag == 0 and summx > 0 and summx < 50:
    cur_id = data_order[2]
    text_ff = text_cnf["cur_penalty2"].format(db_cmd.get_user_data(cur_id)[1], order_id, str(cidx)[
                                             4:], data_order[1], round(float(summx), 2))
    db_cmd.update_bank(
        cur_id, round(float(db_cmd.get_user_bank(1)[1]), 2) - round(float(summx), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=1, money=-round(float(summx), 2))
    db_cmd.update_bank(
        0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(summx - rez), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=0, money=round(float(summx - rez), 2), payer_id=1)
    db_cmd.update_bank(
        1, round(float(db_cmd.get_user_bank(1)[1]), 2) + round(float(rez), 2))
    db_cmd.add_financial_operation(
        id_order=-int(order_id), user_id=1, money=round(float(rez), 2), payer_id=1)
    bot.send_message(config["telegram"]["penalties_channel"], text=text_ff)
###
dopf.take_courier_and_storage_cur_fx(dataxxx, data_order[2])
dopf.update_price()
dopf.add_warehouse(dataxxx["true_product"])
dopf.update_price()
text = dopf.get_text_by_warehouse_order_next3(
    db_cmd.get_order_warehouse_by_id(order_id))
bot.edit_message_text(chat_id=cidx,
                      message_id=data_order[1],
                      text=text,
                      parse_mode=None,
                      reply_markup=None)