import json
import dopf
import ast
import time
import db_cmd
import markup
from datetime import datetime
from datetime import timedelta
import telebot

config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])

while True:
    orders = db_cmd.get_all_confirm_no_start_order()
    for x in db_cmd.get_user_data_by_role(12):
        top_cur_id = x[0]
        text_cnf = dopf.readJs("text.json")
        for order in orders:
            d1 = datetime.strptime(order[8], '%Y-%m-%d %H:%M:%S.%f')
            d2 = datetime.now() - timedelta(minutes=3)
            print(d1, d2)
            if d2 >= d1:
                print(order)
                config = dopf.readJs()
                if order[4] in [12, 33]:
                    chat_order = config["telegram"]["сourier_channel"]
                    url_order = f'https://t.me/c/{str(chat_order)[4:]}/{order[1]}'
                    text = text_cnf["wait_order_top_cur"].format(url_order)
                    bot.send_message(chat_id=top_cur_id ,text=text)
    for x in db_cmd.get_user_data_by_role(17):
        top_cur_id = x[0]
        text_cnf = dopf.readJs("text.json")
        for order in orders:
            d1 = datetime.strptime(order[8], '%Y-%m-%d %H:%M:%S.%f')
            d2 = datetime.now() - timedelta(minutes=3)
            print(d1, d2)
            if d2 >= d1:
                config = dopf.readJs()
                if order[4] in [22, 38]:
                    chat_order = config["telegram"]["pickup_channel"]
                    url_order = f'https://t.me/c/{str(chat_order)[4:]}/{order[1]}'
                    text = text_cnf["wait_order_top_cur"].format(url_order)
                    bot.send_message(chat_id=top_cur_id ,text=text)
    print('yes')
    ordersx = db_cmd.get_all_confirm_no_confirm_order()
    time.sleep(120)
