import db_cmd
import dopf 

text = """1 מזרק (150)
1 שמן נמוך (150)
1 שמן גבוה (300)
1 באדר (180)
1 BHO (150)
10 זול מיאמי (20)
9.9 יקר גדול (43)
10 קאלי (53.5)
10 בררה (15.5)
10 יקר בוטיק (48.5)
9.8 זול (15.5)
10 יקר (40)
10 מונרוק (80)
10 אייס (45)
10 בלונדי (50)
10 חום גדול (20)
10 יקר מיאמי (52)"""
order_id_w = 3028

data_order_w = db_cmd.get_order_warehouse_by_id(order_id_w)
datax, text_next, check = dopf.check_order_for_sw2(data_order_w, text)
print(check)