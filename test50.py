import db_cmd
import ast


banks = db_cmd.get_all_bank()

for bank in banks:
    data = db_cmd.get_user_data(bank[0])
    if data and (not data[6] in [8,9]):
        db_cmd.update_bank(bank[0], 0)
    elif not data:
        db_cmd.update_bank(bank[0], 0)
