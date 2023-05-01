import db_cmd
import ast


LIST_ORDER = [24527,
24459,
24450,
24361,
24279,
24236,
24158,
24138,
24038,
24034,
23845,
23822,
23746,
23691,
23668,
23564,
23424,
23411,
23373,
23372,
23370,
23367,
23357,
23311,
23301,
23292,
23168]
# LIST_ORDER = range(4588, 4690) # 19
# LIST_ORDER = range(4418, 4588) # 18
# LIST_ORDER = range(4254, 4418) # 17
# LIST_ORDER = range(4131, 4254) # 16
# LIST_ORDER = range(3998, 4131) # 15
# LIST_ORDER = range(3887, 3998) # 14
# LIST_ORDER = range(3776, 3887) # 13

fff = open('jvd5.txt', 'w', encoding='utf-8')
fxf = []
all_cur = 0
all_money = 0
all_s = 0
data_l = []
fffx = 0
all_pm = 0
all_text = ""
UID = 814657552
for elx in LIST_ORDER:
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
        pm = db_cmd.get_finance_deals_by_id_and_user(elx, UID)[3]
        all_text += f'Менеджер: @{db_cmd.get_user_data(db_cmd.get_order_by_order_id(elx)[2])[1]} | Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + \
            "Общая цена товара " + str(s) + " Прибыль " + \
            str(round(int(money) - s - cur, 2)) + " Прибыль менеджера " + str(pm) + "\n\n"
        all_cur += cur
        all_money += int(money)
        all_s += s
        all_pm += float(pm)
      except Exception as e:
        print(e)
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
      pm = db_cmd.get_finance_deals_by_id_and_user(elx, UID)[3]
      all_text += f'Менеджер: @{db_cmd.get_user_data(db_cmd.get_order_by_order_id(elx)[2])[1]} | Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + \
          "Общая цена товара " + str(s) + " Прибыль " + \
          str(round(money - s - cur, 2)) + " Прибыль менеджера " + str(pm) + "\n\n"
      all_cur += cur
      all_money += money
      all_s += s
      all_pm += float(pm)
    else:
      dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
      try:
          cur = dd["courier"]
      except:
          cur = 0
      all_cur += cur
      pm = db_cmd.get_finance_deals_by_id_and_user(elx, UID)[3]
      all_pm += float(pm)
      all_text += f'Менеджер: @{db_cmd.get_user_data(db_cmd.get_order_by_order_id(elx)[2])[1]} | Номер заказа ' + str(elx) + " Курьер = " + str(cur) + " Прибыль " + str(-cur) + " Прибыль менеджера " + str(pm) + "\n\n"
  
  except Exception as e:
    print(e, elx)

all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
      all_money) + " Общая цена товара за все заказы " + str(all_s) + " Прибыль " + str(all_money - all_s - all_cur) + " Прибыль менеджера(вся) " + str(all_pm) + "\n\n"
for y in data_l:
  all_text += f'{y[1]} {y[2]} - {y[0]} грамм\n'
  all_text += f'Стоимость {float(y[0]) * float(y[2])}\n'
print(all_text)
fff.write(all_text)
fff.close()
