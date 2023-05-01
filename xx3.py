import dopf
import db_cmd
import ast


def plus(data, all_data):
    for el in data:
        check = True
        for el2 in all_data:
            if el[1] == el2[1]:
                el2[0] += el[0]
                check = False
        if check:
            all_data.append([el[0], el[1]])
    return all_data


def minus(data, all_data):
    for el in data:
        check = True
        for el2 in all_data:
            if el[1] == el2[1]:
                el2[0] -= el[0]
                check = False
        if check:
            all_data.append([- el[0], el[1]])
    return all_data


nowx = range(44858, 44921)
now = []

for i in nowx:
    try:
        data = db_cmd.get_order_warehouse_by_id(i)
        datax = ast.literal_eval(data[4])["product"]
        if data[3] == 3:
            now = plus(datax, now)
        elif data[3] == 6:
            now = minus(datax, now)
        #datax = ast.literal_eval(data[4])["true_product"]
        #now = minus(datax, now)
    except:
        pass

print(nowx)
for el in now:
    print(el[1], el[0])
