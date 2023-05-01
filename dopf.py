import json
import db_cmd
import logging
import ast
import datetime
from datetime import timedelta
import markup

logging.basicConfig(format='%(asctime)s | %(process)d-%(levelname)s-%(message)s',
                    level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')


def readJs(name="config.json"):
    with open(name, encoding='utf-8-sig') as order_file:
        return json.load(order_file)

def all_cur_report_day():
    cur_list = db_cmd.get_user_data_by_role(8)
    pickup_list = db_cmd.get_user_data_by_role(9)
    text_cnf = readJs("text.json")
    all_text = ""
    alls = 0
    for k in range(1, 2):
        summxa = 0
        for cur_tab in cur_list:
            cur_id = cur_tab[0]
            sumx = 0
            for ij in range(k, k+1):
                fxf = []
                all_cur = 0
                all_money = 0
                all_s = 0
                data_l = []
                fffx = 0
                list_order = db_cmd.get_last200_order_cur(cur_id)
                nowx = datetime.datetime.now() - timedelta(days=ij)
                now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) - timedelta(days=ij)
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
                                    all_cur += cur
                                    all_money += int(money)
                                except:
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
                                    if el[1] == "שקל":
                                        money -= int(el[0])
                                for el in dd["true_product"]:
                                    if el[1] == "שקל":
                                        money += int(el[0])
                                    all_cur += cur
                                    all_money += money
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
                all_text += text_cnf["day_report_all"].format(db_cmd.get_user_data(cur_id)[1], sumx, all_cur, all_money)
        for cur_tab in pickup_list:
            cur_id = cur_tab[0]
            sumx = 0
            for ij in range(k, k+1):
                fxf = []
                all_cur = 0
                all_money = 0
                all_s = 0
                data_l = []
                fffx = 0
                list_order = db_cmd.get_last200_order_cur(cur_id)
                nowx = datetime.datetime.now() - timedelta(days=ij)
                now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()) - timedelta(days=ij)
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
                                    all_cur += cur
                                    all_money += int(money)
                                except:
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
                                    if el[1] == "שקל":
                                        money -= int(el[0])
                                for el in dd["true_product"]:
                                    if el[1] == "שקל":
                                        money += int(el[0])
                                    all_cur += cur
                                    all_money += money
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
                all_text += text_cnf["day_report_all"].format(db_cmd.get_user_data(cur_id)[1], sumx, all_cur, all_money)
        all_text += text_cnf["day_all_report_x"].format(summxa)
    return all_text


def check_all_products2(products, products2):
    result = []
    for product in products:
        if db_cmd.check_product(product):
            result.append(True)
        elif product[1] == "שקל":
            result.append(True)
        else:
            result.append(False)
    result2 = []
    for product2 in products2:
        if db_cmd.check_product(product2):
            result2.append(True)
        elif product2[1] == "שקל":
            result2.append(True)
        else:
            result2.append(False)
    return result, result2


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def check_all_products(products):
    result = []
    for product in products:
        result.append(db_cmd.check_product(product))
    return result


def get_text_order_from_mk(data, username, type, order_id):
    dataxx = ast.literal_eval(data)["new_order"]["data"]
    text_cnf = readJs("text.json")
    text_error = text_cnf["number_order"].format(order_id)
    if type in [22, 38]:
        typex = text_cnf["type_pickup"]
    elif type in [12, 33]:
        typex = text_cnf["type_courier"]
    text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
    text_error += text_cnf["order_type_and_username"].format(typex, username)
    if type > 32:
        text_error += text_cnf["return_order_id"].format(ast.literal_eval(data)["order_id"])
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_order3"]
        for product in dataxx["product2"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
    else:
        text_error += text_cnf["text_order"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_price_and_comment_in_order"].format(
            dataxx["money"], dataxx["comment"])
    return text_error


def get_text_order_next_step(data):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    if data[4] in [33, 38]:
        username = db_cmd.get_user_data(data[2])[1]
        type = data[4]
        text_error = text_cnf["number_order"].format(data[0])
        time = data[6]
        if data[3] == 1:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_2"])
        elif data[3] == 2:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_3"])
        elif data[3] == 0:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
        elif data[3] == 3:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_4"])
        elif data[3] == 4:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_5"])
            text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                dataxx["cnlorder"])
        elif data[3] == 5:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_6"])
            try:
                text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                    dataxx["cnlorder"])
            except:
                pass
        elif data[3] == 6:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_7"])
        if type == 22 or type == 38:
            typex = text_cnf["type_pickup"]
        elif type == 12 or type == 33:
            typex = text_cnf["type_courier"]
        text_error += text_cnf["order_type_and_username"].format(typex, username)
        if data[3] != 0 and data[3] != 4:
            try:
                username_courier = db_cmd.get_user_data(data[7])[1]
                text_error += text_cnf["courier_username"].format(username_courier)
            except:
                text_error += text_cnf["courier_username"].format(text_cnf["nocurorder"])
        try:
            text_error += text_cnf["return_order_id"].format(ast.literal_eval(data[5])["connect"])
        except:
            text_error += text_cnf["return_order_id"].format(ast.literal_eval(data[5])["order_id"])
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_order3"]
        for product in dataxx["product2"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
    else:
        username = db_cmd.get_user_data(data[2])[1]
        type = data[4]
        text_error = text_cnf["number_order"].format(data[0])
        time = data[6]
        if data[3] == 1:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_2"])
        elif data[3] == 2:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_3"])
        elif data[3] == 0:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
        elif data[3] == 3:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_4"])
        elif data[3] == 4:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_5"])
            text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                dataxx["cnlorder"])
        elif data[3] == 5:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_6"])
            try:
                text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                    dataxx["cnlorder"])
            except:
                pass
        elif data[3] == 6:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_7"])
        if type == 22:
            typex = text_cnf["type_pickup"]
        elif type == 12:
            typex = text_cnf["type_courier"]
        text_error += text_cnf["order_type_and_username"].format(typex, username)
        try:
            if data[3] != 0 and data[3] != 4:
                try:
                    username_courier = db_cmd.get_user_data(data[7])[1]
                    text_error += text_cnf["courier_username"].format(username_courier)
                except:
                    text_error += text_cnf["courier_username"].format(text_cnf["nocurorder"])
        except:
            pass
        text_error += text_cnf["text_order"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_price_and_comment_in_order"].format(
            dataxx["money"], dataxx["comment"])
    return text_error


def get_text_order_next_step33(data):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    if data[4] in [33, 38]:
        username = db_cmd.get_user_data(data[2])[1]
        type = data[4]
        text_error = text_cnf["number_order"].format(data[0])
        time = data[6]
        if data[3] == 1:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_2"])
        elif data[3] == 2:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_3"])
        elif data[3] == 0:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
        elif data[3] == 3:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_4"])
        elif data[3] == 4:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_5"])
            text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                dataxx["cnlorder"])
        elif data[3] == 5:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_6"])
            try:
                text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                    dataxx["cnlorder"])
            except:
                pass
        elif data[3] == 6:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_7"])
        if type == 22 or type == 38:
            typex = text_cnf["type_pickup"]
        elif type == 12 or type == 33:
            typex = text_cnf["type_courier"]
        text_error += text_cnf["order_type_and_username"].format(typex, "None")
        if data[3] != 0 and data[3] != 4:
            try:
                username_courier = db_cmd.get_user_data(data[7])[1]
                text_error += text_cnf["courier_username"].format(username_courier)
            except:
                text_error += text_cnf["courier_username"].format(text_cnf["nocurorder"])
        try:
            text_error += text_cnf["return_order_id"].format(ast.literal_eval(data[5])["connect"])
        except:
            text_error += text_cnf["return_order_id"].format(ast.literal_eval(data[5])["order_id"])
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_order3"]
        for product in dataxx["product2"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
    else:
        username = db_cmd.get_user_data(data[2])[1]
        type = data[4]
        text_error = text_cnf["number_order"].format(data[0])
        time = data[6]
        if data[3] == 1:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_2"])
        elif data[3] == 2:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_3"])
        elif data[3] == 0:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
        elif data[3] == 3:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_4"])
        elif data[3] == 4:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_5"])
            text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                dataxx["cnlorder"])
        elif data[3] == 5:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_6"])
            try:
                text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                    dataxx["cnlorder"])
            except:
                pass
        elif data[3] == 6:
            text_error += text_cnf["status_order_text"].format(text_cnf["status_order_7"])
        if type == 22:
            typex = text_cnf["type_pickup"]
        elif type == 12:
            typex = text_cnf["type_courier"]
        text_error += text_cnf["order_type_and_username"].format(typex, username)
        try:
            if data[3] != 0 and data[3] != 4:
                try:
                    username_courier = db_cmd.get_user_data(data[7])[1]
                    text_error += text_cnf["courier_username"].format(username_courier)
                except:
                    text_error += text_cnf["courier_username"].format(text_cnf["nocurorder"])
        except:
            pass
        text_error += text_cnf["text_order"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_price_and_comment_in_order"].format(
            dataxx["money"], dataxx["comment"])
    return text_error


