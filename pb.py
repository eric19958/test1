import db_cmd

cur = db_cmd.get_user_data_by_role(8)
pickup = db_cmd.get_user_data_by_role(9)
for i in cur:
	print(i[0], i[1], db_cmd.get_user_bank(i[0])[1])
for i in pickup:
	print(i[0], i[1], db_cmd.get_user_bank(i[0])[1])