import sqlite3
import ast
import random
import datetime
import logging
import time

# 100 Ошибка при добавлении кода
# 101 Ошибка при проверке на наличе кодов
# 102 Проверка активированого кода
# 103 Провекра неактивированого кода
# 104 Присвоение коду пользователя
# 200 Ошибка при добавлении пользователя
# 201 Ошибка при проверке на наличие пользователя в бд
# 202 Ошибка при присваинвании типа пользователя
# 203 Ошибка при взятии карты пользователя
# 204 Ошибка при обновлении карточки пользователя
# 205 Ошибка при взятие активных курьеров/мастеров самовывоза
# 300 Ошибка при проверки товара
# 301 Ошибка при взятие базы всех товаров
# 400 Ошибка при проверки города
# 401 Ошибка при взятии данных по городу
# 500 Ошибка при создании нового заказа
# 501 Ошибка при проверке наличия новго заказа у курьера
# 502 Ошибка при взятие последнего заказа менеджера
# 503 Ошибка при обновлении заказа
# 505 Ошибка при присваивании курьера заказу
# 504 Ошибка при взятие заказа по сообщению и типу доставки
# 506 Ошибка при взятие заказа по идентификатору
# 507 Ошибка при проверке наличия активного заказа у курьера
# 600 Ошибка при создании нового заказа по складу
# 601 Ошибка при взятие последнего заказа курьера по складу
# 602 Ошибка при взятие заказа по id сообщения по складу
# 700 Ошибка при добавлении сообщения в базу на удаление
# 701 Ошибка при взятие сообщений из базы на удаление
# 702 Ошибка при удалении сообщений из базы на удаление

