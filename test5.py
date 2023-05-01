import json
import ast
import time
import db_cmd
import datetime
from datetime import timedelta
import dopf

now = datetime.datetime.combine(
    datetime.date.today(), datetime.datetime.min.time())
textxx = ""
UIDXX = [902167185]

for uid in UIDXX:
    datax = db_cmd.get_financial_operation_by_user_last_week(uid)
   #username = db_cmd.get_user_data(uid)[1]
   # print(f'@{username}')
    for i in range(7):
        summ = 0
        nowf = now - timedelta(days=i)
        for operation in datax:
            orderx = db_cmd.get_order_by_order_id(operation[1])
            date_operation = datetime.datetime.strptime(
                orderx[8], '%Y-%m-%d %H:%M:%S.%f')
            if date_operation < nowf + timedelta(hours=9) and date_operation > nowf - timedelta(hours=15):
                summ += float(operation[3])
        print((nowf - timedelta(days=1)).date(), round(summ - 3520, 2))
    print()
