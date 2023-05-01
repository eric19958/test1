import db_cmd

bank = db_cmd.get_all_bank()
cur = []
pickup = []
storage = []
tops = []
for el in bank:
    f = 0
    data_user = db_cmd.get_user_data(el[0])
    if data_user:
        if data_user[6] in [8]:
            cur.append(el)
            f = 1
        elif data_user[6] in [9]:
            pickup.append(el)
            f = 1
        elif data_user[6] in [10]:
            storage.append(el)
            f = 1
        elif data_user[6] in [12, 5]:
            tops.append(el)
            f = 1
        if (float(el[1]) > 0 or float(el[1]) < 0) and f == 0:
            print(f"@{data_user[1]}: {round(float(el[1]), 2)}")

    elif (float(el[1]) > 0 or float(el[1]) < 0):
        print(f"uid:{el[0]}: {round(float(el[1]), 2)}")

print("\n\n\nהרווחים של כל אחד מהבלדרים בשבוע (Заработок каждого из курьеров за неделю):\n")
for el in cur:
    data_user = db_cmd.get_user_data(el[0])
    print(f"@{data_user[1]}: {round(float(el[1]), 2)}")

print("\n\n\nרווחי איסוף לשבוע (Заработок самовывоза за неделю):\n")
for el in pickup:
    data_user = db_cmd.get_user_data(el[0])
    print(f"@{data_user[1]}: {round(float(el[1]), 2)}")

print("\n\n\nרווחי עובדי מחסנים (Заработок работников склада):\n")
for el in storage:
    data_user = db_cmd.get_user_data(el[0])
    print(f"@{data_user[1]}: {round(float(el[1]), 2)}")

print("\n\n\nרווחי המנהלים המובילים (Заработок топ менеджеров):\n")
for el in tops:
    data_user = db_cmd.get_user_data(el[0])
    print(f"@{data_user[1]}: {round(float(el[1]), 2)}")