logging.basicConfig(format='%(asctime)s | %(process)d-%(levelname)s-%(message)s',
                    level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')


def create_tables():
    db_file = "db.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # status: 0 - новый, 1 - активированый, 2 - деактивированный, 3..4..5 - штраф 1..2..3
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS users(
                            user_id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL,
                            state INTEGER NOT NULL,
                            status INTEGER NOT NULL,
                            data TEXT,
                            on_hands TEXT,
                            type_user INTEGER NOT NULL,
                            date TEXT NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS orders (
                            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            message_id_express INTEGER,
                            manager_id INTEGER NOT NULL,
                            status_order INTEGER NOT NULL,
                            type_order INTEGER NOT NULL,
                            data TEXT NOT NULL,
                            time INTEGER,
                            courier_id INTEGER,
                            date_create TEXT NOT NULL,
                            date_close TEXT
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS orders_warehouse (
                            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            message_id_warehouse INTEGER,
                            courier_id INTEGER NOT NULL,
                            status_order INTEGER NOT NULL,
                            data TEXT NOT NULL,
                            storage_id INTEGER,
                            date_create TEXT NOT NULL,
                            date_close TEXT
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS codes (
                            num_code INTEGER PRIMARY KEY AUTOINCREMENT,
                            code TEXT NOT NULL,
                            type_user INTEGER NOT NULL,
                            status INTEGER NOT NULL,
                            user_id INTEGER,
                            date_activate TEXT
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS refill (
                            refill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name_id INTEGER NOT NULL,
                            number_start TEXT NOT NULL,
                            number_now TEXT NOT NULL,
                            on_hands TEXT NOT NULL,
                            price TEXT NOT NULL,
                            added_value TEXT NOT NULL,
                            status INTEGER NOT NULL,
                            date_refill TEXT NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS stock (
                            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            data TEXT NOT NULL,
                            status INTEGER NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS cities (
                            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city_name TEXT NOT NULL,
                            delivery INTEGER NOT NULL,
                            delivery_after_50 INTEGER NOT NULL,
                            status INTEGER NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS dlt_list (
                            number INTEGER PRIMARY KEY AUTOINCREMENT,
                            uid INTEGER NOT NULL,
                            mid INTEGER NOT NULL,
                            time INTEGER NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS price_flex (
                            id_deals INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_product INTEGER NOT NULL,
                            number TEXT NOT NULL,
                            plus_one TEXT NOT NULL,
                            plus_all TEXT NOT NULL,
                            date TEXT NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS financial_operations(
                            id_deals INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_order INTEGER,
                            user_id INTEGER NOT NULL,
                            money TEXT NOT NULL,
                            payer_id INTEGER,
                            date TEXT NOT NULL
                    )""")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    with conn:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS bank(
                            user_id INTEGER PRIMARY KEY,
                            money TEXT NOT NULL
                    )""")


def add_financial_operation(user_id, money, payer_id=-1, id_order=-1):
    db_file = "db.db"
    conn = None
    check = False
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO financial_operations(id_order, user_id, money, payer_id, date) VALUES(?, ?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (id_order, user_id, money, payer_id, now))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {1000}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def update_bank(user_id, money):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""UPDATE bank SET money = "{money}" WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2045}: {e}')
    finally:
        if conn is not None:
            conn.close()


def get_user_bank(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM bank WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {203}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_bank():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM bank;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2045}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def add_flex_price(id_product, number, plus_one):
    db_file = "db.db"
    conn = None
    check = False
    now = datetime.datetime.now()
    unixtime = int(time.mktime(now.timetuple()))
    try:
        sql = """INSERT INTO price_flex(id_product, number, plus_one, plus_all, date) VALUES(?, ?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (id_product, number, str(plus_one), str(plus_one * number), str(now)))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {900}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check

def add_user_bank(uid):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = """INSERT INTO bank(user_id, money) VALUES(?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (uid, "0"))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {9011}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def add_product_new(name):
    db_file = "db.db"
    conn = None
    try:
        sql = """INSERT INTO stock(name, data, status) VALUES(?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (name, "0.0", 0))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {900}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def update_price_stock(num, price):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""UPDATE stock SET data = '{price}' WHERE product_id = {num}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2044}: {e}')
    finally:
        if conn is not None:
            conn.close()


def update_status_stock(num, status):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""UPDATE stock SET status = {status} WHERE product_id = {num}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2044}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_to_dlt_list(uid, mid):
    db_file = "db.db"
    conn = None
    check = False
    now = datetime.datetime.now()
    unixtime = int(time.mktime(now.timetuple()))
    try:
        sql = """INSERT INTO dlt_list(uid, mid, time) VALUES(?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (uid, mid, unixtime))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {700}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def get_product_refill_active(name_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM refill WHERE name_id = {name_id} AND status = 1 AND number_now != '0'"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {801}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_product_refill_active_next(name_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM refill WHERE name_id = {name_id} AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {801}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_products_refill_active():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM refill WHERE status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {801}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_products_refill_all_work():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM refill WHERE status = 1 or status = 0"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {801}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_product_refill_by_id(id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM refill WHERE refill_id = {id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {8011}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data



def get_all_dlt_list(time):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM dlt_list WHERE time < {time}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {701}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def dlt_in_dlt_list(num):
    db_file = "db.db"

    conn = None
    try:
        sql = f"""DELETE FROM dlt_list WHERE number = {num};"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        test = True
    except Exception as e:
        logging.error(f'Error {702}: {e}')
    finally:
        if conn is not None:
            conn.close()


def dlt_deals_by_order_id(order_id):
    db_file = "db.db"

    conn = None
    try:
        sql = f"""DELETE FROM financial_operations WHERE id_order = {order_id};"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {702}: {e}')
    finally:
        if conn is not None:
            conn.close()


def dlt_deals_by_payer_id(pid):
    db_file = "db.db"

    conn = None
    try:
        sql = f"""DELETE FROM financial_operations WHERE payer_id = {pid};"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {702}: {e}')
    finally:
        if conn is not None:
            conn.close()


def delete_order_wh(message_id):
    db_file = "db.db"

    conn = None
    try:
        sql = f"""DELETE FROM orders_warehouse WHERE message_id_warehouse = {message_id};"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        test = True
    except Exception as e:
        logging.error(f'Error {7022}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_code(code, type_user, status):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = """INSERT INTO codes(code, type_user, status) VALUES(?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (code, type_user, status))
        conn.commit()
        cur.close()
        check = True
    except Exception as e:
        logging.error(f'Error {100}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def create_codes():
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT 1 FROM codes;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if not data:
            '''
            Главный админ 1
            Менеджер курьеров 2
            Менеджер самовывоза 3
            Топ Менеджер по продажам 4
            Менеджер склада 5
            Казначей 6
            Менеджер по продажам 7
            Курьер 8
            Мастер самовывоза 9
            Работник склада 10
            Админ второго сорта 11
            Менеджер курьеров и Менеджер самовывоза 12
            Рядовой 13
            '''
            type = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0,
                    "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0}
            for code in range(168):
                while True:
                    pin = ''.join(random.sample("0123456789", 4))
                    if type["1"] < 1:
                        check = add_code(pin, 1, 1)
                        if check:
                            type["1"] += 1
                            break
                    elif type["2"] < 1:
                        check = add_code(pin, 2, 0)
                        if check:
                            type["2"] += 1
                            break
                    elif type["3"] < 1:
                        check = add_code(pin, 3, 0)
                        if check:
                            type["3"] += 1
                            break
                    elif type["4"] < 1:
                        check = add_code(pin, 4, 0)
                        if check:
                            type["4"] += 1
                            break
                    elif type["5"] < 1:
                        check = add_code(pin, 5, 0)
                        if check:
                            type["5"] += 1
                            break
                    elif type["6"] < 1:
                        check = add_code(pin, 6, 0)
                        if check:
                            type["6"] += 1
                            break
                    elif type["7"] < 40:
                        check = add_code(pin, 7, 0)
                        if check:
                            type["7"] += 1
                            break
                    elif type["8"] < 40:
                        check = add_code(pin, 8, 0)
                        if check:
                            type["8"] += 1
                            break
                    elif type["9"] < 40:
                        check = add_code(pin, 9, 0)
                        if check:
                            type["9"] += 1
                            break
                    elif type["10"] < 40:
                        check = add_code(pin, 10, 0)
                        if check:
                            type["10"] += 1
                            break
                    elif type["11"] < 1:
                        check = add_code(pin, 11, 0)
                        if check:
                            type["11"] += 1
                            break
                    elif type["12"] < 1:
                        check = add_code(pin, 12, 0)
                        if check:
                            type["12"] += 1
                            break
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {101}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def check_user_id(user_id, username):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT * FROM users WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if not data:
            cur.close()
            add_user(user_id, username)
            check = True
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {201}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def add_user(user_id, username):
    db_file = "db.db"
    conn = None
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO users(user_id, username, state, status, type_user, date) VALUES(?, ?, ?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (user_id, username, 0, 0, 13, now))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {200}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_type_user(user_id, type_user):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""UPDATE users SET type_user = {type_user}, status = 1 WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {202}: {e}')
    finally:
        if conn is not None:
            conn.close()


def order_time_null(order_id):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""UPDATE orders SET date_close = NULL WHERE order_id = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {202}: {e}')
    finally:
        if conn is not None:
            conn.close()


def update_user(user_id, name, data):
    db_file = "db.db"
    conn = None
    sql_string = ''
    if name == 'status':
        sql_string = f"status = {data}"
    elif name == 'state':
        sql_string = f"state = {data}"
    elif name == 'data':
        sql_string = f'data = "{data}"'
    elif name == 'on_hands':
        sql_string = f'on_hands = "{data}"'
    elif name == 'type_user':
        sql_string = f'type_user = {data}'
    try:
        sql = f"""UPDATE users SET {sql_string} WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {204}: {e}')
    finally:
        if conn is not None:
            conn.close()


def update_refill(refill_id, name, data):
    db_file = "db.db"
    conn = None
    sql_string = ''
    if name == 'number_now':
        sql_string = f"number_now = '{data}'"
    elif name == 'number_start':
        sql_string = f"number_start = '{data}'"
    elif name == 'on_hands':
        sql_string = f"on_hands = '{data}'"
    elif name == 'status':
        sql_string = f"status = {data}"
    elif name == 'price':
        sql_string = f"price = '{data}'"
    elif name == 'added_value':
        sql_string = f"added_value = '{data}'"
    try:
        sql = f"""UPDATE refill SET {sql_string} WHERE refill_id = {refill_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {800}: {e}')
    finally:
        if conn is not None:
            conn.close()


def get_user_data(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM users WHERE user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {203}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_user_data_by_role(role):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM users WHERE type_user = {role} and status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {206}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data

def get_user_data_by_role_all(role):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM users WHERE type_user = {role}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2061}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data

def get_finance_deals_by_id(order_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE id_order = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2067}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_finance_deals_by_id_and_user(order_id, user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE id_order = {order_id} AND user_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2067}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_finance_deals_by_payer(pid):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE payer_id = {pid}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2067}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data

def get_finance_deals_by_orderid(oid):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE id_order = {oid}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2067}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def check_activate_code(user_id, code):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT * FROM codes WHERE user_id = {user_id} AND status = 2 AND code = '{code}'"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            cur.close()
            check = True
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {102}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def check_noactivate_code(user_id, code):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT * FROM codes WHERE code = '{code}' AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            cur.close()
            check = True
            add_code_from_user(user_id, code, data[2])
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {103}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def add_code_from_user(user_id, code, type_user):
    db_file = "db.db"
    conn = None
    now = str(datetime.datetime.now())
    try:
        sql = f"""UPDATE codes SET user_id = {user_id}, status = 2, date_activate = '{now}' WHERE code = '{code}'"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        add_type_user(user_id, type_user)
    except Exception as e:
        logging.error(f'Error {104}: {e}')
    finally:
        if conn is not None:
            conn.close()


def check_product(prodcut):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT * FROM stock WHERE name = '{prodcut[1]}' AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            cur.close()
            check = True
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {300}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def add_city(city, price, price2):
    db_file = "db.db"
    conn = None
    try:
        sql = """INSERT INTO cities(city_name, delivery, delivery_after_50, status) VALUES(?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (city, price, price2, 1))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2003}: {e}')
    finally:
        if conn is not None:
            conn.close()


def check_city(city):
    db_file = "db.db"
    conn = None
    check = False
    try:
        sql = f"""SELECT * FROM cities WHERE city_name = "{city}" AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        if data:
            cur.close()
            check = True
        else:
            cur.close()
    except Exception as e:
        logging.error(f'Error {400}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return check


def get_products():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM stock;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {301}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_product_by_name(name):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM stock WHERE name = '{name}'"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {302}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_product_by_num(num):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM stock WHERE product_id = {num}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {302}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_product_all():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM stock;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {302}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_price_product(product):
    db_file = "db.db"
    conn = None
    price = None
    try:
        sql = f"""SELECT * FROM stock WHERE name = '{product[1]}' AND status = 1;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        price = product[0] * data[2]
        cur.close()
    except Exception as e:
        logging.error(f'Error {302}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return price


def get_data_city(city):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM cities WHERE city_name = "{city}" AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {401}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def add_order(user_id, data, type):
    db_file = "db.db"
    conn = None
    data_order = ast.literal_eval(data)
    datax = data_order["new_order"]["data"]
    datax["photo"] = data_order["new_order"]["photo"]
    try:
        datax["order_id"] = data_order["order_id"]
    except:
        pass
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO orders(manager_id, status_order, type_order, data, date_create) VALUES(?, ?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (user_id, 0, type, str(datax), now))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {500}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_order_warehouse(courier_id, product):
    db_file = "db.db"
    conn = None
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO orders_warehouse(courier_id, status_order, data, date_create) VALUES(?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (courier_id, 0, product, now))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {600}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_order_warehouse2(courier_id, product):
    db_file = "db.db"
    conn = None
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO orders_warehouse(courier_id, status_order, data, date_create) VALUES(?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (courier_id, 4, product, now))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {610}: {e}')
    finally:
        if conn is not None:
            conn.close()


def add_refill(name_id, num_start, price, added_value):
    db_file = "db.db"
    conn = None
    now = str(datetime.datetime.now())
    try:
        sql = """INSERT INTO refill(name_id, number_start, number_now, on_hands, price, added_value, status, date_refill) VALUES(?, ?, ?, ?, ?, ?, ?, ?);"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql, (name_id, num_start, num_start, 0, price, added_value, 0, now))
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {6130}: {e}')
    finally:
        if conn is not None:
            conn.close()


def get_last_order_warehouse(courier_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE courier_id = {courier_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()[-1]
        cur.close()
    except Exception as e:
        logging.error(f'Error {601}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_stock():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = """SELECT * FROM stock WHERE status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {6012}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_last10_order_warehouse(courier_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE courier_id = {courier_id} ORDER BY order_id DESC LIMIT 10"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {601}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_confirm_order_no_check():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = """SELECT * FROM orders WHERE time != 1 AND status_order >= 3"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {601}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_confirm_order_no_check2():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = """SELECT * FROM orders WHERE (time IS NULL OR time != 1) AND status_order >= 3;"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {601}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_confirm_no_start_order():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = """SELECT * FROM orders WHERE status_order = 0"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {6011}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_financial_operation_by_user_last(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE user_id = {user_id} ORDER BY id_order DESC LIMIT 1000"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {9907}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_financial_operation_by_user_and_id_order(user_id, id_order):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE user_id = {user_id} AND id_order = {id_order}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {9907}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_orders_for_report():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders ORDER BY order_id DESC LIMIT 2000"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {991199}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_orders_for_report_by_user_id(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE manager_id = {user_id} ORDER BY order_id DESC LIMIT 1000"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {991199}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_financial_operation_by_user_last_week(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE user_id = {user_id} ORDER BY id_order DESC LIMIT 10000"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {990722}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_financial_operation_by_user_and_order(user_id, order_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM financial_operations WHERE user_id = {user_id} AND id_order = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {990722}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_wh_by_yestrd():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse ORDER BY order_id DESC LIMIT 2000"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {99075}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_all_confirm_no_confirm_order():
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = """SELECT * FROM orders WHERE status_order = 2"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {6011}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_complite_order_warehouse(courier_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE courier_id = {courier_id} AND status_order = 2"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {601}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_warehouse_by_mid(mid):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE message_id_warehouse = {mid}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {603}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_warehouse_by_id(order_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE order_id = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {605}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_warehouse_by_cur(courier_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE courier_id = {courier_id} ORDER BY order_id DESC LIMIT 12"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {607}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_by_cur2(courier_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {courier_id} ORDER BY order_id DESC LIMIT 12"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {607}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def check_new_order_sw(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders_warehouse WHERE storage_id = {user_id} AND (status_order = 1 OR status_order = 5)"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {604}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def update_order_w(order_id, type, data):
    db_file = "db.db"
    conn = None
    sql_string = ''
    if type == 'message_id_warehouse':
        sql_string = f"message_id_warehouse = {data}"
    elif type == 'status_order':
        sql_string = f"status_order = {data}"
    elif type == 'storage_id':
        sql_string = f"storage_id = {data}"
    elif type == 'data':
        sql_string = f'data = "{data}"'
    elif type == 'date_close':
        sql_string = f'date_close = "{data}"'
    try:
        sql = f"""UPDATE orders_warehouse SET {sql_string} WHERE order_id = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {602}: {e}')
    finally:
        if conn is not None:
            conn.close()


def check_new_order_courier(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {user_id} AND status_order = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {501}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def check_active_order_courier(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {user_id} AND status_order = 2"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {507}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def check_cloesd_return_order_courier(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {user_id} AND status_order = 3 AND type_order = 33 ORDER BY order_id DESC LIMIT 5"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {507}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_last200_order_cur(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {user_id} AND status_order > 2 ORDER BY order_id DESC LIMIT 500"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2077}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_last200_order_curx(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE courier_id = {user_id} AND status_order > 2 ORDER BY order_id DESC LIMIT 200"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {2077}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_active_order_sm(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE manager_id = {user_id} AND status_order < 3"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {507}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_cloesed_order_sm(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE manager_id = {user_id} AND (status_order = 3 OR status_order = 5)"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {508}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_last_order(user_id):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM orders WHERE manager_id = {user_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()[-1]
        cur.close()
    except Exception as e:
        logging.error(f'Error {502}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def update_order(order_id, type, data):
    db_file = "db.db"
    conn = None
    sql_string = ''
    if type == 'message_id_express':
        sql_string = f"message_id_express = {data}"
    elif type == 'status_order':
        sql_string = f"status_order = {data}"
    elif type == 'time':
        sql_string = f"time = {data}"
    elif type == 'data':
        sql_string = f'data = "{data}"'
    elif type == 'date_close':
        sql_string = f'date_close = "{data}"'
    try:
        sql = f'''UPDATE orders SET {sql_string} WHERE order_id = {order_id}'''
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {503}: {e}')
    finally:
        if conn is not None:
            conn.close()


def get_users_for_delivery(type):
    db_file = "db.db"
    conn = None
    data = None
    try:
        sql = f"""SELECT * FROM users WHERE type_user = {type} AND status = 1"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
    except Exception as e:
        logging.error(f'Error {205}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def set_courier_or_pickup_order(message_id, courier_id, type_courier):
    db_file = "db.db"
    conn = None
    if type_courier == 8:
        type = 12
        type2 = 33
    elif type_courier == 9:
        type = 22
        type2 = 38
    try:
        sql = f"""UPDATE orders SET courier_id = {courier_id} WHERE message_id_express = {message_id} AND (type_order = {type} OR type_order = {type2})"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {505}: {e}')
    finally:
        if conn is not None:
            conn.close()
    conn = None
    try:
        sql = f"""UPDATE orders SET status_order = 1 WHERE message_id_express = {message_id} AND type_order = {type}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        logging.error(f'Error {505}: {e}')
    finally:
        if conn is not None:
            conn.close()


def get_order_by_message_id(message_id, type_courier):
    db_file = "db.db"
    conn = None
    if type_courier == 8:
        type = 12
        type2 = 33
    elif type_courier == 9:
        type = 22
        type2 = 38
    try:
        sql = f"""SELECT * FROM orders WHERE message_id_express = {message_id} AND (type_order = {type} OR type_order = {type2})"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {504}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


def get_order_by_order_id(order_id):
    db_file = "db.db"
    conn = None
    try:
        sql = f"""SELECT * FROM orders WHERE order_id = {order_id}"""
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        cur.close()
    except Exception as e:
        logging.error(f'Error {506}: {e}')
    finally:
        if conn is not None:
            conn.close()
        return data


create_tables()
create_codes()
