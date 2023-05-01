import dopf
import db_cmd

data_order = db_cmd.get_order_by_order_id(2463)
print(dopf.checkxcur(data_order))