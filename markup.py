from telebot import types
import db_cmd
import dopf
import ast


def menu_sales_manager(user_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["new_order_sm"], callback_data="new_order_sm")
    markup.add(btn1)
    data = db_cmd.get_active_order_sm(user_id)
    if data:
        btn0 = types.InlineKeyboardButton(
            text_cnf["active_order_courier"], callback_data="active_order_sm")
        markup.add(btn0)
    btn2 = types.InlineKeyboardButton(
        text_cnf["history_order_sm"], callback_data="history_order_sm")
    markup.add(btn2)
    btn4 = types.InlineKeyboardButton(
        text_cnf["history_order_sm2"], callback_data="history_order_sm2")
    markup.add(btn4)
    btn3 = types.InlineKeyboardButton(
        text_cnf["earnings_sm"], callback_data="earnings_sm")
    markup.add(btn3)
    btn5 = types.InlineKeyboardButton(
        text_cnf["goods_stock"], callback_data="goods_stock")
    markup.add(btn5)
    return markup


def main_sm_earning():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    '''btn2 = types.InlineKeyboardButton(
        text_cnf["creat_report_sm"], callback_data="creat_report_sm")'''
    markup.add(btn1)
    return markup


def menu_manager_courier_and_pickup():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["courier_management"], callback_data="courier_management")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["mass_message_mng"], callback_data="mass_message_mng")
    markup.add(btn2)
    btn3 = types.InlineKeyboardButton(
        text_cnf["mass_message_cur"], callback_data="mass_message_cur")
    markup.add(btn3)
    btn4 = types.InlineKeyboardButton(
        text_cnf["add_city"], callback_data="add_city")
    markup.add(btn4)
    btn5 = types.InlineKeyboardButton(
        text_cnf["comeback_order"], callback_data="comeback_order")
    markup.add(btn5)
    btn6 = types.InlineKeyboardButton(
        text_cnf["cur_ordes_reposts"], callback_data="corr#0")
    markup.add(btn6)
    btn7 = types.InlineKeyboardButton(
        text_cnf["goods_cur"], callback_data="goods_cur")
    markup.add(btn7)
    btn8 = types.InlineKeyboardButton(
        text_cnf["general_report"], callback_data="general_report")
    markup.add(btn8)
    btn9 = types.InlineKeyboardButton(
        text_cnf["complete_order"], callback_data="complete_order")
    markup.add(btn9)
    btn10 = types.InlineKeyboardButton(
        text_cnf["change_order_money"], callback_data="change_order_money")
    markup.add(btn10)
    return markup


def menu_top_mng():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["courier_management"], callback_data="courier_management")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(                           
        text_cnf["mass_message_mng"], callback_data="mass_message_mng")
    markup.add(btn2)                                                  
    btn5 = types.InlineKeyboardButton(
        text_cnf["comeback_order"], callback_data="comeback_order")
    markup.add(btn5)
    btn9 = types.InlineKeyboardButton(
        text_cnf["complete_order"], callback_data="complete_order")
    markup.add(btn9)
    btn10 = types.InlineKeyboardButton(
        text_cnf["change_order_money"], callback_data="change_order_money")
    markup.add(btn10)
    btn6 = types.InlineKeyboardButton(
        text_cnf["cur_ordes_reposts"], callback_data="corr#0")
    markup.add(btn6)
    btn7 = types.InlineKeyboardButton(
        text_cnf["goods_cur"], callback_data="goods_cur")
    markup.add(btn7)
    btn8 = types.InlineKeyboardButton(
        text_cnf["general_report"], callback_data="general_report")
    markup.add(btn8)
    return markup                                          