def storage_text_now():
    text_cnf = readJs("text.json")
    tft = db_cmd.get_all_stock()
    text = f'{text_cnf["goods_stock"]}:\n\n'
    for element in tft:
        k = 0
        product_data_refill = db_cmd.get_product_refill_active_next(element[0])
        for el in product_data_refill:
            k += float(el[3])
        if k > 0 and k < 50:
            text += text_cnf["product_card"].format(element[1],
                                                    element[2], text_cnf["product_status_0"])
        elif k >= 50:
            text += text_cnf["product_card"].format(element[1],
                                                    element[2], text_cnf["product_status_1"])
    return text


def goods_cur():
    text_cnf = readJs("text.json")
    text = f'{text_cnf["product_cur_all"]}'
    data = db_cmd.get_user_data_by_role(8)
    for el in data:
        datax = ast.literal_eval(el[5])["product"]
        for i in datax:
            if i[0] > 0 and i[1] != "שקל":
                text += text_cnf["card_prodcut_cur_sm"].format(el[1], i[1], i[2], i[0])

    data = db_cmd.get_user_data_by_role(9)
    for el in data:
        datax = ast.literal_eval(el[5])["product"]
        for i in datax:
            if i[0] > 0 and i[1] != "שקל":
                text += text_cnf["card_prodcut_cur_sm"].format(el[1], i[1], i[2], i[0])

    return text


def goods_cur2():
    text_cnf = readJs("text.json")
    text = f'{text_cnf["product_cur_all"]}'
    data = db_cmd.get_user_data_by_role(8)
    for el in data:
        datax = ast.literal_eval(el[5])["product"]
        for i in datax:
            if i[0] > 0 and i[1] != "שקל":
                text += text_cnf["card_prodcut_cur_sm"].format(el[1], i[1], i[2], i[0])
            elif i[1] == "שקל":
                bank = db_cmd.get_user_bank(el[0])[1]
                text += text_cnf["card_prodcut_cur_sm2"].format(el[1], i[1], i[0], bank)

    data = db_cmd.get_user_data_by_role(9)
    for el in data:
        datax = ast.literal_eval(el[5])["product"]
        for i in datax:
            if i[0] > 0 and i[1] != "שקל":
                text += text_cnf["card_prodcut_cur_sm"].format(el[1], i[1], i[2], i[0])
            elif i[1] == "שקל":
                bank = db_cmd.get_user_bank(el[0])[1]
                text += text_cnf["card_prodcut_cur_sm2"].format(el[1], i[1], i[0], bank)

    return text


def get_text_order_next_step_sm(data):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    username = db_cmd.get_user_data(data[2])[1]
    type = data[4]
    text_error = text_cnf["number_order"].format(data[0])
    time = data[6]
    if data[3] == 1:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_2"])
    elif data[3] == 2:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_3"])
    elif data[3] == 0:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_1"])
    elif data[3] == 3:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_4"])
    elif data[3] == 4:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_5"])
        text_error += text_cnf["reason_for_cancellation_in_channel"].format(
            dataxx["cnlorder"])
    elif data[3] == 5:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_order_6"])
        try:
            text_error += text_cnf["reason_for_cancellation_in_channel"].format(
                dataxx["cnlorder"])
        except:
            pass
    if type == 22 or type == 38:
        typex = text_cnf["type_pickup"]
    elif type == 12 or type == 33:
        typex = text_cnf["type_courier"]
    if type == 33 or type == 38:
        text_error += text_cnf["order_type_and_username"].format(typex, username)
        text_error += text_cnf["return_order_id"].format(dataxx["order_id"])
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_order3"]
        for product in dataxx["product2"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
    else:
        text_error += text_cnf["order_type_and_username"].format(typex, username)
        text_error += text_cnf["text_order"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_price_and_comment_in_order"].format(
            dataxx["money"], dataxx["comment"])
    return text_error


def get_text_by_warehouse_order(data):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(data[7])[1]
    text_error = text_cnf["courier_username"].format(username_courier)
    try:
        text_error += text_cnf["workerss"].format(db_cmd.get_user_data(data_w[5])[1])
    except:
        pass
    text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_0"])
    for product in dataxx["product"]:
        if product[1] != "שקל":
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
    return text_error


def return_order(order_id):
    order_data = db_cmd.get_order_by_order_id(order_id)
    if order_data[3] == 3:
        db_cmd.update_order(order_id, 'status_order', 2)
        if order_data[4] in [12, 22]:
            take_product_return(order_data)
            cur_id = order_data[7]
            money = ast.literal_eval(order_data[5])['money']
            cur_data = db_cmd.get_user_data(cur_id)
            backpuck = ast.literal_eval(cur_data[5])
            money = float(money)
            if money < 0:
                money = -1 * money - 1
            backpuck['product'][0][0] -= float(money)
            db_cmd.update_user(cur_id, "on_hands", str(backpuck))
        elif order_data[4] in [33, 38]:
            take_product_return(order_data)
    db_cmd.update_order(order_id, 'status_order', 2)
    finance_deals = db_cmd.get_finance_deals_by_id(order_id)
    for deals in finance_deals:
        db_cmd.update_bank(deals[2], round(
            float(db_cmd.get_user_bank(deals[2])[1]), 2) - round(float(deals[3]), 2))
        if deals[4] != -1:
            db_cmd.update_bank(deals[4], round(
                float(db_cmd.get_user_bank(deals[4])[1]), 2) + round(float(deals[3]), 2))
    db_cmd.dlt_deals_by_order_id(order_id)
    db_cmd.order_time_null(order_id)
    if order_data[6] == 1:
        db_cmd.update_order(order_id, 'time', 2)


def return_order_w(order_id, botx):
    order_data = db_cmd.get_order_warehouse_by_id(order_id)
    if order_data[3] in [2, 3]:
        db_cmd.update_order_w(order_id, 'status_order', 1)
        take_product_return_w(order_data)
        data = db_cmd.get_order_warehouse_by_id(order_id)
        text = get_text_by_warehouse_order_next(data)
        botx.edit_message_text(chat_id=readJs()["telegram"]["warehouse_channel"],
                               message_id=data[1],
                               text=text,
                               parse_mode=None,
                               reply_markup=markup.menu_cnlwhx())
    elif order_data[3] in [6]:
        db_cmd.update_order_w(order_id, 'status_order', 5)
        take_product_return_w2(order_data)
        finance_deals = db_cmd.get_finance_deals_by_orderid(int(order_id) * -1)
        for deals in finance_deals:
            db_cmd.update_bank(deals[2], round(
                float(db_cmd.get_user_bank(deals[2])[1]), 2) - round(float(deals[3]), 2))
        db_cmd.dlt_deals_by_order_id(int(order_id) * -1)
        data = db_cmd.get_order_warehouse_by_id(order_id)
        text = get_text_by_warehouse_order2(data)
        botx.edit_message_text(chat_id=readJs()["telegram"]["warehouse_channel"],
                               message_id=data[1],
                               text=text,
                               parse_mode=None,
                               reply_markup=markup.menu_cnlwhx())

    '''
    finance_deals = db_cmd.get_finance_deals_by_id(order_id)
    for deals in finance_deals:
        db_cmd.update_bank(deals[2], round(
            float(db_cmd.get_user_bank(deals[2])[1]), 2) - round(float(deals[3]), 2))
        if deals[4] != -1:
            db_cmd.update_bank(deals[4], round(
                float(db_cmd.get_user_bank(deals[4])[1]), 2) + round(float(deals[3]), 2))
    db_cmd.dlt_deals_by_order_id(order_id)'''
    # db_cmd.order_time_null(order_id)


def take_product_return_w(data_w):
    products = ast.literal_eval(data_w[4])['correct_product']
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active_next(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                    product_refill[4]) - product_num_now, 2)))
                db_cmd.update_refill(product_refill[0], 'number_now', "{:.2f}".format(round(float(
                    product_refill[3]) + product_num_now, 2)))
                update_on_hands_courier(data_w[2], product_name, - product_num_now, product_price)
                break


