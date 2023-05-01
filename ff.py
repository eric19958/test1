import db_cmd
import ast

data = db_cmd.get_user_data_by_role(8)

for el in data:
	datax = ast.literal_eval(el[5])["product"]
	for i in datax:
		if i[0] > 0 and i[1] != "שקל":
			print(i, el[1])

data = db_cmd.get_user_data_by_role(9)

for el in data:
	datax = ast.literal_eval(el[5])["product"]
	for i in datax:
		if i[0] > 0 and i[1] != "שקל":
			print(i, el[1])