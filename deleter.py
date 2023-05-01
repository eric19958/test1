import telebot
import json
import time
import db_cmd
import datetime
import logging
import dopf

config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])

while True:
    now = datetime.datetime.now()
    unixtime = int(time.mktime(now.timetuple()))
    data = db_cmd.get_all_dlt_list(unixtime - 240)
    for msg in data:
        try:
            bot.delete_message(msg[1], msg[2])
        except:
            pass
        db_cmd.dlt_in_dlt_list(msg[0])
    time.sleep(4)