def mng_cur_menu():
    text_cnf = dopf.readJs("text.json")
    cur_x = dopf.readJs("courier.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    cur = db_cmd.get_user_data_by_role(8)
    pickup = db_cmd.get_user_data_by_role(9)
    for el in cur:
        btn = types.InlineKeyboardButton(
            text_cnf["text_cur_mng"].format(el[1]), callback_data=f"switch#{el[0]}")
        if cur_x["courier"] != el[0]:
            btnx = types.InlineKeyboardButton(
                text_cnf["auto_cur"].format(el[1]), callback_data=f"sjubf#{el[0]}")
        else:
            btnx = types.InlineKeyboardButton(
                text_cnf["cnl_auto_cur"].format(el[1]), callback_data=f"sjubf#0")
        markup.add(btn)
        markup.add(btnx)
    for el in pickup:
        btn = types.InlineKeyboardButton(
            text_cnf["text_pickup_mng"].format(el[1]), callback_data=f"switch#{el[0]}")
        btn2 = types.InlineKeyboardButton(
            text_cnf["text_plus_zp"].format(el[1]), callback_data=f"xluszp#{el[0]}")
        markup.add(btn, btn2)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def mng_worker_menu():
    text_cnf = dopf.readJs("text.json")
    worker_x = dopf.readJs("worker.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    workers = db_cmd.get_user_data_by_role(10)
    for el in workers:
        if worker_x["worker"] != el[0]:
            btnx = types.InlineKeyboardButton(
                text_cnf["auto_worker"].format(el[1]), callback_data=f"kjubf#{el[0]}")
        else:
            btnx = types.InlineKeyboardButton(
                text_cnf["cnl_auto_worker"].format(el[1]), callback_data=f"kjubf#0")
        markup.add(btnx)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def report_cur_kb(uid):
    text_cnf = dopf.readJs("text.json")
    worker_x = dopf.readJs("worker.json")
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in [8, 9]:
        curs = db_cmd.get_user_data_by_role(i)
        for el in curs:
            if uid != el[0]:
                btnx = types.InlineKeyboardButton(f"@{el[1]}", callback_data=f"corr#{el[0]}")
                btnx2 = types.InlineKeyboardButton(f"ystrd:@{el[1]}", callback_data=f"cxrr#{el[0]}")
                markup.row(btnx, btnx2)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.row(btn1)
    return markup


def mng_cur_menu2(user_id):
    text_cnf = dopf.readJs("text.json")
    cur_x = dopf.readJs("courier.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    cur = db_cmd.get_user_data_by_role(8)
    pickup = db_cmd.get_user_data_by_role(9)
    for el in cur:
        btn = types.InlineKeyboardButton(
            text_cnf["text_cur_mng"].format(el[1]), callback_data=f"switch#{el[0]}")
        if cur_x["courier"] != el[0]:
            btnx = types.InlineKeyboardButton(
                text_cnf["auto_cur"].format(el[1]), callback_data=f"sjubf#{el[0]}")
        else:
            btnx = types.InlineKeyboardButton(
                text_cnf["cnl_auto_cur"].format(el[1]), callback_data=f"sjubf#0")
        markup.add(btn)
        markup.add(btnx)
    for el in pickup:
        btn = types.InlineKeyboardButton(
            text_cnf["text_pickup_mng"].format(el[1]), callback_data=f"switch#{el[0]}")
        if el[0] == user_id:
            btn2 = types.InlineKeyboardButton(
                text_cnf["text_plus_zp2"].format(el[1]), callback_data=f"pluszp#{el[0]}")
        else:
            btn2 = types.InlineKeyboardButton(
                text_cnf["text_plus_zp"].format(el[1]), callback_data=f"xluszp#{el[0]}")
        markup.add(btn, btn2)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def delivery_officer_kb():
    text_cnf = dopf.readJs("text.json")
    cur_x = dopf.readJs("courier.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    cur = db_cmd.get_user_data_by_role(8)
    pickup = db_cmd.get_user_data_by_role(9)
    for el in cur:
        bank = db_cmd.get_user_bank(el[0])[1]
        money = ast.literal_eval(db_cmd.get_user_data(el[0])[5])["product"][0][0]
        need_comeback = round(float(money) - float(bank), 2)
        btn = types.InlineKeyboardButton(
            text_cnf["comeback_money_text"].format(el[1], need_comeback), callback_data=f"mxm#{el[0]}")
        markup.add(btn)
    for el in pickup:
        bank = db_cmd.get_user_bank(el[0])[1]
        money = ast.literal_eval(db_cmd.get_user_data(el[0])[5])["product"][0][0]
        need_comeback = round(float(money) - float(bank), 2)
        btn = types.InlineKeyboardButton(
            text_cnf["comeback_money_text"].format(el[1], money), callback_data=f"mxm#{el[0]}")
        markup.add(btn)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def menu_storage_manager():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["control_storage_worker"], callback_data="control_storage_worker")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["mass_message_mng"], callback_data="mass_message_mng")
    markup.add(btn2)
    btn3 = types.InlineKeyboardButton(
        text_cnf["warehouse_consumption"], callback_data="warehouse_consumption")
    markup.add(btn3)
    btn4 = types.InlineKeyboardButton(
        text_cnf["mass_message_cur"], callback_data="mass_message_cur")
    markup.add(btn4)
    btn5 = types.InlineKeyboardButton(
        text_cnf["auto_storage_worker"], callback_data="auto_storage_worker")
    markup.add(btn5)
    btn6 = types.InlineKeyboardButton(
        text_cnf["comeback_order_w"], callback_data="comeback_order_w")
    markup.add(btn6)
    btn7 = types.InlineKeyboardButton(
        text_cnf["goods_cur"], callback_data="goods_cur")
    markup.add(btn7)
    btn8 = types.InlineKeyboardButton(
        text_cnf["supply_chain_management"], callback_data="supchainmng")
    markup.add(btn8)
    return markup


def menu_supplies():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["working_supplies"], callback_data="working_supplies")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["range"], callback_data="range")
    markup.add(btn2)
    btn3 = types.InlineKeyboardButton(
        text_cnf["reserve_management"], callback_data="reserve_management")
    markup.add(btn3)
    btn5 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn5)
    return markup


