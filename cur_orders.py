import db_cmd
import ast

CUR_ID = 1388086076


fff = open('jvd5.txt', 'w', encoding='utf-8')
fxf = []
all_cur = 0
all_money = 0
all_s = 0
data_l = []
fffx = 0
all_text = ""
list_order = db_cmd.get_last200_order_cur(CUR_ID)
now = datetime.datetime.combine(
            datetime.date.today(), datetime.datetime.min.time())
for elx in list_order:
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
          all_text += 'Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur)
          str(round(int(money) - s - cur, 2)) + "\n\n"
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
        for el in dd["product2"]:
          if el[1] != "שקל":
            ff = 0
            try:
              old_order_data = db_cmd.get_order_by_order_id(dd["order_id"])
              old_order_data_correct = ast.literal_eval(old_order_data[5])['correct_product']
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

        all_text += 'Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur)
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
        all_text += 'Номер заказа ' + str(elx) + " Курьер = " + str(cur) + " Прибыль " + str(-cur) + "\n\n"
  
    except Exception as e:
  print(e, elx)
all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
      all_money)

print(all_text)
fff.write(all_text)
fff.close()