def take_product_return_w2(data_w):
    products2 = ast.literal_eval(data_w[4])['product']
    products2x = ast.literal_eval(data_w[4])['true_product']
    if len(products2[0]) == 3:
        for product in products2:
            product_name = product[1]
            product_num_now = product[0]
            product_price = float(product[2])
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) + product_num_now, 2)))
                    update_on_hands_courier(data_w[2], product_name, product_num_now, product_price)
                    break
    else:
        product_next = []
        for xxx in products2:
            f = 0
            for yyy in products2x:
                if yyy[1] == xxx[1]:
                    product_next.append([xxx[0], xxx[1], yyy[2]])
                    f = 1
                    break
            if f == 0:
                price = db_cmd.get_product_by_name(xxx[1])[2]
                product_next.append([xxx[0], xxx[1], price])
        for product in product_next:
            product_name = product[1]
            product_num_now = product[0]
            product_price = float(product[2])
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) + product_num_now, 2)))
                    update_on_hands_courier(data_w[2], product_name, product_num_now, product_price)
                    break
    for product in products2x:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active_next(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                db_cmd.update_refill(product_refill[0], 'number_now', "{:.2f}".format(round(float(
                    product_refill[3]) - product_num_now, 2)))
                break


def take_product_return(data_w):
    products = ast.literal_eval(data_w[5])['correct_product']
    for product in products:
        if product[1] != "שקל":
            product_name = product[1]
            product_num_now = product[0]
            product_price = float(product[2])
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) + product_num_now, 2)))
                    update_on_hands_courier(data_w[7], product_name, product_num_now, product_price)
                    break
        else:
            cur_data = db_cmd.get_user_data(data_w[7])
            backpuck = ast.literal_eval(cur_data[5])
            backpuck['product'][0][0] += float(product[0])
            db_cmd.update_user(data_w[7], "on_hands", str(backpuck))
    if data_w[4] in [33, 38]:
        products2 = ast.literal_eval(data_w[5])['true_product']
        for product in products2:
            if product[1] != "שקל":
                product_name = product[1]
                product_num_now = product[0]
                product_price = float(product[2])
                product_data = db_cmd.get_product_by_name(product_name)
                product_id = product_data[0]
                product_data_refill = db_cmd.get_product_refill_active_next(product_id)
                for product_refill in product_data_refill:
                    if float(product_refill[5]) + float(product_refill[6]) == product_price:
                        db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                            product_refill[4]) - product_num_now, 2)))
                        update_on_hands_courier(
                            data_w[7], product_name, -product_num_now, product_price)
                        break
            else:
                cur_data = db_cmd.get_user_data(data_w[7])
                backpuck = ast.literal_eval(cur_data[5])
                backpuck['product'][0][0] -= float(product[0])
                db_cmd.update_user(data_w[7], "on_hands", str(backpuck))


def text_report_cur_ystd(list_order, uid):
    text_cnf = readJs("text.json")
    massx = []
    nowx = datetime.datetime.now() - timedelta(days=1)
    now = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time()) - timedelta(days=1)
    status_list = ["✅⚖️", "✅💸", "✅⚖️", "❌💸",  "❌⚖️"]
    all_cur = 0
    result_cur = 0
    all_money = 0
    data_l = []
    if nowx > now + timedelta(hours=10):
        now = now + timedelta(days=1)
    date_order_time = (now - timedelta(days=1)).strftime("%d.%m.%Y")
    all_text = text_cnf["report_cur_title"].format(
        db_cmd.get_user_data(uid)[1], str(date_order_time))
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
                        city = dd["city"]
                        mx = dd["money"].replace(",", "")
                        money = mx
                        if float(money) < 0:
                            money = -float(money)
                        text = ""
                        for el in dd["correct_product"]:
                            if el[0] != 0:
                                text += f"{el[0]} {el[1]}\n"
                            f = 0
                            for x in range(len(data_l)):
                                if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
                                    data_l[x][0] += el[0]
                                    f = 1
                                    break
                            if f == 0:
                                data_l.append(el)
                        # "#{} | Статус: {} | Город: {} | Цена доставки: {} | Деньги: {} |\nТовары:\n{}\n"
                        status = db_cmd.get_order_by_order_id(elx)[6]
                        if not status:
                            status = 0
                        all_text += text_cnf["report_cur_text"].format(
                            elx, status_list[status], city, cur, money, text[:-1])
                        if status == 1:
                            result_cur += cur
                        all_cur += cur
                        all_money += int(money)
                    except Exception as e:
                        error1x += f"{e} {elx}\n\n"
                elif db_cmd.get_order_by_order_id(elx)[3] == 3 and db_cmd.get_order_by_order_id(elx)[4] > 30:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    city = dd["city"]
                    text = ""
                    money = 0
                    for el in dd["correct_product"]:
                        if el[1] != "שקל":
                            text += f"{el[0]} {el[1]}\n"
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
                            text += f"- {el[0]} {el[1]}\n"
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
                    status = db_cmd.get_order_by_order_id(elx)[6]
                    if not status:
                        status = 0
                    all_text += text_cnf["report_cur_text"].format(
                        elx, status_list[status], city, cur, money, text[:-1])
                    if status == 1:
                        result_cur += cur
                    all_cur += cur
                    all_money += money
                else:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    city = dd["city"]
                    money = 0
                    status = db_cmd.get_order_by_order_id(elx)[6]
                    if status == 1:
                        status = 3
                    else:
                        status = 4
                    if status == 3:
                        result_cur += cur
                    all_cur += cur
                    all_text += text_cnf["report_cur_text2"].format(
                        elx, status_list[status], city, cur, money)
                    if len(all_text) > 3550:
                        massx.append(all_text)
                        all_text = ""
            except Exception as e:
                print(e, elx)
    if len(all_text) > 4:
        all_text += text_cnf["general_report_cur_text"].format(
            all_cur, result_cur, all_money, all_money - all_cur, all_money - result_cur)
        massx.append(all_text)
    else:
        massx[-1] = massx[-1] + text_cnf["general_report_cur_text"].format(
            all_cur, result_cur, all_money, all_money - all_cur, all_money - result_cur)
    return massx


def text_report_cur(list_order, uid):
    text_cnf = readJs("text.json")
    nowx = datetime.datetime.now()
    massx = []
    now = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time())
    status_list = ["✅⚖️", "✅💸", "✅⚖️", "❌💸",  "❌⚖️"]
    all_cur = 0
    result_cur = 0
    all_money = 0
    data_l = []
    if nowx > now + timedelta(hours=10):
        now = now + timedelta(days=1)
    date_order_time = (now - timedelta(days=1)).strftime("%d.%m.%Y")
    all_text = text_cnf["report_cur_title"].format(
        db_cmd.get_user_data(uid)[1], str(date_order_time))
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
                        city = dd["city"]
                        mx = dd["money"].replace(",", "")
                        money = mx
                        if float(money) < 0:
                            money = -float(money)
                        text = ""
                        for el in dd["correct_product"]:
                            text += f"{el[0]} {el[1]}\n"
                            f = 0
                            for x in range(len(data_l)):
                                if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
                                    data_l[x][0] += el[0]
                                    f = 1
                                    break
                            if f == 0:
                                data_l.append(el)
                        # "#{} | Статус: {} | Город: {} | Цена доставки: {} | Деньги: {} |\nТовары:\n{}\n"
                        status = db_cmd.get_order_by_order_id(elx)[6]
                        if not status:
                            status = 0
                        all_text += text_cnf["report_cur_text"].format(
                            elx, status_list[status], city, cur, money, text[:-1])
                        if status == 1:
                            result_cur += cur
                        all_cur += cur
                        all_money += int(money)
                    except Exception as e:
                        error1x += f"{e} {elx}\n\n"
                elif db_cmd.get_order_by_order_id(elx)[3] == 3 and db_cmd.get_order_by_order_id(elx)[4] > 30:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    city = dd["city"]
                    text = ""
                    money = 0
                    for el in dd["correct_product"]:
                        if el[1] != "שקל":
                            text += f"{el[0]} {el[1]}\n"
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
                            text += f"- {el[0]} {el[1]}\n"
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
                    status = db_cmd.get_order_by_order_id(elx)[6]
                    if not status:
                        status = 0
                    all_text += text_cnf["report_cur_text"].format(
                        elx, status_list[status], city, cur, money, text[:-1])
                    if status == 1:
                        result_cur += cur
                    all_cur += cur
                    all_money += money
                else:
                    dd = ast.literal_eval(db_cmd.get_order_by_order_id(elx)[5])
                    try:
                        cur = dd["courier"]
                    except:
                        cur = 0
                    city = dd["city"]
                    money = 0
                    status = db_cmd.get_order_by_order_id(elx)[6]
                    if status == 1:
                        status = 3
                    else:
                        status = 4
                    if status == 3:
                        result_cur += cur
                    all_cur += cur
                    all_text += text_cnf["report_cur_text2"].format(
                        elx, status_list[status], city, cur, money)
                    if len(all_text) > 3550:
                        massx.append(all_text)
                        all_text = ""
            except Exception as e:
                print(e, elx)

    if len(all_text) > 4:
        all_text += text_cnf["general_report_cur_text"].format(
            all_cur, result_cur, all_money, all_money - all_cur, all_money - result_cur)
        massx.append(all_text)
    else:
        massx[-1] = massx[-1] + text_cnf["general_report_cur_text"].format(
            all_cur, result_cur, all_money, all_money - all_cur, all_money - result_cur)
    print(massx)
    return massx


def get_text_by_warehouse_order_x(data, uid):
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(uid)[1]
    text_error = text_cnf["courier_username"].format(username_courier)
    text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_0"])
    for product in data:
        if product[1] != "שקל":
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order2"].format(
                    product[1], int(product[0]), product[2])
            else:
                text_error += text_cnf["text_product_in_order2"].format(
                    product[1], product[0], product[2])
    return text_error


def get_text_by_warehouse_order_x2(data, uid):
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(uid)[1]
    text_error = text_cnf["courier_username"].format(username_courier)
    text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_0"])
    try:
        for product in data:
            if product[1] != "שקל":
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order2"].format(
                        product[1], int(product[0]), product[2])
                else:
                    text_error += text_cnf["text_product_in_order2"].format(
                        product[1], product[0], product[2])
    except:
        for product in data:
            if product[1] != "שקל":
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], product[0])
    return text_error


