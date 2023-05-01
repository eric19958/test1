import db_cmd
import ast
import dopf


LIST_ORDER = [55446,
55442,
55433,
55429,
55428,
55427,
55425,
55424,
55420,
55419,
55416,
55412,
55411,
55389,
55388,
55385,
55375,
55372,
55371,
55364,
55361,
55360,
55349,
55346,
55324,
55302,
55296,
55288,
55271,
55259,
55247,
55246,
55240,
55230,
55224,
55223,
55216,
55210,
55203,
55201,
55184,
55166,
55149,
55136,
55133,
55122,
55121,
55114,
55113,
55111,
55107,
55105,
55104,
55103,
55099,
55098,
55087,
55072,
55061,
55043,
55028,
55017,
55014,
55012,
55002,
55001,
54998,
54990,
54972,
54971,
54955,
54954,
54948,
54932,
54923,
54921,
54917,
54912,
54909,
54903,
54902,
54895,
54877,
54858,
54848,
54846,
54835,
54831,
54829,
54812,
54807,
54799,
54792,
54790,
54789,
54786,
54780,
54767,
54763,
54757,
54755,
54754,
54740,
54737,
54734,
54732,
54723,
54709,
54703,
54692,
54685,
54674,
54673,
54659,
54645,
54644,
54643,
54635,
54632,
54624,
54614,
54612,
54611,
54610,
54608,
54593,
54592,
54591,
54576,
54558,
54557,
54555,
54535,
54529,
54526,
54520,
54497,
54492,
54474,
54468,
54465,
54460,
54458,
54456,
54453,
54452,
54451,
54431,
54422,
54417,
54414,
54404,
54388,
54385,
54383,
54370,
54369,
54367,
54355,
54346,
54316,
54315,
54309,
54304,
54283,
54282,
54266,
54239,
54222,
54211,
54209,
54173,
54172,
54166,
54165,
54154,
54145,
54127,
54124,
54093,
54065]
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
            all_text += 'Номер заказа ' + str(elx) + " Курьер = " + \
                str(cur) + " Прибыль " + str(-cur) + "\n\n"

    except Exception as e:
        print(e, elx)
all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
    all_money) + " Общая цена товара за все заказы " + str(all_s) + " Прибыль " + str(all_money - all_s - all_cur) + "\n\n"
data_ff = []
for y in data_l:
    f = 0
    k = 0
    all_text += f'{y[1]} {y[2]} - {y[0]} грамм\n'
    all_text += f'Стоимость {float(y[0]) * float(y[2])}\n'
    for x in data_ff:
        if x[1] == y[1]:
            f = 1
            break
        k += 1
    if f == 1:
        data_ff[k][0] = data_ff[k][0] + float(y[0])
    else:
        data_ff.append([float(y[0]), y[1]])

print(all_text)
for i in data_ff:
    print(i[0], i[1])