def supply_map():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=2)
    data = db_cmd.get_products_refill_all_work()
    btn1 = types.InlineKeyboardButton(
        text_cnf["new_supply"], callback_data="new_supply")
    btn0 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="supchainmng")
    x = len(data)
    mass = []
    for i in range(x):
        el = data[i]
        name = db_cmd.get_product_by_num(el[1])[1]
        btn2 = types.InlineKeyboardButton(
            text_cnf["refill_btn_to"].format(el[2], el[3], el[4]), callback_data=f"tgy#{el[0]}")
        if el[7] == 0:
            x = "❌"
            y = 1
        elif el[7] == 1:
            x = "✅"
            y = 0
        btn3 = types.InlineKeyboardButton(
            text_cnf["refill_btn_price"].format(str(name), el[5], el[6], x), callback_data=f"zod{el[0]}#{y}")
        mass.append(btn2)
        mass.append(btn3)
    markup.add(*mass)
    markup.row(btn1)
    markup.row(btn0)
    return markup


def product_map():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=2)
    data = db_cmd.get_product_all()
    x = len(data)
    btn1 = types.InlineKeyboardButton(
        text_cnf["new_product_stm"], callback_data="new_product_stm")
    btn0 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="supchainmng")
    mass = []
    for i in range(x):
        el = data[i]
        if el[3] == 0:
            x = "❌"
            y = 1
        elif el[3] == 1:
            x = "✅"
            y = 0
        btn2 = types.InlineKeyboardButton(
            text_cnf["product_stm"].format(el[1], el[2], x), callback_data=f"tgn{el[0]}#{y}")
        mass.append(btn2)
    markup.add(*mass)
    markup.row(btn1)
    markup.row(btn0)
    return markup


def mng_worker_kb():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    worker = db_cmd.get_user_data_by_role(10)
    for el in worker:
        btn = types.InlineKeyboardButton(
            text_cnf["text_plus_worker"].format(el[1]), callback_data=f"zpm#{el[0]}")
        markup.add(btn)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def cur_cur_order_kb():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(
        text_cnf["report_cur_cur_ystd"], callback_data="report_cur_cur_ystd")
    markup.add(btn)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def cur_cur_order_kb2():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(
        text_cnf["report_cur_cur"], callback_data="report_cur_cur")
    markup.add(btn)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def menu_cnlwhx():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["rewhx"], callback_data="rewhx")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["cnlwhx"], callback_data="cnlwhx")
    markup.add(btn2)
    return markup