def get_text_by_warehouse_order2(order_w):
    cur = order_w[2]
    dataxx = ast.literal_eval(order_w[4])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(cur)[1]
    text_error = text_cnf["number_order_storage"].format(order_w[0])
    text_error += text_cnf["courier_username"].format(username_courier)
    text_error += text_cnf["return_type_order"]
    if order_w[3] in [4, 0]:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_0"])
    elif order_w[3] == 5:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_5"])
    try:
        for product in dataxx["product"]:
            if product[1] != "שקל":
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order2"].format(
                        product[1], int(product[0]), product[2])
                else:
                    text_error += text_cnf["text_product_in_order2"].format(
                        product[1], product[0], product[2])
    except:
        for product in dataxx["product"]:
            if product[1] != "שקל":
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], product[0])
    return text_error


def get_text_by_warehouse_order3(order_w):
    cur = order_w[2]
    dataxx = ast.literal_eval(order_w[4])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(cur)[1]
    text_error = text_cnf["number_order_storage"].format(order_w[0])
    text_error += text_cnf["courier_username"].format(username_courier)
    text_error += text_cnf["return_type_order"]
    if order_w[3] in [4, 0]:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_0"])
    elif order_w[3] == 5:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_5"])
    for product in dataxx["product"]:
        if product[1] != "שקל":
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], product[0])
    return text_error


def update_on_hands_courier2(courier_id, product_name, product_num, product_price):
    data = db_cmd.get_user_data(courier_id)
    if data[5]:
        datax = ast.literal_eval(data[5])["product"]
        check = False
        for i in range(len(datax)):
            if datax[i][1] == product_name and datax[i][2] == product_price:
                datax[i][0] = float("{:.2f}".format(round(float(
                    datax[i][0] + product_num), 2)))
                check = True
                break
        if not check:
            datax.append([float("{:.2f}".format(round(float(product_num), 2))),
                          product_name, round(product_price, 2)])
        new_data = {'product': datax}
    else:
        new_data = {'product': [
            [float("{:.2f}".format(round(float(product_num), 2))), product_name, round(product_price, 2)]]}
    db_cmd.update_user(courier_id, 'on_hands', str(new_data))


def update_on_hands_courier(courier_id, product_name, product_num, product_price):
    data = db_cmd.get_user_data(courier_id)
    if data[5]:
        datax = ast.literal_eval(data[5])["product"]
        check = False
        for i in range(len(datax)):
            if datax[i][1] == product_name and datax[i][2] == product_price:
                datax[i][0] = float("{:.2f}".format(round(float(
                    datax[i][0] + product_num), 2)))
                check = True
                break
        if not check:
            datax.append([float("{:.2f}".format(round(float(product_num), 2))),
                          product_name, round(product_price, 2)])
        new_data = {'product': datax}
    else:
        new_data = {'product': [
            [float("{:.2f}".format(round(float(product_num), 2))), product_name, round(product_price, 2)]]}
    db_cmd.update_user(courier_id, 'on_hands', str(new_data))


def update_on_hands_courie_money(courier_id, product_name, product_num):
    data = db_cmd.get_user_data(courier_id)
    if data[5]:
        datax = ast.literal_eval(data[5])["product"]
        check = False
        for i in range(len(datax)):
            if datax[i][1] == product_name:
                datax[i][0] = float("{:.2f}".format(round(float(
                    datax[i][0] + product_num), 2)))
                check = True
                break
        if not check:
            datax.append([float("{:.2f}".format(round(float(product_num), 2))),
                          product_name])
        new_data = {'product': datax}
    else:
        new_data = {'product': [
            [float("{:.2f}".format(round(float(product_num), 2))), product_name]]}
    db_cmd.update_user(courier_id, 'on_hands', str(new_data))


def take_warehouse(data_w):
    products = ast.literal_eval(data_w[4])['correct_product']
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                db_cmd.update_refill(product_refill[0], 'number_now', "{:.2f}".format(round(float(
                    product_refill[3]) - product_num_now, 2)))
                db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                    product_refill[4]) + product_num_now, 2)))
                update_on_hands_courier(data_w[2], product_name, product_num_now, product_price)
                break


def take_warehouse23(data_w):
    products = ast.literal_eval(data_w[4])['correct_product']
    product_alt = ast.literal_eval(data_w[4])['product']
    dataxx = []
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                for el in product_alt:
                    if el[1] == product_name:
                        db_cmd.update_refill(product_refill[0], 'number_now', "{:.2f}".format(round(float(
                            product_refill[3]) - product_num_now, 2)))
                        db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                            product_refill[4]) + product_num_now, 2)))
                        update_on_hands_courier(data_w[2], product_name, el[0], product_price)
                        dataxx.append([product_num_now - el[0], el[1], product_price])
                        break

        return dataxx


def check_storage_now(data):
    if "correct_product" in data:
        for product in data["correct_product"]:
            product_name = product[1]
            product_num_now = product[0]
            product_price = float(product[2])
            product_id = db_cmd.get_product_by_name(product_name)[0]
            product_data_refill = db_cmd.get_product_refill_active(product_id)
            checkx = 0
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price and float(product_refill[3]) >= float(product_num_now):
                    checkx = 1
                    break
            if checkx == 0:
                return False
        return True
    else:
        for product in data["product"]:
            product_name = product[1]
            product_num_now = product[0]
            # product_price = float(product[2])
            product_id = db_cmd.get_product_by_name(product_name)[0]
            product_data_refill = db_cmd.get_product_refill_active(product_id)
            checkx = 0
            for product_refill in product_data_refill:
                if float(product_refill[3]) >= float(product_num_now):
                    checkx = 1
                    break
            if checkx == 0:
                return False
        return True


def check_storage_now_xt(data):
    if "correct_product" in data:
        for product in data["correct_product"]:
            product_name = product[1]
            product_num_now = product[0]
            product_price = float(product[2])
            product_id = db_cmd.get_product_by_name(product_name)[0]
            product_data_refill = db_cmd.get_product_refill_active(product_id)
            checkx = 0
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price and float(product_refill[3]) + float(product_refill[4]) >= float(product_num_now):
                    checkx = 1
                    break
            if checkx == 0:
                return False
        return True
    else:
        for product in data["product"]:
            product_name = product[1]
            product_num_now = product[0]
            # product_price = float(product[2])
            product_id = db_cmd.get_product_by_name(product_name)[0]
            product_data_refill = db_cmd.get_product_refill_active(product_id)
            checkx = 0
            for product_refill in product_data_refill:
                if float(product_refill[3]) + float(product_refill[4]) >= float(product_num_now):
                    checkx = 1
                    break
            if checkx == 0:
                return False
        return True


def add_warehouse(data_w):
    products = data_w
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                db_cmd.update_refill(product_refill[0], 'number_now', "{:.2f}".format(round(float(
                    product_refill[3]) + product_num_now, 2)))
                break


def take_courier_and_storage(data):
    products = ast.literal_eval(data[5])['correct_product']
    for product in products:
        product_name = product[1]
        if product_name != "שקל":
            product_num_now = product[0]
            product_price = float(product[2])
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) - product_num_now, 2)))
                    update_on_hands_courier2(data[7], product_name, -
                                             1 * product_num_now, product_price)
                    break
        else:
            product_num_now = product[0]
            update_on_hands_courie_money(data[7], product_name, -1 * product_num_now)
    dtf = ast.literal_eval(data[5])
    if "money" in dtf:
        money = round(float(ast.literal_eval(data[5])['money']), 2)
        update_on_hands_courie_money(data[7], "שקל", money)


def take_courier_and_storage_cur(data, cur):
    products = data
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        product_price = float(product[2])
        product_data = db_cmd.get_product_by_name(product_name)
        product_id = product_data[0]
        product_data_refill = db_cmd.get_product_refill_active_next(product_id)
        for product_refill in product_data_refill:
            if float(product_refill[5]) + float(product_refill[6]) == product_price:
                db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                    product_refill[4]) - product_num_now, 2)))
                update_on_hands_courier2(cur, product_name, -
                                         1 * product_num_now, product_price)
                break


def take_courier_and_storage_cur_fx(data, cur):
    products = data["product"]
    products2 = ast.literal_eval(db_cmd.get_user_data(cur)[5])["product"]
    for product in products:
        product_name = product[1]
        product_num_now = product[0]
        if len(product) == 3:
            product_price = float(product[2])
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) - product_num_now, 2)))
                    update_on_hands_courier2(cur, product_name, -
                                             1 * product_num_now, product_price)
                    break
        else:
            product_data = db_cmd.get_product_by_name(product_name)
            product_id = product_data[0]
            f = 0
            for el in products2:
                if el[1] == product_name and el[0] >= product_num_now:
                    product_price = el[2]
                    f = 1
                    break
            if f == 0:
                product_price = db_cmd.get_product_by_name(product_name)[2]
            product_data_refill = db_cmd.get_product_refill_active_next(product_id)
            for product_refill in product_data_refill:
                if float(product_refill[5]) + float(product_refill[6]) == product_price:
                    db_cmd.update_refill(product_refill[0], 'on_hands', "{:.2f}".format(round(float(
                        product_refill[4]) - product_num_now, 2)))
                    update_on_hands_courier2(cur, product_name, -
                                             1 * product_num_now, product_price)
                    break


