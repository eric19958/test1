import dopf
import db_cmd
import ast


def plus(data, all_data):
  for el in data:
    check = True
    for el2 in all_data:
      if el[1] == el2[1] and float(el[2]) == el2[2]:
        el2[0] += el[0]
        check = False
    if check:
      all_data.append([el[0], el[1], float(el[2])])
  return all_data


def minus(data, all_data):
  for el in data:
    check = True
    for el2 in all_data:
      if el[1] == el2[1] and float(el[2]) == el2[2]:
        el2[0] -= el[0]
        check = False
    if check:
      all_data.append([- el[0], el[1], float(el[2])])
  return all_data

nowx = [18527,
18518,
18517,
18495,
18489,
18488,
18486,
18483,
18479]
now = []

for i in nowx:
  try:
    data = db_cmd.get_order_warehouse_by_id(i)
    if data[3] == 3 or data[3] == 2:
      datax = ast.literal_eval(data[4])["correct_product"]
      now = plus(datax, now)
    elif data[3] == 6:
      datax = ast.literal_eval(data[4])["true_product"]
      now = minus(datax, now)
  except:
    pass

for el in now:
  print(el[1], "(", el[2], ")", el[0])