def cloesed_order_sm_kb(order_id):
    text_cnf = dopf.readJs("text.json")
    if db_cmd.get_order_by_order_id(order_id)[3] == 3:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(
            text_cnf["exchange_return"], callback_data=f"exchangesm{order_id}")
        markup.add(btn1)
        return markup
    else:
        return None


def menu_courier(user_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = db_cmd.check_new_order_courier(user_id)
    if data:
        btn1 = types.InlineKeyboardButton(
            text_cnf["new_order_courier"], callback_data="new_order_cr")
        markup.add(btn1)
    data2 = db_cmd.get_complite_order_warehouse(user_id)
    if data2:
        btn0 = types.InlineKeyboardButton(
            text_cnf["complite_storage_order"], callback_data="complite_storage_order")
        markup.add(btn0)
    data3 = db_cmd.check_active_order_courier(user_id)
    if data3:
        btn2 = types.InlineKeyboardButton(
            text_cnf["active_order_courier"], callback_data="active_order_courier")
        markup.add(btn2)
    btn3 = types.InlineKeyboardButton(
        text_cnf["completed_order_courier"], callback_data="completed_order_courier")
    markup.add(btn3)
    btn5 = types.InlineKeyboardButton(
        text_cnf["now_products_courier"], callback_data="now_products_courier")
    markup.add(btn5)
    btn6 = types.InlineKeyboardButton(
        text_cnf["report_cur_cur"], callback_data="report_cur_cur")
    markup.add(btn6)
    return markup


def closed_order_kb_c(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    order_data = db_cmd.get_order_by_order_id(order_id)
    dtx = ast.literal_eval(order_data[5])
    try:
        stk = dtx["stk"]
        if stk == 0:
            btn0 = types.InlineKeyboardButton(
                text_cnf["true_return"], callback_data=f"right#{order_id}")
            markup.add(btn0)
            return markup
    except:
        pass
    return None


def complite_order_w(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn0 = types.InlineKeyboardButton(
        text_cnf["product_get_confirm"], callback_data=f"csoc{order_id}")
    markup.add(btn0)
    return markup


def menu_storage(user_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = db_cmd.check_new_order_sw(user_id)
    if data:
        btn1 = types.InlineKeyboardButton(
            text_cnf["active_order_courier"], callback_data="active_order_storage_w")
        markup.add(btn1)
    '''
    btn2 = types.InlineKeyboardButton(
        text_cnf["storage_now"], callback_data="storage_now")
    btn3 = types.InlineKeyboardButton(
        text_cnf["casting"], callback_data="casting")
    btn4 = types.InlineKeyboardButton(
        text_cnf["earnings_sm"], callback_data="earnings_sw")
    markup.add(btn2, btn3, btn4)'''
    return markup


def menu_cashier():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["workon_with_kur"], callback_data="workon_with_kur")
    markup.add(btn1)
    return markup


def menu_accountant():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["workon_with_cashier"], callback_data="workon_with_cashier")
    markup.add(btn1)
    return markup


def backpuck_cr_kb(user_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["return_backpuck"], callback_data="return_backpuck")
    markup.add(btn1)
    btn4 = types.InlineKeyboardButton(
        text_cnf["get_products_courier"], callback_data="getproducts_courier")
    markup.add(btn4)
    cur_backpuck = ast.literal_eval(
        db_cmd.get_user_data(user_id)[5])["product"]
    text, money, bank = dopf.cur_backpuck_text(cur_backpuck, user_id)
    state = db_cmd.get_user_data(user_id)[2]
    if money >= bank and bank > 0 and state == 51:
        btn2 = types.InlineKeyboardButton(
            text_cnf["xget_cash_cur"], callback_data="get_cash_cur")
        markup.add(btn2)
    elif money >= bank and bank > 0:
        btn2 = types.InlineKeyboardButton(
            text_cnf["get_cash_cur"], callback_data="get_cash_cur")
        markup.add(btn2)
    return markup


def backpuck_cr_kb2(user_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn4 = types.InlineKeyboardButton(
        text_cnf["get_products_courier"], callback_data="getproducts_courier")
    markup.add(btn4)
    return markup


def confirm_s_request():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn4 = types.InlineKeyboardButton(
        text_cnf["confirm_sm"], callback_data="takeprconf")
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn4, btn1)
    return markup


def active_order_cr_kb(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data_order = db_cmd.get_order_by_order_id(order_id)
    data = ast.literal_eval(data_order[5])
    if len(data["product"]) == 1 and data["product"][0][1] == "שקל":
        pass
    else:
        try:
            if data["correct_product"]:
                pass
        except:
            if data_order[6] != 2:
                btn0 = types.InlineKeyboardButton(
                    text_cnf["get_product_by_order_now"], callback_data=f"get_product{order_id}")
                markup.add(btn0)
    if data_order[4] in [12, 33]:
        btnx = types.InlineKeyboardButton(
            text_cnf["kurwin"], callback_data=f"kurwin{order_id}")
        markup.add(btnx)
    btn1 = types.InlineKeyboardButton(
        text_cnf["car_crash_in_active_order"], callback_data=f"xar_crash{order_id}")
    btn2 = types.InlineKeyboardButton(
        text_cnf["client_cancel_order"], callback_data=f"xlient_cancel{order_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["order_courier_confirm"], callback_data=f"order_confirm{order_id}")
    btn4 = types.InlineKeyboardButton(
        text_cnf["cancel_order_courier"], callback_data=f"xaoc{order_id}")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def active_order_cr_kb2(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data_order = db_cmd.get_order_by_order_id(order_id)
    data = ast.literal_eval(data_order[5])
    if len(data["product"]) == 1 and data["product"][0][1] == "שקל":
        pass
    else:
        try:
            if data["correct_product"]:
                pass
        except:
            if data_order[6] != 2:
                btn0 = types.InlineKeyboardButton(
                    text_cnf["get_product_by_order_now"], callback_data=f"get_product{order_id}")
                markup.add(btn0)
    if data_order[4] in [12, 33]:
        btnx = types.InlineKeyboardButton(
            text_cnf["kurwin"], callback_data=f"kurwin{order_id}")
        markup.add(btnx)
    btn1 = types.InlineKeyboardButton(
        text_cnf["car_crash_in_active_order"], callback_data=f"xar_crash{order_id}")
    btn2 = types.InlineKeyboardButton(
        text_cnf["confirm_btm_sw"], callback_data=f"client_cancel{order_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["order_courier_confirm"], callback_data=f"order_confirm{order_id}")
    btn4 = types.InlineKeyboardButton(
        text_cnf["cancel_order_courier"], callback_data=f"xaoc{order_id}")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def active_order_cr_kb3(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data_order = db_cmd.get_order_by_order_id(order_id)
    data = ast.literal_eval(data_order[5])
    if len(data["product"]) == 1 and data["product"][0][1] == "שקל":
        pass
    else:
        try:
            if data["correct_product"]:
                pass
        except:
            if data_order[6] != 2:
                btn0 = types.InlineKeyboardButton(
                    text_cnf["get_product_by_order_now"], callback_data=f"get_product{order_id}")
                markup.add(btn0)
    if data_order[4] in [12, 33]:
        btnx = types.InlineKeyboardButton(
            text_cnf["kurwin"], callback_data=f"kurwin{order_id}")
        markup.add(btnx)
    btn1 = types.InlineKeyboardButton(
        text_cnf["car_crash_in_active_order"], callback_data=f"xar_crash{order_id}")
    btn2 = types.InlineKeyboardButton(
        text_cnf["client_cancel_order"], callback_data=f"xlient_cancel{order_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["order_courier_confirm"], callback_data=f"order_confirm{order_id}")
    btn4 = types.InlineKeyboardButton(
        text_cnf["confirm_btm_sw"], callback_data=f"caoc{order_id}")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def active_order_cr_kb4(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data_order = db_cmd.get_order_by_order_id(order_id)
    data = ast.literal_eval(data_order[5])
    if len(data["product"]) == 1 and data["product"][0][1] == "שקל":
        pass
    else:
        try:
            if data["correct_product"]:
                pass
        except:
            if data_order[6] != 2:
                btn0 = types.InlineKeyboardButton(
                    text_cnf["get_product_by_order_now"], callback_data=f"get_product{order_id}")
                markup.add(btn0)
    if data_order[4] in [12, 33]:
        btnx = types.InlineKeyboardButton(
            text_cnf["kurwin"], callback_data=f"kurwin{order_id}")
        markup.add(btnx)
    btn1 = types.InlineKeyboardButton(
        text_cnf["car_crash_in_active_order"], callback_data=f"car_crash{order_id}")
    btn2 = types.InlineKeyboardButton(
        text_cnf["client_cancel_order"], callback_data=f"xlient_cancel{order_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["order_courier_confirm"], callback_data=f"order_confirm{order_id}")
    btn4 = types.InlineKeyboardButton(
        text_cnf["confirm_btm_sw"], callback_data=f"xaoc{order_id}")
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def active_order_sw(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = ast.literal_eval(db_cmd.get_order_warehouse_by_id(order_id)[4])
    btn0 = types.InlineKeyboardButton(
        text_cnf["order_w_courier_confirm"], callback_data=f"order_sw_confirm{order_id}")
    markup.add(btn0)
    btn1 = types.InlineKeyboardButton(
        text_cnf["adjust_delivery"], callback_data=f"adjust_delivery{order_id}")
    markup.add(btn1)
    return markup


def active_order_sw2(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["take_product_cur"], callback_data=f"takeprcur{order_id}")
    markup.add(btn1)
    return markup


def change_pay_cur(type, money, order_id):
    if type == 22:
        return None
    else:
        text_cnf = dopf.readJs("text.json")
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(
            text_cnf["change_price_dlv"].format(money), url=f"t.me/{text_cnf['bot_name']}?start=chngpr{order_id}")
        markup.add(btn1)
        return markup


def set_price_cur(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=4)
    price_lsit = text_cnf["price_cur_list"]
    mb = []
    for i in price_lsit:
        btn1 = types.InlineKeyboardButton(
            f'{i} ₪', callback_data=f"cpn#{i}#{order_id}")
        mb.append(btn1)
    markup.add(*mb)
    return markup


def client_now(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = db_cmd.get_order_by_order_id(order_id)
    if data[3] == 2 and data[4] == 22:
        btn0 = types.InlineKeyboardButton(
            text_cnf["client_now"], callback_data=f"client_now{order_id}")
        markup.add(btn0)
    btn1 = types.InlineKeyboardButton(
        text_cnf["edit_order_sm"], callback_data=f"editsm{order_id}")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["dlt_order_sm"], callback_data=f"smdlt{order_id}")
    markup.add(btn2)
    return markup


def courier_order_kb(order):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn3 = types.InlineKeyboardButton(
        text_cnf["confirm_order_courier"], callback_data=f"cooc{order[0]}#0")
    btn4 = types.InlineKeyboardButton(
        text_cnf["cancel_order_courier"], callback_data=f"caoc{order[0]}")
    markup.add(btn3, btn4)
    return markup


def confirm_dlt_sm(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn3 = types.InlineKeyboardButton(
        text_cnf["confirm_dlt_sm2"], callback_data=f"confirmdltsm{order_id}")
    markup.add(btn3)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def select_courier_or_pickup(type, order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    if type == 12 or type == 33 or type == 17 or type == 43:
        x_type = 8
    elif type == 22 or type == 38 or type == 27 or type == 48:
        x_type = 9
    data = db_cmd.get_users_for_delivery(x_type)
    for user in data:
        btn = types.InlineKeyboardButton(
            f"@{user[1]}", callback_data=f"dlv{user[0]}")
        markup.add(btn)
    btn_pre_last = types.InlineKeyboardButton(
        text_cnf["manager_connect"], url=f"t.me/{text_cnf['bot_name']}?start=sndmsg{order_id}")
    markup.add(btn_pre_last)
    btn_last = types.InlineKeyboardButton(
        text_cnf["cancel_order_mc"], url=f"t.me/{text_cnf['bot_name']}?start=cnlorder{order_id}")
    markup.add(btn_last)
    return markup


def comment_to_cancel(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_last = types.InlineKeyboardButton(
        text_cnf["comment_to_cancel"], url=f"t.me/{text_cnf['bot_name']}?start=ccnlorder{order_id}")
    markup.add(btn_last)
    return markup


def main_menu():
    return None


def select_storage_worker(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = db_cmd.get_users_for_delivery(10)
    for user in data:
        btn = types.InlineKeyboardButton(
            f"@{user[1]}", callback_data=f"strg{user[0]}")
        markup.add(btn)
    btn2 = types.InlineKeyboardButton(
        text_cnf["cnlwhx"], callback_data="cnlwhx")
    markup.add(btn2)
    return markup


def select_storage_worker2(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    data = db_cmd.get_users_for_delivery(10)
    for user in data:
        btn = types.InlineKeyboardButton(
            f"@{user[1]}", callback_data=f"rtrn{user[0]}")
        markup.add(btn)
    btn2 = types.InlineKeyboardButton(
        text_cnf["cnlwhx"], callback_data="cnlwhx")
    markup.add(btn2)
    return markup


def recourier_order(order_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["recourier"], callback_data="redlv")
    btn2 = types.InlineKeyboardButton(
        text_cnf["manager_connect"], url=f"t.me/{text_cnf['bot_name']}?start=sndmsg{order_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["cancel_order_mc"], url=f"t.me/{text_cnf['bot_name']}?start=cnlorder{order_id}")
    markup.add(btn1, btn2, btn3)
    return markup


def select_type_delivery():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["courier_sm"], callback_data="courier_sm")
    btn2 = types.InlineKeyboardButton(
        text_cnf["pickup_sm"], callback_data="pickup_sm")
    btn3 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1, btn2, btn3)
    return markup


def back_sm():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_sm")
    markup.add(btn1)
    return markup


def main_sm():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup

def main_refill(element_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["change_scope_delivery"], callback_data=f"csr#{element_id}")
    btn2 = types.InlineKeyboardButton(
        text_cnf["correct_save_refill"], callback_data=f"csd#{element_id}")
    btn3 = types.InlineKeyboardButton(
        text_cnf["convert_to_waste"], callback_data=f"ctw#{element_id}")
    btn0 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="working_supplies")
    markup.add(btn1, btn2, btn3, btn0)
    return markup

def editprice_refill_kb(element_id):
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn0 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data=f"tgy#{element_id}")
    markup.add(btn0)
    return markup

def confirm_cashir_operation():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(
        text_cnf["confirm_btm_sw"], callback_data="trucash")
    markup.add(btn)
    btn1 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn1)
    return markup


def confirm_order_sm():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["confirm_sm"], callback_data="confirm_sm")
    btn2 = types.InlineKeyboardButton(
        text_cnf["try_sm"], callback_data="try_sm")
    btn3 = types.InlineKeyboardButton(
        text_cnf["cancel_sm"], callback_data="cancel_sm")
    markup.add(btn1, btn2, btn3)
    return markup


def cancel_order_sm():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["cancel_sm"], callback_data="cancel_sm")
    markup.add(btn1)
    return markup


def confirm_sw():
    text_cnf = dopf.readJs("text.json")
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text_cnf["confirm_btm_sw"], callback_data="confirm_sw_order")
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(
        text_cnf["back_sm"], callback_data="back_main_sm")
    markup.add(btn2)
    return markup