def take_courier_and_storage2(data):
    order_data = ast.literal_eval(data[5])
    if "true_product" in order_data and "stk" in order_data:
        products = order_data['true_product']
        for product in products:
            if product[1] != "שקל":
                product_data = db_cmd.get_product_by_name(product[1])
                product_id = product_data[0]
                product_data_refill = db_cmd.get_product_refill_active_next(product_id)
                for prx in product_data_refill:
                    if float(prx[5]) + float(prx[6]) == float(pricexx):
                        db_cmd.update_refill(prx[0], 'on_hands', "{:.2f}".format(round(float(
                            prx[4]) + product[0], 2)))
                        update_on_hands_courier2(data[7], product[1], product[0],
                                                 round(float(product[2]), 2))
                        break
            else:
                product_num_now = product[0]
                update_on_hands_courie_money(data[7], product[1], product[0])
    else:
        order_referance_id = order_data['order_id']
        products = order_data['product2']
        true_product = []
        for product in products:
            if product[1] != "שקל":
                ff = 0
                try:
                    old_order_data = db_cmd.get_order_by_order_id(order_referance_id)
                    old_order_data_correct = ast.literal_eval(
                        old_order_data[5])['correct_product']
                    for elll in old_order_data_correct:
                        if elll[1] == product[1] and elll[0] > 0:
                            pricexx = elll[2]
                            true_product.append([product[0], product[1], pricexx])
                            ff = 1
                            break
                except:
                    pass
                if ff == 0:
                    pricexx = db_cmd.get_product_by_name(product[1])[2]
                    true_product.append([product[0], product[1], pricexx])
                product_data = db_cmd.get_product_by_name(product[1])
                product_id = product_data[0]
                product_data_refill = db_cmd.get_product_refill_active_next(product_id)
                for prx in product_data_refill:
                    if float(prx[5]) + float(prx[6]) == float(pricexx):
                        db_cmd.update_refill(prx[0], 'on_hands', "{:.2f}".format(round(float(
                            prx[4]) + product[0], 2)))
                        update_on_hands_courier2(data[7], product[1], product[0],
                                                 round(float(pricexx), 2))
                        break
            else:
                product_num_now = product[0]
                true_product.append([product[0], product[1]])
                update_on_hands_courie_money(data[7], product[1], product_num_now)

        order_data["true_product"] = true_product
        order_data["stk"] = 0
        if data[4] in [38]:
            order_data["stk"] = 1
        db_cmd.update_order(data[0], 'data', str(order_data))


def checkxcur(data):
    id_cur = data[7]
    order_id = data[0]
    check = True
    if id_cur:
        list_order_w = db_cmd.get_order_warehouse_by_cur(id_cur)
        for ow in list_order_w:
            try:
                if ast.literal_eval(ow[4])["order_id"] == order_id:
                    check = False
                    orderx = ow
                    break
            except:
                pass
        if not check:
            order_telo = ast.literal_eval(data[5])
            try:
                if order_telo["correct_product"]:
                    check = True
            except:
                if orderx[3] == 3:
                    check = True
                else:
                    check = False
        return check
    else:
        return False


def checkxcur2(data, datax):
    id_cur = data[7]
    order_id = data[0]
    check = True
    if id_cur:
        list_order_w = db_cmd.get_order_warehouse_by_cur(id_cur)
        for ow in list_order_w:
            try:
                if ast.literal_eval(ow[4])["order_id"] == order_id:
                    check = False
                    break
            except:
                pass
        if not check:
            order_telo = ast.literal_eval(data[5])
            try:
                if order_telo["correct_product"]:
                    check = True
            except:
                check = False
            if check:
                check = checkff(data, datax)
        return check
    else:
        return False


def checkff(data, datax):
    datafx = ast.literal_eval(data[5])["product"]
    check = True
    for el in datafx:
        for el2 in datax:
            if el[1] == el2[1] and float(el2[0]) > float(el[0]):
                check = False
    for el2 in datax:
        k = 0
        for el in datafx:
            if el[1] == el2[1]:
                k = 1
        if k == 0:
            check = False
    return check


def update_concret_price(prices):
    for price in prices:
        db_cmd.update_price_stock(price, prices[price])


def update_price():
    data2 = db_cmd.get_products_refill_active()
    data_price = {}
    data = db_cmd.get_product_all()
    for refill in data:
        pr = 0
        kol = 0
        for ref2 in data2:
            if refill[0] == ref2[1] and float(ref2[4]) + float(ref2[3]) > kol and kol < 50:
                pr = float(ref2[5]) + float(ref2[6])
                kol = float(ref2[4]) + float(ref2[3])
        if pr != float(refill[2]) and pr > 0:
            print(refill)
            data_price[str(refill[0])] = pr
    update_concret_price(data_price)


def get_text_by_warehouse_order_next(data_w):
    dataxx = ast.literal_eval(data_w[4])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(data_w[2])[1]
    text_error = text_cnf["number_order_storage"].format(data_w[0])
    text_error += text_cnf["courier_username"].format(username_courier)
    try:
        text_error += text_cnf["workerss"].format(db_cmd.get_user_data(data_w[5])[1])
    except:
        pass
    if data_w[3] == 1:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_1"])
    elif data_w[3] == 2:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_2"])
    elif data_w[3] == 3:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_3"])
    for product in dataxx["product"]:
        if str(product[0]).split(".")[1] == "0":

            text_error += text_cnf["text_product_in_order"].format(
                product[1], int(product[0]))
        else:
            text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
    try:
        comment = ast.literal_eval(db_cmd.get_order_by_order_id(dataxx["order_id"])[5])["comment"]
        text_error += text_cnf["text_comment_in_order"].format(comment)
    except:
        pass
    return text_error


def get_text_by_warehouse_order_next2(data_w):
    dataxx = ast.literal_eval(data_w[4])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(data_w[2])[1]
    text_error = text_cnf["number_order_storage"].format(data_w[0])
    text_error += text_cnf["courier_username"].format(username_courier)
    try:
        text_error += text_cnf["workerss"].format(db_cmd.get_user_data(data_w[5])[1])
    except:
        pass
    if data_w[3] == 1:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_1"])
    elif data_w[3] == 2:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_2"])
    elif data_w[3] == 3:
        text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_3"])
    for product in dataxx["correct_product"]:
        if str(product[0]).split(".")[1] == "0":

            text_error += text_cnf["text_product_in_order2"].format(
                product[1], int(product[0]), product[2])
        else:
            text_error += text_cnf["text_product_in_order2"].format(
                product[1], product[0], product[2])
    try:
        comment = ast.literal_eval(db_cmd.get_order_by_order_id(dataxx["order_id"])[5])["comment"]
        text_error += text_cnf["text_comment_in_order"].format(comment)
    except:
        pass
    return text_error


def get_text_by_warehouse_order_next3(data_w):
    dataxx = ast.literal_eval(data_w[4])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(data_w[2])[1]
    text_error = text_cnf["number_order_storage"].format(data_w[0])
    text_error += text_cnf["courier_username"].format(username_courier)
    try:
        text_error += text_cnf["workerss"].format(db_cmd.get_user_data(data_w[5])[1])
    except:
        pass
    text_error += text_cnf["status_order_text"].format(text_cnf["status_storage_6"])
    text_error += "\n\n"
    try:
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":

                text_error += text_cnf["text_product_in_order2"].format(
                    product[1], int(product[0]), product[2])
            else:
                text_error += text_cnf["text_product_in_order2"].format(
                    product[1], product[0], product[2])
    except:
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":

                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], product[0])
    text_error += f'\n\n{text_cnf["true_product"]}'
    for product in dataxx["true_product"]:
        if str(product[0]).split(".")[1] == "0":

            text_error += text_cnf["text_product_in_order2"].format(
                product[1], int(product[0]), product[2])
        else:
            text_error += text_cnf["text_product_in_order2"].format(
                product[1], product[0], product[2])
    return text_error


def get_text_order_from_sm(data, time):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    username = db_cmd.get_user_data(data[2])[1]
    type = data[4]
    text_error = text_cnf["number_order"].format(data[0])
    if type == 22:
        typex = text_cnf["type_pickup"]
    elif type == 12:
        typex = text_cnf["type_courier"]
    text_error += text_cnf["order_type_and_username"].format(typex, username)
    text_error += text_cnf["text_order"].format(
        dataxx["city"], dataxx["street"], dataxx["phone"])
    for product in dataxx["product"]:
        if str(product[0]).split(".")[1] == "0":
            text_error += text_cnf["text_product_in_order"].format(
                product[1], int(product[0]))
        else:
            text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
    text_error += text_cnf["text_price_and_comment_in_order"].format(
        dataxx["money"], dataxx["comment"])
    text_error.replace('_', '\_')
    return text_error


def conformity(data_orderx_do, data_orderx_posle):
    new_product2 = []
    check = True
    for product in data_orderx_posle:
        new_product2.append([product[0], product[1]])
    for i in range(len(new_product2) - 1):
        for j in range(i + 1, len(new_product2)):
            if new_product2[j][1] == new_product2[i][1]:
                new_product2[i][0] += new_product2[j][0]
                new_product2[j][0] = 0
    nnp = []
    for el in new_product2:
        if el[0] != 0:
            # new_product2.remove(el)
            nnp.append(el)
    new_product2 = nnp
    for i in new_product2:
        if not i in data_orderx_do:
            check = False
            break
    return check


