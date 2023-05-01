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
FFX = [1282013231]
for rrr in FFX:
    for i in range(7):
        bot.send_message(871500685, text=f"{i+13}.12.2020")
        UIDXX = [rrr]
        for uid in UIDXX:
            now = datetime.datetime.combine(
                datetime.date.today(), datetime.datetime.min.time())- timedelta(days=8 - i)
            datax = db_cmd.get_financial_operation_by_user_last(uid)
            list_xxx = []
            for operation in datax:
                orderx = db_cmd.get_order_by_order_id(operation[1])
                date_operation = datetime.datetime.strptime(
                    orderx[8], '%Y-%m-%d %H:%M:%S.%f')
                if date_operation < now + timedelta(hours=9) and date_operation > now - timedelta(hours=15) and operation[1] != -1:
                    list_xxx.append(operation[1])
            fff = open(f'{uid}.txt', 'w', encoding='utf-8')
            all_cur = 0
            all_money = 0
            all_s = 0
            data_l = []
            all_text = f"{i+13}.12.2020  @{db_cmd.get_user_data(uid)[1]}\n\n"
            for elx in list_xxx:
                if db_cmd.get_order_by_order_id(elx)[3] == 3 and db_cmd.get_order_by_order_id(elx)[4] < 30:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    try:
                        money = dd["money"]
                        if float(money) < 0:
                            money = str(int(money) * -1)
                        text = ""
                        s = 0
                        for el in dd["correct_product"]:
                            s += float(el[0]) * float(el[2])
                            text += f"{el[0]} x {el[2]} = {float(el[0])*float(el[2])}  {el[1]}\n"
                            f = 0
                            for x in range(len(data_l)):
                                if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
                                    data_l[x][0] += el[0]
                                    f = 1
                                    break
                            if f == 0:
                                data_l.append(el)
                        all_text += 'Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + "Общая цена товара " + str(
                            s) + " Прибыль " + str(round(int(money) - s - cur, 2)) + "\n\n"
                        all_cur += cur
                        all_money += int(money)
                        all_s += s
                    except Exception as e:
                        print(e, elx)
                elif db_cmd.get_order_by_order_id(elx)[3] == 3 and db_cmd.get_order_by_order_id(elx)[4] > 30:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    text = ""
                    s = 0
                    money = 0
                    for el in dd["correct_product"]:
                        if el[1] != "שקל":
                            s += float(el[0]) * float(el[2])
                            text += f"{el[0]} x {el[2]} = {float(el[0])*float(el[2])}  {el[1]}\n"
                            f = 0
                            for x in range(len(data_l)):
                                if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
                                    data_l[x][0] += el[0]
                                    f = 1
                                    break
                            if f == 0:
                                data_l.append(el)
                        else:
                            money -= int(el[0])
                        for el in dd["product2"]:
                            if el[1] != "שקל":
                                ff = 0
                                try:
                                    old_order_data = db_cmd.get_order_by_order_id(
                                        dd["order_id"])
                                    old_order_data_correct = ast.literal_eval(
                                        old_order_data[5])['correct_product']
                                    for elll in old_order_data_correct:
                                        if elll[1] == el[1]:
                                            pricexx = elll[2]
                                            ff = 1
                                            break
                                except:
                                    pass
                                if ff == 0:
                                    pricexx = db_cmd.get_product_by_name(el[1])[2]
                                s -= float(el[0]) * float(pricexx)
                                text += f"- {el[0]} x {pricexx} = -{float(el[0]) * float(pricexx)}  {el[1]}\n"
                                f = 0
                                for x in range(len(data_l)):
                                    if data_l[x][1] == el[1] and data_l[x][2] == pricexx:
                                        data_l[x][0] -= el[0]
                                        f = 1
                                        break
                                if f == 0:
                                    data_l.append(
                                        [-1 * el[0], el[1], pricexx])
                            else:
                                money += int(el[0])

                        all_text += 'Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + \
                            "Общая цена товара " + str(s) + " Прибыль " + \
                            str(round(money - s - cur, 2)) + "\n\n"
                        all_cur += cur
                        all_money += money
                        all_s += s
                else:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    all_cur += cur
                    all_text += 'Номер заказа ' + \
                        str(elx) + " Курьер = " + str(cur) + \
                        " Прибыль " + str(-cur) + "\n\n"

            all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
                all_money) + " Общая цена товара за все заказы " + str(all_s) + " Прибыль " + str(all_money - all_s - all_cur) + "\n\n"

            for y in data_l:
                all_text += f'{y[1]} {y[2]} - {y[0]} грамм\n'
                all_text += f'Стоимость {float(y[0]) * float(y[2])}\n'

            # print(all_text)
            fff.write(all_text)
            fff.close()
            # doc = open('/tmp/file.txt', 'rb')
            fff = open(f'{uid}.txt', 'rb')
            bot.send_document(
                871500685, fff, caption=f"@{db_cmd.get_user_data(uid)[1]}")
            fff.close()
