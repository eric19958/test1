import db_cmd
import ast


LIST_ORDER = list(range(23982, 24950))

fxf = []
all_cur = 0
all_money = 0
all_s = 0
data_l = []
fffx = 0
all_text = ""
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
                all_text += 'Номер заказа ' + str(elx) + ' Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + \
                    "Общая цена товара " + str(s) + " Прибыль " + \
                    str(round(int(money) - s - cur, 2)) + "\n\n"
                all_cur += cur
                all_money += int(money)
                all_s += s
            except:
                pass
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
            all_text += 'Номер заказа ' + str(elx) + " Курьер = " + \
                str(cur) + " Прибыль " + str(-cur) + "\n\n"

    except Exception as e:
        pass
        #print(e, elx)
all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
    all_money) + " Общая цена товара за все заказы " + str(all_s) + " Прибыль " + str(all_money - all_s - all_cur) + "\n\n"
rez = 0
for y in data_l:
    product_data = db_cmd.get_product_by_name(y[1])
    product_id = product_data[0]
    product_data_refill = db_cmd.get_product_refill_active_next(product_id)
    for ref in product_data_refill:
        if float(ref[5]) + float(ref[6]) == float(y[2]):
            x = ref[5]
            z = ref[6]
            break
    all_text += f'{y[1]} {y[2]} - {y[0]} грамм\n'
    all_text += f'Стоимость {float(y[0]) * float(y[2])}, Себестоимость {float(y[0]) * float(x)},  Резерв {float(y[0]) * float(z)}\n'
    rez += float(y[0]) * float(z)


all_text += f'\nОбщий резерв {rez} \n'
print(all_text)