def day_courir_text(cur_id, day):

    return 0


def calibration(product_list, courier_id):
    courier_data = db_cmd.get_user_data(courier_id)
    product_courier = ast.literal_eval(courier_data[5])["product"]
    new_product_list = []
    checkff = True
    for el in product_list:
        if el[1] == "שקל":
            new_product_list.append([el[0], el[1]])
        else:
            d = el[0]
            check = True
            for el2 in product_courier:
                if el2[1] == el[1] and el[0] <= el2[0]:
                    new_product_list.append([d, el[1], str(el2[2])])
                    check = False
                    d = 0
                    break
                elif el2[1] == el[1] and el[0] > el2[0]:
                    new_product_list.append([el2[0], el[1], str(el2[2])])
                    check = False
                    d = d - el2[0]
            if check:
                new_product_list.append([el[0], el[1], db_cmd.get_product_by_name(el[1])[2]])

            if d > 0:
                checkff = False

    return new_product_list, checkff


def cur_backpuck_text(cur_backpuck, user_id):
    text_cnf = readJs("text.json")
    new_product2 = []
    text = ""
    money = 0
    for product in cur_backpuck:
        if product[1] == "שקל":
            money = round(float(product[0]), 2)
        new_product2.append([product[0], product[1]])
    bank = round(float(db_cmd.get_user_bank(user_id)[1]), 2)
    for i in range(len(new_product2) - 1):
        for j in range(i + 1, len(new_product2)):
            if new_product2[j][1] == new_product2[i][1]:
                new_product2[i][0] += new_product2[j][0]
                new_product2[j][0] = 0
    nnp = []
    for el in new_product2:
        if el[0] != 0:
            # new_product2.remove(el)
            nnp.append(el)
    new_product2 = nnp
    if len(new_product2) == 0:
        text += text_cnf["text_clear_backpuck"]
    else:
        text += text_cnf["backpuck"]
        for el in new_product2:
            if str(el[0]).split(".")[1] == "0":
                text += text_cnf["text_product_in_order"].format(
                    el[1], int(el[0]))
            else:
                text += text_cnf["text_product_in_order"].format(el[1], el[0])
    return text, money, bank


def check_order_for_sw(data, text):
    text_cnf = readJs("text.json")
    dataxx = ast.literal_eval(data[4])["product"]
    check = False
    text_error = ""
    new_product = []
    try:
        check = True
        text = text.replace('(', '')
        text = text.replace('\n', '')
        datax = text.split(')')
        while '' in datax:
            datax.remove('')
        for el in datax:
            d = el.split(" ")
            while '' in d:
                d.remove('')
            dx = " ".join(d[1: -1])
            dataprf = db_cmd.get_product_refill_active(db_cmd.get_product_by_name(dx)[0])
            xx = False
            for fd in dataprf:
                if float(fd[5]) + float(fd[6]) == float(d[-1]):
                    xx = True
            if xx:
                new_product.append([round(float(d[0]), 1), " ".join(d[1: -1]), d[-1]])
            else:
                text_error = text_cnf["text_daun"]
                return new_product, text_error, False
        new_product2 = []
        for product in new_product:
            new_product2.append([product[0], product[1]])
        for i in range(len(new_product2) - 1):
            for j in range(i + 1, len(new_product2)):
                if new_product2[j][1] == new_product2[i][1]:
                    new_product2[i][0] += new_product2[j][0]
                    new_product2[j][0] = 0
        nnp = []
        for el in new_product2:
            if el[0] != 0:
                # new_product2.remove(el)
                nnp.append(el)
        new_product2 = nnp
        for i in range(len(dataxx) - 1):
            for j in range(i + 1, len(dataxx)):
                if dataxx[j][1] == dataxx[i][1]:
                    dataxx[i][0] += dataxx[j][0]
                    dataxx[j][0] = 0
        nnp = []
        for el in dataxx:
            if el[0] != 0:
                # new_product2.remove(el)
                nnp.append(el)
        dataxx = nnp
        for i in dataxx:
            if not (i in new_product2) and i[0] > 0:
                check = False
                break
        text = ""
        for pr in new_product:
            text += f'{pr[0]} {pr[1]} {text_cnf["price_product1"]} {pr[2]}\n'
        return new_product, text, check
    except:
        return new_product, text_error, False


def check_cur_and_order(order_data, cur_data):
    new_order_data = []
    for product in order_data:
        new_order_data.append([product[0], product[1]])
    for i in range(len(new_order_data) - 1):
        for j in range(i + 1, len(new_order_data)):
            if new_order_data[j][1] == new_order_data[i][1]:
                new_order_data[i][0] += new_order_data[j][0]
                new_order_data[j][0] = 0
    nnp = []
    for el in new_order_data:
        if el[0] != 0:
            nnp.append(el)
    new_order_data = nnp
    new_cur_data = []
    for product in cur_data:
        new_cur_data .append([product[0], product[1]])
    for i in range(len(new_cur_data) - 1):
        for j in range(i + 1, len(new_cur_data)):
            if new_cur_data[j][1] == new_cur_data[i][1]:
                new_cur_data[i][0] += new_cur_data[j][0]
                new_cur_data[j][0] = 0
    nnp = []
    for el in new_cur_data:
        if el[0] != 0:
            nnp.append(el)
    new_cur_data = nnp
    check = True
    for el in new_order_data:
        f = 0
        for el2 in new_cur_data:
            if el[1] == el2[1] and el2[0] < el[0]:
                check = False
                f = 1
            elif el[1] == el2[1] and el2[0] >= el[0]:
                f = 1
        if f == 0:
            check = False
    return check


def eqal(data0, data2):
    summ1 = 0
    summ2 = 0
    data1 = []
    try:
        f = data0[0][2]
        data1 = data0
    except:
        for el in data0:
            f = 0
            for el2 in data2:
                if el[1] == el2[1]:
                    data1.append([el[0], el[1], el2[2]])
                    f = 1
                    break
            if f == 0:
                data1.append([el[0], el[1], db_cmd.get_product_by_name(el[1])[2]])
    for i in data1:
        summ1 += i[0] * float(i[2])
    for j in data2:
        summ2 += j[0] * float(j[2])
    summ = summ1 - summ2
    return summ

def eqal2(data0, data2):
    summ1 = 0
    summ2 = 0
    rez1 = 0
    rez2 = 0
    data1 = []
    try:
        f = data0[0][2]
        data1 = data0
    except:
        for el in data0:
            f = 0
            for el2 in data2:
                if el[1] == el2[1]:
                    data1.append([el[0], el[1], el2[2]])
                    f = 1
                    break
            if f == 0:
                data1.append([el[0], el[1], db_cmd.get_product_by_name(el[1])[2]])
    for i in data1:
        summ1 += i[0] * float(i[2])
        rez1 += i[0] * refill_rezerv(db_cmd.get_product_by_name(i[1])[0], i[2])
    for j in data2:
        summ2 += j[0] * float(j[2])
        rez2 += j[0] * refill_rezerv(db_cmd.get_product_by_name(j[1])[0], j[2])
    summ = summ1 - summ2
    rez = rez1 - rez2
    return summ, rez

def check_order_for_sw2(data, text):
    text_cnf = readJs("text.json")
    dataxx = ast.literal_eval(data[4])["product"]
    check = False
    text_error = text_cnf["text_error_sw_adjust"]
    new_product = []
    try:
        check = True
        text = text.replace('(', '')
        text = text.replace('\n', '')
        datax = text.split(')')
        while '' in datax:
            datax.remove('')
        for el in datax:
            d = el.split(" ")
            if d[0] == '':
                del d[0]
            num = d[0]
            numx = d[-1]
            name = " ".join(d[1: -1])
            if is_number(num) and is_number(numx) and db_cmd.get_product_by_name(name):
                numx = round(float(numx), 1)
                num = round(float(num), 1)
                new_product.append([num, name, numx])
            else:
                text_error += text_cnf["error_in_str"].format(str(el))
                check = False
        if check:
            text_error = ""
            for pr in new_product:
                text_error += f'{pr[0]} {pr[1]} {text_cnf["price_product1"]} {pr[2]}\n'
        return new_product, text_error, check
    except:
        return new_product, text_error, check


def plus_ss(data, all_data):
    for el in data:
        check = True
        for el2 in all_data:
            if el[1] == el2[1] and float(el[2]) == el2[2]:
                el2[0] += el[0]
                check = False
        if check:
            all_data.append([el[0], el[1], float(el[2])])
    return all_data


def minus_ss(data, all_data):
    for el in data:
        check = True
        for el2 in all_data:
            if el[1] == el2[1] and float(el[2]) == el2[2]:
                el2[0] -= el[0]
                check = False
        if check:
            all_data.append([- el[0], el[1], float(el[2])])
    return all_data


