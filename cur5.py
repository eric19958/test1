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
import time



curxx = [1428158343]
alls = 0
for k in range(0, 30):
  allttt = ""
  summxa = 0
  nowx2= datetime.datetime.now() - timedelta(days=k)
  print(nowx2.strftime('%d.%m.%Y'))
  print()
  for cur_id in curxx:
    sumx = 0
    # k = 1
    for ij in range(k, k+1):
      # date_order < now + timedelta(hours=24) and date_order > now + timedelta(hours=10)
      fxf = []
      all_cur = 0
      all_money = 0
      all_s = 0
      data_l = []
      fffx = 0
      all_text = ""
      list_order = db_cmd.get_last200_order_cur(cur_id)
      nowx = datetime.datetime.now() - timedelta(days=ij)
      now = datetime.datetime.combine(
          datetime.date.today(), datetime.datetime.min.time()) - timedelta(days=ij)
      if nowx > now + timedelta(hours=9):
        now = now + timedelta(days=1)
      for eltt in list_order:
        elx = eltt[0]
        time = db_cmd.get_order_by_order_id(elx)[8]
        date_order = datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S.%f')
        if date_order < now + timedelta(hours=9) and date_order > now - timedelta(hours=15):
          try:
            if db_cmd.get_order_by_order_id(elx)[3] == 3 and db_cmd.get_order_by_order_id(elx)[4] < 30:
              dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
              try:
                cur = dd["courier"]
              except:
                cur = 0
              try:
                mx = dd["money"].replace(",", "")
                money = mx
                if float(money) < 0:
                  money = -float(money)
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
                all_cur += cur
                all_money += int(money)
                all_s += s
              except:
                print(2)
                print(db_cmd.get_order_by_order_id(elx))
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
              for el in dd["true_product"]:
                if el[1] != "שקל":
                  pricexx = el[2]
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
          except Exception as e:
            print(e, elx)

      # print(all_text)
      sumx += (all_money - all_cur)
      summxa += sumx
    if sumx != 0:
        print(f"@{db_cmd.get_user_data(cur_id)[1]} | Должен сдать: {sumx} | ЗП: {all_cur} | Всего: {all_money}")
    #print(sumx, db_cmd.get_user_data(cur_id)[1], all_money, all_cur)
  print()
  print(f"Всего: {summxa}")
  alls += summxa
  print()
  print('# --------- #')
print()
print(f"Должны сдать за неделю: {alls}")