def get_text_order_for_courier(data):
    dataxx = ast.literal_eval(data[5])
    text_cnf = readJs("text.json")
    username_courier = db_cmd.get_user_data(data[7])[1]
    type = data[4]
    text_error = text_cnf["number_order"].format(data[0])
    if type == 22 or type == 38:
        typex = text_cnf["type_pickup"]
    elif type == 12 or type == 33:
        typex = text_cnf["type_courier"]
    if type in [38, 33]:
        text_error += text_cnf["order_type_text"].format(typex)
        text_error += text_cnf["courier_username"].format(username_courier)
        text_error += text_cnf["return_order_id"].format(ast.literal_eval(data[5])["order_id"])
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_order3"]
        for product in dataxx["product2"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
    else:
        text_error += text_cnf["order_type_text"].format(typex)
        text_error += text_cnf["courier_username"].format(username_courier)
        text_error += text_cnf["text_order2"].format(
            dataxx["city"], dataxx["street"], dataxx["phone"])
        for product in dataxx["product"]:
            if str(product[0]).split(".")[1] == "0":
                text_error += text_cnf["text_product_in_order"].format(
                    product[1], int(product[0]))
            else:
                text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
        text_error += text_cnf["text_price_and_comment_in_order"].format(
            dataxx["money"], dataxx["comment"])
    return text_error


def check_data_order(text):
    text_cnf = readJs("text.json")

    try:
        text = ' '.join(text.split('\n'))
        text = text.replace('"', '')
        text = text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        i = 0
        n = -1
        k = -1
        p = -1
        for element in data:
            if element.isdigit() and len(element) <= 5:
                if k == -1:
                    k = i  # номер улицы
            elif element.isdigit() and len(element) == 10:
                if n == -1:
                    n = i  # телефон
            elif element.find('₪') >= 0:
                if p == -1:
                    p = i
            i += 1
        street = ''
        town = ''
        product = ''
        comments = ''
        for i in range(0, k + 1):
            street += f'{data[i]} '
        for i in range(k + 1, n):
            town += f'{data[i]} '
        for i in range(n + 1, p):
            if is_number(data[i]):
                product += f',{data[i]}'
            else:
                product += f' {data[i]}'
        for i in range(p + 1, len(data)):
            comments += f' {data[i]}'
        productx = product[1:].split(',')
        pr = []
        for prx in productx:
            pr.append([float(prx[:prx.find(' ')]), prx[prx.find(' ') + 1:]])

        dataxx = {"street": street[:-1], "city": town[:-1],
                  "phone": data[n], "product": pr, "money": data[p][:-1], "comment": comments}
        check_product = check_all_products(pr)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        check_city = db_cmd.check_city(dataxx["city"])
        if not check_city:
            text_error += text_cnf["error_in_name_city"] + dataxx["city"] + "\n"
        checkxx = True
        pll = []
        for plo in pr:
            if not (plo[1] in pll):
                pll.append(plo[1])
            else:
                checkxx = False
                text_error += text_cnf["double_product"].format(plo[1])
        checkfx = False
        if is_number(dataxx["money"]):
            checkfx = True
        else:
            text_error += text_cnf["error_in_money"]
        if check_city and checker and checkxx and checkfx:
            text_error = text_cnf["text_order"].format(
                dataxx["city"], dataxx["street"], dataxx["phone"])
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_price_and_comment_in_order"].format(
                dataxx["money"], dataxx["comment"])
            return True, text_error, dataxx
        else:
            text_error += text_cnf["try_again"]
            return False, text_error, None
    except Exception as e:
        return False, text_cnf["error_in_text_order"], None
        logging.error(f'Error in creat_text: {e}')


def check_data_order3(text):
    text_cnf = readJs("text.json")
    try:
        text = ' '.join(text.split('\n'))
        text = text.replace('"', '')
        text = text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        i = 0
        n = -1
        k = -1
        p = -1
        p2 = -1
        for element in data:
            if element.isdigit() and len(element) <= 5:
                if k == -1:
                    k = i  # номер улицы
            elif element.isdigit() and len(element) == 10:
                if n == -1:
                    n = i  # телефон
            elif element == '#':
                if p == -1:
                    p = i
                else:
                    p2 = i
            i += 1
        street = ''
        town = ''
        product = ''
        comments = ''
        product2 = ''
        for i in range(0, k + 1):
            street += f'{data[i]} '
        for i in range(k + 1, n):
            town += f'{data[i]} '
        for i in range(n + 1, p):
            if is_number(data[i]):
                product += f',{data[i]}'
            else:
                product += f' {data[i]}'
        for i in range(p + 1, p2):
            if is_number(data[i]):
                product2 += f',{data[i]}'
            else:
                product2 += f' {data[i]}'
        for i in range(p2 + 1, len(data)):
            comments += f' {data[i]}'
        productx = product[1:].split(',')
        pr = []
        for prx in productx:
            pr.append([float(prx[:prx.find(' ')]), prx[prx.find(' ') + 1:]])
        productx2 = product2[1:].split(',')
        pr2 = []
        for prx2 in productx2:
            pr2.append([float(prx2[:prx2.find(' ')]), prx2[prx2.find(' ') + 1:]])
        dataxx = {"street": street[:-1], "city": town[:-1],
                  "phone": data[n], "product": pr, "product2": pr2, "comment": comments}
        check_product, check_product2 = check_all_products2(pr, pr2)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        checker2 = True
        for i in range(len(check_product2)):
            if not check_product2[i]:
                text_error += text_cnf["error_in_name_product"] + pr2[i][1] + "\n"
                checker2 = False
        check_city = db_cmd.check_city(dataxx["city"])
        if not check_city:
            text_error += text_cnf["error_in_name_city"] + dataxx["city"] + "\n"
        checkxx = True
        pll = []
        for plo in pr:
            if not (plo[1] in pll):
                pll.append(plo[1])
            else:
                checkxx = False
                text_error += text_cnf["double_product"].format(plo[1])
        if check_city and checker and checker2 and checkxx:
            gramms = 0
            for product in pr:
                if product[1] != "שקל":
                    gramms += product[0]
            text_error = text_cnf["text_order2"].format(
                dataxx["city"], dataxx["street"], dataxx["phone"])
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_order3"]
            for product in pr2:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
            return True, text_error, dataxx
        else:
            text_error += text_cnf["try_again"]
            return False, text_error, None
    except Exception as e:
        return False, text_cnf["error_in_text_order"], None
        logging.error(f'Error in creat_text: {e}')


def check_data_order2(text):
    text_cnf = readJs("text.json")
    try:
        text = ' '.join(text.split('\n'))
        text = text.replace('"', '')
        text = text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        i = 0
        p = -1
        for element in data:
            if element.find('₪') >= 0:
                if p == -1:
                    p = i
            i += 1
        product = ''
        comments = ''
        for i in range(0, p):
            if is_number(data[i]):
                product += f',{data[i]}'
            else:
                product += f' {data[i]}'
        for i in range(p + 1, len(data)):
            comments += f' {data[i]}'
        productx = product[1:].split(',')
        pr = []
        for prx in productx:
            pr.append([float(prx[:prx.find(' ')]), prx[prx.find(' ') + 1:]])

        dataxx = {"street": text_cnf["clear_x"], "city": text_cnf["clear_x"],
                  "phone": text_cnf["clear_x"], "product": pr, "money": data[p][:-1], "comment": comments}
        check_product = check_all_products(pr)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        checkxx = True
        pll = []
        for plo in pr:
            if not (plo[1] in pll):
                pll.append(plo[1])
            else:
                checkxx = False
                text_error += text_cnf["double_product"].format(plo[1])
        checkfx = False
        if is_number(dataxx["money"]):
            checkfx = True
        else:
            text_error += text_cnf["error_in_money"]
        if checker and checkxx and checkfx:
            text_error = text_cnf["text_order"].format(
                dataxx["city"], dataxx["street"], dataxx["phone"])
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_price_and_comment_in_order"].format(
                dataxx["money"], dataxx["comment"])
            return True, text_error, dataxx
        else:
            text_error += text_cnf["try_again"]
            return False, text_error, None
    except Exception as e:
        return False, text_cnf["error_in_text_order"], None
        logging.error(f'Error in creat_text: {e}')


def chek_plus_product(prx, cur_id):
    data = db_cmd.get_user_data(cur_id)
    datax = ast.literal_eval(data[5])["product"]
    for i in prx:
        f = i[0]
        for j in datax:
            if j[1] == i[1]:
                f -= j[0]
        if f > 0:
            return False
    return True


def get_pr_cur_asm(text, cur_id):
    text_cnf = readJs("text.json")
    try:
        text = ' '.join(text.split('\n'))
        text.replace('"', '')
        text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        product = ""
        for i in data:
            if is_number(i):
                product += f',{i}'
            else:
                product += f' {i}'
        pr = []
        productx = product[1:].split(',')
        for prx in productx:
            pr.append([float(prx[:prx.find(' ')]), prx[prx.find(' ') + 1:]])
        check_product = check_all_products(pr)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        if checker:
            text_error += text_cnf["text_order33"]
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            return True, pr, text_error
        else:
            return False, pr, text_error
    except Exception as e:
        return False, [], text_cnf["error_in_text_order"]


def get_pr_cur_asmx(text):
    text_cnf = readJs("text.json")
    try:
        text = ' '.join(text.split('\n'))
        text.replace('"', '')
        text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        product = ""
        for i in data:
            if is_number(i):
                product += f',{i}'
            else:
                product += f' {i}'
        pr = []
        productx = product[1:].split(',')
        for prx in productx:
            pr.append([prx[:prx.find(' ')], float(prx[prx.find(' ') + 1:])])
        check_product = check_all_products(pr)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        if checker:
            text_error += text_cnf["text_order33"]
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            return True, pr, text_error
        else:
            return False, pr, text_error
    except Exception as e:
        return False, [], text_cnf["error_in_text_order"]


def get_profit(order):
    data = ast.literal_eval(order[5])
    product = data['correct_product']
    try:
        cur = float(data['courier'])
    except:
        cur = 0
    try:
        mx = ''
        for i in data['money']:
            if i.isdigit() or i == '-':
                mx += i
        money = float(mx)
    except:
        money = 0
    product_price = 0
    for pr in product:
        try:
            product_price += float(pr[0]) * float(pr[2])
        except:
            if pr[1] == "שקל":
                product_price += float(pr[0])
    profit = money - product_price - cur

    return money, profit, product_price, cur


def get_profit_rezerv(order):
    data = ast.literal_eval(order[5])
    product = data['correct_product']
    try:
        cur = float(data['courier'])
        d1 = datetime.datetime.strptime(order[9], '%Y-%m-%d %H:%M:%S.%f')
        d0 = datetime.datetime.strptime(order[8], '%Y-%m-%d %H:%M:%S.%f')
        delta = (d1-d0).total_seconds()
        if cur < 100 and delta < 3600 and cur != 0 and data['city'] != 'פתח תקווה':
            cur = 100
            data['courier'] = 100
            db_cmd.update_order(order[0], 'data', str(data))
    except:
        cur = 0
    try:
        mx = ''
        for i in data['money']:
            if i.isdigit() or i == '-':
                mx += i
        money = float(mx)
    except:
        money = 0
    product_price = 0
    rezerv = 0
    for pr in product:
        try:
            product_price += float(pr[0]) * float(pr[2])
            rezerv += refill_rezerv(db_cmd.get_product_by_name(pr[1])[0], pr[2]) * float(pr[0])
        except:
            if pr[1] == "שקל":
                product_price += float(pr[0])
    profit = money - product_price - cur

    return money, profit, product_price, cur, rezerv

def get_profit_alt(order):
    data = ast.literal_eval(order[5])
    product = data['correct_product']
    try:
        cur = float(data['courier'])
    except:
        cur = 0
    
    try:
        mx = ''
        for i in data['money']:
            if i.isdigit() or i == '-':
                mx += i
        money = float(mx)
    except:
        money = 0
    product_price = 0
    for pr in product:
        try:
            product_price += float(pr[0]) * float(pr[2])
        except:
            if pr[1] == "שקל":
                product_price += float(pr[0])
    profit = money - product_price - cur

    return money, profit, product_price, cur


def check_type_order(product):
    f = True
    fpr = []
    productx = []
    for el in product:
        if float(el[0]) < 0:
            f = False
            productx.append([float(el[0]) * -1, el[1]])
        else:
            productx.append([float(el[0]), el[1]])
    return productx, f


def get_profit_exchange(order):
    data = ast.literal_eval(order[5])
    product = data['correct_product']
    try:
        cur = float(data['courier'])
    except:
        cur = 0
    product_price = 0
    money = 0
    for pr in product:
        if pr[1] != "שקל":
            product_price -= float(pr[0]) * float(pr[2])
        else:
            money -= float(pr[0])
    product2 = data["true_product"]
    for el in product2:
        if el[1] != "שקל":
            product_price += float(el[0]) * float(el[2])
        else:
            money += int(el[0])
    try:
        x, yprofit, z, w = get_profit(db_cmd.get_order_by_order_id(data['order_id']))
    except:
        try:
            x, yprofit, z, w = get_profit(db_cmd.get_order_by_order_id(data['connect']))
        except:
            yprofit = 0
    profit = money - cur + product_price
    if yprofit + profit >= 0:
        check = True
    else:
        check = False
    return profit, - product_price, cur, check

def refill_rezerv(id_product, price):
    ref_l = db_cmd.get_product_refill_active_next(id_product)
    for ref in ref_l:
        if float(ref[5]) + float(ref[6]) == float(price):
            return float(ref[6])
    return 0

def get_profit_exchange2(order):
    data = ast.literal_eval(order[5])
    product = data['correct_product']
    try:
        cur = float(data['courier'])
        d1 = datetime.datetime.strptime(order[9], '%Y-%m-%d %H:%M:%S.%f')
        d0 = datetime.datetime.strptime(order[8], '%Y-%m-%d %H:%M:%S.%f')
        delta = (d1-d0).total_seconds()
        if cur < 100 and delta < 3600 and cur != 0 and data['city'] != 'פתח תקווה':
            cur = 100
            data['courier'] = 100
            db_cmd.update_order(order[0], 'data', str(data))
    except:
        cur = 0
    product_price = 0
    rezerv = 0
    money = 0
    for pr in product:
        if pr[1] != "שקל":
            product_price -= float(pr[0]) * float(pr[2])
            print(db_cmd.get_product_by_name(pr[1]), pr[1])
            rezerv -= refill_rezerv(db_cmd.get_product_by_name(pr[1])[0], pr[2]) * float(pr[0])
        else:
            money -= float(pr[0])
    product2 = data["true_product"]
    for el in product2:
        if el[1] != "שקל":
            product_price += float(el[0]) * float(el[2])
            rezerv += refill_rezerv(db_cmd.get_product_by_name(el[1])[0], el[2]) * float(el[0])
        else:
            money += int(el[0])
    try:
        x, yprofit, z, w, r = get_profit_rezerv(db_cmd.get_order_by_order_id(data['order_id']))
    except:
        try:
            x, yprofit, z, w, r = get_profit_rezerv(db_cmd.get_order_by_order_id(data['connect']))
        except:
            yprofit = 0
    profit = money - cur + product_price
    if yprofit + profit >= 0:
        check = True
    else:
        check = False
    return profit, - product_price, cur, check, - rezerv


def check_data_order4(text):
    text_cnf = readJs("text.json")
    try:
        text = ' '.join(text.split('\n'))
        text = text.replace('"', '')
        text = text.replace("'", "")
        data = text.split(' ')
        while '' in data:
            data.remove('')
        i = 0
        p = -1
        p2 = -1
        for element in data:
            if element == '#':
                if p == -1:
                    p = i
                else:
                    p2 = i
            i += 1
        product = ''
        comments = ''
        product2 = ''
        for i in range(0, p):
            if is_number(data[i]):
                product += f',{data[i]}'
            else:
                product += f' {data[i]}'
        for i in range(p + 1, p2):
            if is_number(data[i]):
                product2 += f',{data[i]}'
            else:
                product2 += f' {data[i]}'
        for i in range(p2 + 1, len(data)):
            comments += f' {data[i]}'
        productx = product[1:].split(',')
        pr = []
        for prx in productx:
            pr.append([float(prx[:prx.find(' ')]), prx[prx.find(' ') + 1:]])
        checkxx = True
        pll = []
        for plo in pr:
            if not (plo[1] in pll):
                pll.append(plo[1])
            else:
                checkxx = False
                text_error += text_cnf["double_product"].format(plo[1])

        productx2 = product2[1:].split(',')
        pr2 = []
        for prx2 in productx2:
            pr2.append([float(prx2[:prx2.find(' ')]), prx2[prx2.find(' ') + 1:]])
        dataxx = {"street": text_cnf["clear_x"], "city": text_cnf["clear_x"],
                  "phone": text_cnf["clear_x"], "product": pr, "product2": pr2, "comment": comments}
        check_product, check_product2 = check_all_products2(pr, pr2)
        text_error = ''
        checker = True
        for i in range(len(check_product)):
            if not check_product[i]:
                text_error += text_cnf["error_in_name_product"] + pr[i][1] + "\n"
                checker = False
        checker2 = True
        for i in range(len(check_product2)):
            if not check_product2[i]:
                text_error += text_cnf["error_in_name_product"] + pr2[i][1] + "\n"
                checker2 = False
        if checker and checker2 and checkxx:
            gramms = 0
            for product in pr:
                if product[1] != "שקל":
                    gramms += product[0]
            text_error = text_cnf["text_order2"].format(
                dataxx["city"], dataxx["street"], dataxx["phone"])
            for product in pr:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_order3"]
            for product in pr2:
                if str(product[0]).split(".")[1] == "0":
                    text_error += text_cnf["text_product_in_order"].format(
                        product[1], int(product[0]))
                else:
                    text_error += text_cnf["text_product_in_order"].format(product[1], product[0])
            text_error += text_cnf["text_comment_in_order"].format(dataxx["comment"])
            return True, text_error, dataxx
        else:
            text_error += text_cnf["try_again"]
            return False, text_error, None
    except Exception as e:
        return False, text_cnf["error_in_text_order"], None
        logging.error(f'Error in creat_text: {e}')
