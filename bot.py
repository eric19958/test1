#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json
import ast
import time
import db_cmd
import markup
import datetime
from datetime import timedelta
import logging
import dopf
import threading

config = dopf.readJs()
bot = telebot.TeleBot(config['telegram']['token'])
mod = config['telegram']['mod']
logging.basicConfig(format='%(asctime)s | %(process)d-%(levelname)s-%(message)s',
					level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')

'''
Состояния менеджер: 0 - база, 1 - новый заказа, курьер
'''

def close(xxx, ooii, mng_id):
	cid = xxx
	uid = xxx
	text_cnf = dopf.readJs("text.json")
	data = db_cmd.get_user_data(uid)
	if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
		order_id = ooii
		config = dopf.readJs()
		data_order = db_cmd.get_order_by_order_id(order_id)
		if uid == data_order[7]:
			if data[6] == 8:
				cidx = config["telegram"]["сourier_channel"]
				type = 12
			else:
				cidx = config["telegram"]["pickup_channel"]
				type = 22
			data_orderx = ast.literal_eval(data_order[5])
			grm = 0
			for product in data_orderx["product"]:
				if product[1] != "שקל":
					grm += product[0]
			try:
				if grm <= 60:
					data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[2]
				else:
					data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[3]
			except:
				data_orderx["courier"] = 0
			chx = True
			try:
				if "correct_product" in data_orderx:
					if not dopf.conformity(data_orderx["product"], data_orderx["correct_product"]):
						data_orderx["correct_product"], chx = dopf.calibration(
							data_orderx["product"], data_order[7])
				else:
					data_orderx["correct_product"], chx = dopf.calibration(
						data_orderx["product"], data_order[7])
			except Exception as e:
				print(e)
				data_orderx["correct_product"], chx = dopf.calibration(
					data_orderx["product"], data_order[7])
			if dopf.check_cur_and_order(data_orderx["correct_product"], ast.literal_eval(db_cmd.get_user_data(uid)[5])["product"]) and chx:
				if type == 12:
					print(text_cnf["order_confirm_all2"].format(
												 data_orderx["courier"]))
				else:
					print(text_cnf["order_confirm_all"].format(
												 data_orderx["courier"]))
				db_cmd.update_order(order_id, 'status_order', 3)
				db_cmd.update_order(order_id, 'data', str(data_orderx))
				db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
				dopf.take_courier_and_storage(db_cmd.get_order_by_order_id(order_id))
				dopf.update_price()
				if data_order[4] in [33, 38]:
					dopf.take_courier_and_storage2(db_cmd.get_order_by_order_id(order_id))
					dopf.update_price()
				text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
				bot.edit_message_caption(chat_id=cidx,
										 message_id=data_order[1],
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))
				bot.send_message(chat_id=mng_id, text=text_cnf["complete_order_confirm"], reply_markup=markup.main_sm())
			else:
				bot.send_message(mng_id, text=text_cnf["no_products_curier"], reply_markup=markup.main_sm())
				

@bot.message_handler(commands=['start'])
def handler_start_new(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		text = message.text
		username = message.from_user.username
		text_cnf = dopf.readJs("text.json")
		if cid == uid:
			db_cmd.check_user_id(uid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [1, 2, 3, 5, 6, 7, 11, 12, 14, 17] and data[3] == 1:
				db_cmd.update_user(uid, 'state', 0)
				if data[6] == 1:
					pass
				elif data[6] == 2:
					pass
				elif data[6] == 3:
					pass
				elif data[6] == 5:
					bot.send_message(cid,
									 text=text_cnf["menu_sales_manager"],
									 parse_mode=None,
									 reply_markup=markup.menu_storage_manager())
				elif data[6] == 6:
					pass
				elif data[6] == 7:
					bot.send_message(cid,
									 text=text_cnf["menu_sales_manager"],
									 parse_mode=None,
									 reply_markup=markup.menu_sales_manager(uid))
				elif data[6] == 17:
					if len(text) == 6:
						bot.send_message(cid,
									 text=text_cnf["menu_sales_manager"],
									 parse_mode=None,
									 reply_markup=markup.menu_top_mng())
					else:
						command = text[7:]
						if command.startswith('cnlorder'):
							order_id = command[8:]
							db_cmd.update_user(uid, 'state', 5)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["cnlorder"] = int(order_id)
							else:
								datax = {"cnlorder": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["reason_for_cancellation"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())
						elif command.startswith('ccnlorder'):
							order_id = command[9:]
							db_cmd.update_user(uid, 'state', 5)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["cnlorder"] = int(order_id)
							else:
								datax = {"cnlorder": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["reason_for_cancellation"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())
						elif command.startswith('chngpr'):
							order_id = command[6:]
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["chngpr"] = int(order_id)
							else:
								datax = {"chngpr": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							dataxx = db_cmd.get_order_by_order_id(int(order_id))
							if dataxx[4] in [12, 33]:
								cidx = config["telegram"]["сourier_channel"]
							else:
								cidx = config["telegram"]["pickup_channel"]
							url_order = f'https://t.me/c/{str(cidx)[4:]}/{str(dataxx[1])}'
							bot.send_message(chat_id=uid,
											 text=text_cnf["price_for_order"].format(
												 url_order),
											 parse_mode=None,
											 reply_markup=markup.set_price_cur(order_id))
						elif command.startswith('sndmsg'):
							order_id = command[6:]
							db_cmd.update_user(uid, 'state', 6)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["sndmsg"] = int(order_id)
							else:
								datax = {"sndmsg": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["sndmsg_for_order_sm"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())
				elif data[6] == 11:
					pass
				elif data[6] == 14:
					bank = db_cmd.get_user_bank(uid)[1]
					bank_storage = db_cmd.get_user_bank(0)[1]
					bot.send_message(cid,
									 text=text_cnf["boss_text"].format(bank, bank_storage),
									 parse_mode=None,
									 reply_markup=None)
				elif data[6] == 12:
					if len(text) == 6:
						bot.send_message(cid,
										 text=text_cnf["menu_manager_courier_and_pickup"],
										 parse_mode=None,
										 reply_markup=markup.menu_manager_courier_and_pickup())
					else:
						command = text[7:]
						if command.startswith('cnlorder'):
							order_id = command[8:]
							db_cmd.update_user(uid, 'state', 5)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["cnlorder"] = int(order_id)
							else:
								datax = {"cnlorder": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["reason_for_cancellation"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())
						elif command.startswith('ccnlorder'):
							order_id = command[9:]
							db_cmd.update_user(uid, 'state', 5)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["cnlorder"] = int(order_id)
							else:
								datax = {"cnlorder": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["reason_for_cancellation"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())
						elif command.startswith('chngpr'):
							order_id = command[6:]
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["chngpr"] = int(order_id)
							else:
								datax = {"chngpr": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							dataxx = db_cmd.get_order_by_order_id(int(order_id))
							if dataxx[4] in [12, 33]:
								cidx = config["telegram"]["сourier_channel"]
							else:
								cidx = config["telegram"]["pickup_channel"]
							url_order = f'https://t.me/c/{str(cidx)[4:]}/{str(dataxx[1])}'
							bot.send_message(chat_id=uid,
											 text=text_cnf["price_for_order"].format(
												 url_order),
											 parse_mode=None,
											 reply_markup=markup.set_price_cur(order_id))
						elif command.startswith('sndmsg'):
							order_id = command[6:]
							db_cmd.update_user(uid, 'state', 6)
							if data[4]:
								datax = ast.literal_eval(data[4])
								datax["sndmsg"] = int(order_id)
							else:
								datax = {"sndmsg": int(order_id)}
							db_cmd.update_user(uid, 'data', str(datax))
							bot.send_message(chat_id=uid,
											 text=text_cnf["sndmsg_for_order_sm"].format(
												 order_id),
											 parse_mode=None,
											 reply_markup=markup.main_menu())

			else:
				bot.send_message(cid,
								 text=text_cnf["start"],
								 parse_mode=None,
								 reply_markup=None)
	except Exception as e:
		logging.error(f'Error in /start: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("get_product"))
def callback_get_product(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[11:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if uid == data_order[7] and data_order[6] != 2:
				db_cmd.update_order(order_id, 'time', 2)
				chat_warehouse = config["telegram"]["warehouse_channel"]
				text = dopf.get_text_by_warehouse_order(data_order)
				pr = ast.literal_eval(data_order[5])["product"]
				pr2 = []
				for px in pr:
					if px[1] != "שקל":
						pr2.append(px)
				checkx = True
				for prx in pr2:
					product_name = prx[1]
					product_num_now = prx[0]
					product_data = db_cmd.get_product_by_name(product_name)
					product_id = product_data[0]
					product_data_refill = db_cmd.get_product_refill_active(product_id)
					k = 0
					for product_data_re in product_data_refill:
						k += float(product_data_re[3])
					if k < product_num_now:
						checkx = False
						break
				if not checkx:
					db_cmd.update_order(order_id, 'time', 0)
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["text_alert_ff"])
				else:
					product = str({"product": pr2, "order_id": order_id})
					courier_id = data_order[7]
					db_cmd.add_order_warehouse(courier_id, product)
					order_w = db_cmd.get_last_order_warehouse(courier_id)
					msgx = bot.send_message(chat_warehouse,
											text=text,
											parse_mode=None,
											reply_markup=markup.select_storage_worker(order_w[0]))
					db_cmd.update_order_w(order_w[0], 'message_id_warehouse', msgx.message_id)
					bot.edit_message_reply_markup(
						chat_id=cid, message_id=mid, reply_markup=markup.active_order_cr_kb(order_id))
					msg = bot.send_message(chat_id=cid,
										   text=text_cnf["request_sent_warehouse"],
										   parse_mode=None,
										   reply_markup=None)
					db_cmd.add_to_dlt_list(uid, msg.message_id)
					storage_worker_id = dopf.readJs("worker.json")["worker"]
					if storage_worker_id != 0:
						config = dopf.readJs()
						mid = msgx.message_id
						order_w = db_cmd.get_order_warehouse_by_mid(mid)
						db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
						db_cmd.update_order_w(order_w[0], 'status_order', 1)
						dataxx = ast.literal_eval(order_w[4])
						correct_product = []
						check_k = 0
						for el in dataxx["product"]:
							if el[1] != "שקל":
								name_id = db_cmd.get_product_by_name(el[1])[0]
								list_ref = db_cmd.get_product_refill_active(name_id)
								ffx = 0
								for ref in list_ref:
									if float(ref[3]) >= float(el[0]) and float(ref[5]) + float(ref[6]) == float(db_cmd.get_product_by_name(el[1])[2]):
										price = str(float(ref[5]) + float(ref[6]))
										correct_product.append([el[0], el[1], price])
										ffx = 1
										break
								if ffx == 0:
									check_k += 1
						if check_k > 0:
							db_cmd.update_order_w(order_w[0], 'status_order', 0)
							tops = db_cmd.get_user_data_by_role(5)
							for top in tops:
								bot.send_message(
									top[0], text=text_cnf["no_auto_worker_no_products"].format(chat_warehouse, mid), parse_mode=None)
						else:
							dataxx["correct_product"] = correct_product
							db_cmd.update_order_w(order_w[0], 'data', str(dataxx))
							order_w = db_cmd.get_order_warehouse_by_mid(mid)
							text = dopf.get_text_by_warehouse_order_next(order_w)
							msg = bot.send_message(
								storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
							bot.edit_message_text(chat_id=chat_warehouse,
												  message_id=mid,
												  text=text,
												  parse_mode=None,
												  reply_markup=markup.menu_cnlwhx())
							db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in get_product: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "takeprconf")
def callback_takeprconf(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1 and data[2] == 41:
			config = dopf.readJs()
			chat_warehouse = config["telegram"]["warehouse_channel"]
			text = dopf.get_text_by_warehouse_order_x2(ast.literal_eval(data[4])["productx"], uid)
			productf = ast.literal_eval(data[4])["productx"]
			prxx, checkxx = dopf.check_type_order(productf)
			if checkxx:
				product = {"product": prxx}
				db_cmd.add_order_warehouse(uid, str(product))
				order_w = db_cmd.get_last_order_warehouse(uid)
				db_cmd.update_user(uid, 'state', 0)
				msgx = bot.send_message(chat_warehouse,
										text=text,
										parse_mode=None,
										reply_markup=markup.select_storage_worker(order_w[0]))
				db_cmd.update_order_w(order_w[0], 'message_id_warehouse', msgx.message_id)
				msg = bot.send_message(chat_id=cid,
									   text=text_cnf["request_sent_warehouse"],
									   parse_mode=None,
									   reply_markup=None)
				if data[6] == 8:
					cur_mng_list = db_cmd.get_user_data_by_role(12)
					for i in cur_mng_list:
						try:
							bot.send_message(i, text_cnf["return_cur_request"].format(data[1], order_w[0]), parse_mode=None)
						except:
							print(i, "BLOCK")
				else:
					cur_mng_list = db_cmd.get_user_data_by_role(17)
					for i in cur_mng_list:
						try:
							bot.send_message(i, text_cnf["return_cur_request"].format(data[1], order_w[0]), parse_mode=None)
						except:
							print(i, "BLOCK")
				db_cmd.add_to_dlt_list(uid, msg.message_id)
				storage_worker_id = dopf.readJs("worker.json")["worker"]
				if storage_worker_id != 0:
					config = dopf.readJs()
					mid = msgx.message_id
					order_w = db_cmd.get_order_warehouse_by_mid(mid)
					db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
					db_cmd.update_order_w(order_w[0], 'status_order', 1)
					try:
						dataxx = ast.literal_eval(order_w[4])
						correct_product = []
						for el in dataxx["product"]:
							if el[1] != "שקל":
								name_id = db_cmd.get_product_by_name(el[1])[0]
								list_ref = db_cmd.get_product_refill_active(name_id)
								ffx = 0
								for ref in list_ref:
									if float(ref[3]) > float(el[0]) and float(ref[5]) + float(ref[6]) == float(db_cmd.get_product_by_name(el[1])[2]):
										price = str(float(ref[5]) + float(ref[6]))
										correct_product.append([el[0], el[1], price])
										ffx = 1
										break
								if ffx == 0:
									for ref in list_ref:
										if float(ref[3]) > float(el[0]):
											price = str(float(ref[5]) + float(ref[6]))
											correct_product.append([el[0], el[1], price])
											break
						dataxx["correct_product"] = correct_product
						db_cmd.update_order_w(order_w[0], 'data', str(dataxx))
					except:
						pass
					order_w = db_cmd.get_order_warehouse_by_mid(mid)
					text = dopf.get_text_by_warehouse_order_next(order_w)
					msg = bot.send_message(
						storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
					bot.edit_message_text(chat_id=chat_warehouse,
										  message_id=mid,
										  text=text,
										  parse_mode=None,
										  reply_markup=markup.menu_cnlwhx())
					db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
			else:
				product = str({"product": prxx})
				courier_id = uid
				if dopf.chek_plus_product(prxx, courier_id):
					list_xxx = db_cmd.check_cloesd_return_order_courier(courier_id)
					for elxx in list_xxx:
						tft = ast.literal_eval(elxx[5])
						if "stk" in tft:
							if tft["stk"] == 0:
								bot.answer_callback_query(
									callback_query_id=call.id, text=text_cnf["not_finance_order"])
								return 0
					db_cmd.add_order_warehouse2(courier_id, product)
					order_w = db_cmd.get_last_order_warehouse(courier_id)
					text = dopf.get_text_by_warehouse_order3(order_w)
					msgx = bot.send_message(chat_warehouse,
											text=text,
											parse_mode=None,
											reply_markup=markup.select_storage_worker2(order_w[0]))
					db_cmd.update_order_w(order_w[0], 'message_id_warehouse', msgx.message_id)
					bot.edit_message_reply_markup(chat_id=cid,
												  message_id=mid,
												  reply_markup=markup.backpuck_cr_kb2(uid))
					storage_worker_id = dopf.readJs("worker.json")["worker"]
					if storage_worker_id != 0:
						mid = msgx.message_id
						config = dopf.readJs()
						chat_warehouse = config["telegram"]["warehouse_channel"]
						order_w = db_cmd.get_order_warehouse_by_mid(mid)
						db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
						db_cmd.update_order_w(order_w[0], 'status_order', 5)
						order_w = db_cmd.get_order_warehouse_by_mid(mid)
						text = dopf.get_text_by_warehouse_order2(order_w)
						msg = bot.send_message(
							storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
						bot.edit_message_text(chat_id=chat_warehouse,
											  message_id=mid,
											  text=text,
											  parse_mode=None,
											  reply_markup=markup.menu_cnlwhx())
						db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
				else:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["not_product_in_back"])
	except Exception as e:
		logging.error(f'Error in takeprconf: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("right"))
def callback_right(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data.split('#')[1])
			order_data = db_cmd.get_order_by_order_id(order_id)
			config = dopf.readJs()
			chat_warehouse = config["telegram"]["warehouse_channel"]
			text = dopf.get_text_by_warehouse_order_x2(
				ast.literal_eval(order_data[5])["true_product"], uid)
			productf = ast.literal_eval(order_data[5])["true_product"]
			tr = []
			for i in productf:
				if i[1] != "שקל":
					tr.append(i)
			product = str({"product": tr, "order_id": order_id})
			courier_id = uid
			db_cmd.add_order_warehouse2(courier_id, product)
			order_w = db_cmd.get_last_order_warehouse(courier_id)
			text = dopf.get_text_by_warehouse_order2(order_w)
			msgx = bot.send_message(chat_warehouse,
									text=text,
									parse_mode=None,
									reply_markup=markup.select_storage_worker2(order_w[0]))
			db_cmd.update_order_w(order_w[0], 'message_id_warehouse', msgx.message_id)
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=None)
			storage_worker_id = dopf.readJs("worker.json")["worker"]
			if storage_worker_id != 0:
				mid = msgx.message_id
				config = dopf.readJs()
				chat_warehouse = config["telegram"]["warehouse_channel"]
				order_w = db_cmd.get_order_warehouse_by_mid(mid)
				db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
				db_cmd.update_order_w(order_w[0], 'status_order', 5)
				order_w = db_cmd.get_order_warehouse_by_mid(mid)
				text = dopf.get_text_by_warehouse_order2(order_w)
				msg = bot.send_message(
					storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
				bot.edit_message_text(chat_id=chat_warehouse,
									  message_id=mid,
									  text=text,
									  parse_mode=None,
									  reply_markup=markup.menu_cnlwhx())
				db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in right: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("car_crash"))
def callback_car_crash(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[9:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if uid == data_order[7]:
				db_cmd.update_order(order_id, 'status_order', 0)
				bot.edit_message_caption(chat_id=cid,
										 message_id=mid,
										 caption=text_cnf["delivery_cancel_car_crash"],
										 parse_mode=None,
										 reply_markup=None)
				if data[6] == 8:
					cidx = config["telegram"]["сourier_channel"]
					type = 12
				else:
					cidx = config["telegram"]["pickup_channel"]
					type = 22
				text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
				bot.edit_message_caption(chat_id=cidx,
										 message_id=data_order[1],
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.select_courier_or_pickup(type, order_id))
				if data[6] == 8:
					top_couriers = db_cmd.get_user_data_by_role(12)
					url_order = f'https://t.me/c/{str(cidx)[4:]}/{data_order[1]}'
					for fxx in top_couriers:
						top_courier_id = fxx[0]
						try:
							bot.send_message(chat_id=top_courier_id,
											text=text_cnf["delivery_cancel_car_crash2"].format(
												username, url_order),
											parse_mode=None,
											reply_markup=markup.main_menu())
						except:
							pass
				else:
					top_couriers = db_cmd.get_user_data_by_role(17)
					url_order = f'https://t.me/c/{str(cidx)[4:]}/{data_order[1]}'
					for fxx in top_couriers:
						top_courier_id = fxx[0]
						try:
							bot.send_message(chat_id=top_courier_id,
											text=text_cnf["delivery_cancel_car_crash2"].format(
												username, url_order),
											parse_mode=None,
											reply_markup=markup.main_menu())
						except:
							pass
	except Exception as e:
		logging.error(f'Error in car_crash: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("cpn"))
def callback_cpn(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data.split('#')[2])
			price = int(call.data.split('#')[1])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			dataxx = ast.literal_eval(data_order[5])
			dataxx["courier"] = price
			db_cmd.update_order(order_id, 'data', str(dataxx))
			bot.answer_callback_query(
				callback_query_id=call.id, text=text_cnf["change_price_confirm"])
			bot.delete_message(cid, mid)
			if data_order[6] == 1:
				old_status = data_order[3]
				dopf.return_order(order_id)
				if old_status == 3:
					config = dopf.readJs()
					data_order = db_cmd.get_order_by_order_id(order_id)
					if data_order[4] in [12, 33]:
						cidx = config["telegram"]["сourier_channel"]
						type = 12
					else:
						cidx = config["telegram"]["pickup_channel"]
						type = 22
					data_orderx = ast.literal_eval(data_order[5])
					db_cmd.update_order(order_id, 'status_order', 3)
					db_cmd.update_order(order_id, 'data', str(data_orderx))
					db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
					dopf.take_courier_and_storage(db_cmd.get_order_by_order_id(order_id))
					dopf.update_price()
					if data_order[4] in [33, 38]:
						dopf.take_courier_and_storage2(db_cmd.get_order_by_order_id(order_id))
						dopf.update_price()
					text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
					bot.edit_message_caption(chat_id=cidx,
											 message_id=data_order[1],
											 caption=text,
											 parse_mode=None,
											 reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))
				elif old_status == [4, 5, 6]:
					config = dopf.readJs()
					data_order = db_cmd.get_order_by_order_id(order_id)
					if data_order[4] in [12, 33]:
						cidx = config["telegram"]["сourier_channel"]
						type = 12
					else:
						cidx = config["telegram"]["pickup_channel"]
						type = 22
					datax = ast.literal_eval(data_order[5])
					data_orderx = ast.literal_eval(data_order[5])
					db_cmd.update_order(order_id, "status_order", old_status)
					db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
					text2 = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
					bot.edit_message_caption(chat_id=cidx,
											 message_id=data_order[1],
											 caption=text2,
											 parse_mode=None,
											 reply_markup=markup.change_pay_cur(type, datax["courier"], order_id))
			else:
				if data_order[4] in [12, 33]:
					cidx = config["telegram"]["сourier_channel"]
					type = 12
				else:
					cidx = config["telegram"]["pickup_channel"]
					type = 22
				text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
				bot.edit_message_caption(chat_id=cidx,
										 message_id=data_order[1],
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.change_pay_cur(type, dataxx["courier"], order_id))
	except Exception as e:
		logging.error(f'Error in cpn: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("order_confirm"))
def callback_order_confirm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[13:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if uid == data_order[7]:
				if data[6] == 8:
					cidx = config["telegram"]["сourier_channel"]
					type = 12
				else:
					cidx = config["telegram"]["pickup_channel"]
					type = 22
				data_orderx = ast.literal_eval(data_order[5])
				grm = 0
				for product in data_orderx["product"]:
					if product[1] != "שקל":
						grm += product[0]
				try:
					if grm <= 60:
						data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[2]
					else:
						data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[3]
				except:
					data_orderx["courier"] = 0
				chx = True
				try:
					if "correct_product" in data_orderx:
						if not dopf.conformity(data_orderx["product"], data_orderx["correct_product"]):
							data_orderx["correct_product"], chx = dopf.calibration(
								data_orderx["product"], data_order[7])
					else:
						data_orderx["correct_product"], chx = dopf.calibration(
							data_orderx["product"], data_order[7])
				except Exception as e:
					print(e)
					data_orderx["correct_product"], chx = dopf.calibration(
						data_orderx["product"], data_order[7])
				if dopf.check_cur_and_order(data_orderx["correct_product"], ast.literal_eval(db_cmd.get_user_data(uid)[5])["product"]) and chx:
					if type == 12:
						bot.edit_message_caption(chat_id=cid,
												 message_id=mid,
												 caption=text_cnf["order_confirm_all2"].format(
													 data_orderx["courier"]),
												 parse_mode=None,
												 reply_markup=None)
					else:
						bot.edit_message_caption(chat_id=cid,
												 message_id=mid,
												 caption=text_cnf["order_confirm_all"],
												 parse_mode=None,
												 reply_markup=None)
					db_cmd.update_order(order_id, 'status_order', 3)
					db_cmd.update_order(order_id, 'data', str(data_orderx))
					db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
					dopf.take_courier_and_storage(db_cmd.get_order_by_order_id(order_id))
					dopf.update_price()
					if data_order[4] in [33, 38]:
						dopf.take_courier_and_storage2(db_cmd.get_order_by_order_id(order_id))
						dopf.update_price()
					text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
					bot.edit_message_caption(chat_id=cidx,
											 message_id=data_order[1],
											 caption=text,
											 parse_mode=None,
											 reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))
				else:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["next_cnf"])
	except Exception as e:
		logging.error(f'Error in order_confirm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "confirm_sw_order")
def callback_confirm_sw_order(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [10] and data[3] == 1 and data[2] == 3:
			datax = ast.literal_eval(data[4])
			order_id = datax["active"]
			dataxx = datax["correct_order"]
			data_order = db_cmd.get_order_warehouse_by_id(order_id)
			dataf = ast.literal_eval(data_order[4])
			dataf["correct_product"] = dataxx
			db_cmd.update_order_w(order_id, 'data', str(dataf))
			config = dopf.readJs()
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=markup.active_order_sw(order_id))
			cidx = config["telegram"]["warehouse_channel"]
			text = dopf.get_text_by_warehouse_order_next2(
				db_cmd.get_order_warehouse_by_id(order_id))
			db_cmd.update_user(uid, "state", 0)
			bot.edit_message_text(chat_id=cidx,
								  message_id=data_order[1],
								  text=text,
								  parse_mode=None,
								  reply_markup=markup.menu_cnlwhx())
		elif data[6] in [10] and data[3] == 1 and data[2] == 13:
			datax = ast.literal_eval(data[4])
			order_id = datax["active"]
			dataxx = datax["true_order"]
			data_order = db_cmd.get_order_warehouse_by_id(order_id)
			dataf = ast.literal_eval(data_order[4])
			dataf["true_product"] = dataxx
			flag = 0
			if 'order_id' in dataf:
				orderx_data = ast.literal_eval(db_cmd.get_order_by_order_id(dataf["order_id"])[5])
				for i in orderx_data["true_product"]:
					if i[1] == "שקל":
						dataxx.append(i)
						break
				orderx_data["true_product"] = dataxx
				orderx_data["stk"] = 1
				db_cmd.update_order(dataf["order_id"], 'data', str(orderx_data))
				flag = 1
			true_now = []
			for prx in dataf["true_product"]:
				if prx[1] != "שקל":
					true_now.append(prx)
			dataf["true_product"] = true_now
			db_cmd.update_order_w(order_id, 'data', str(dataf))
			db_cmd.update_order_w(order_id, 'status_order', 6)
			config = dopf.readJs()
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=None)
			cidx = config["telegram"]["warehouse_channel"]
			db_cmd.update_user(uid, "state", 0)
			dataxxx = ast.literal_eval(db_cmd.get_order_warehouse_by_id(order_id)[4])
			summx, rez = dopf.eqal2(dataxxx["product"], dataxxx["true_product"])
			###
			if flag == 0 and summx >= 50:
				cur_id = data_order[2]
				text_ff = text_cnf["cur_penalty"].format(db_cmd.get_user_data(cur_id)[1], order_id, str(cidx)[
														 4:], data_order[1], round(float(summx), 2))
				db_cmd.update_bank(
					cur_id, round(float(db_cmd.get_user_bank(cur_id)[1]), 2) - round(float(summx), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=cur_id, money=-round(float(summx), 2))
				db_cmd.update_bank(
					0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(summx - rez), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=0, money=round(float(summx - rez), 2), payer_id=cur_id)
				db_cmd.update_bank(
					1, round(float(db_cmd.get_user_bank(1)[1]), 2) + round(float(rez), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=1, money=round(float(rez), 2), payer_id=cur_id)
				bot.send_message(config["telegram"]["penalties_channel"], text=text_ff)
			elif flag == 0 and summx > 0 and summx < 50:
				cur_id = data_order[2]
				text_ff = text_cnf["cur_penalty2"].format(db_cmd.get_user_data(cur_id)[1], order_id, str(cidx)[
														 4:], data_order[1], round(float(summx), 2))
				db_cmd.update_bank(
					1, round(float(db_cmd.get_user_bank(1)[1]), 2) - round(float(summx), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=1, money=-round(float(summx), 2))
				db_cmd.update_bank(
					0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(summx - rez), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=0, money=round(float(summx - rez), 2), payer_id=1)
				db_cmd.update_bank(
					1, round(float(db_cmd.get_user_bank(1)[1]), 2) + round(float(rez), 2))
				db_cmd.add_financial_operation(
					id_order=-int(order_id), user_id=1, money=round(float(rez), 2), payer_id=1)
				bot.send_message(config["telegram"]["penalties_channel"], text=text_ff)
			###
			dopf.take_courier_and_storage_cur_fx(dataxxx, data_order[2])
			dopf.update_price()
			dopf.add_warehouse(dataxxx["true_product"])
			dopf.update_price()
			text = dopf.get_text_by_warehouse_order_next3(
				db_cmd.get_order_warehouse_by_id(order_id))
			bot.edit_message_text(chat_id=cidx,
								  message_id=data_order[1],
								  text=text,
								  parse_mode=None,
								  reply_markup=None)
	except Exception as e:
		logging.error(f'Error in confirm_sw_order: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("client_now"))
def callback_client_now(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [7] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[10:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if uid == data_order[2]:
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=None)
				msg = bot.send_message(chat_id=data_order[7],
									   text=text_cnf["client_now2"].format(data_order[0]),
									   parse_mode=None,
									   reply_markup=markup.main_menu())
				db_cmd.add_to_dlt_list(data_order[7], msg.message_id)
	except Exception as e:
		logging.error(f'Error in client_now: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "new_order_sm")
def callback_new_order_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["select_type_delivery"],
									  reply_markup=markup.select_type_delivery())
	except Exception as e:
		logging.error(f'Error in new_order_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "supchainmng")
def callback_supchainmng(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["menu_supplies"],
									  reply_markup=markup.menu_supplies())
	except Exception as e:
		logging.error(f'Error in supchainmng: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "working_supplies")
def callback_working_supplies(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["open_refill"],
									  reply_markup=markup.supply_map())
	except Exception as e:
		logging.error(f'Error in working_supplies: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("zod"))
def callback_zod(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				datax = call.data.split("#")
				idx = int(datax[0][3:])
				statusx = int(datax[1])
				db_cmd.update_refill(idx, "status", statusx)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["open_refill"],
									  reply_markup=markup.supply_map())
	except Exception as e:
		logging.error(f'Error in zod: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("tgn"))
def callback_tgn(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				datax = call.data.split("#")
				idx = int(datax[0][3:])
				statusx = int(datax[1])
				db_cmd.update_status_stock(idx, statusx)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["text_product_stm"],
									  reply_markup=markup.product_map())
	except Exception as e:
		logging.error(f'Error in tgn: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "goods_cur")
def callback_goods_cur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				text = dopf.goods_cur()
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text,
									  reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				text = dopf.goods_cur2()
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in goods_cur: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "range")
def callback_range(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 5 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				text = text_cnf["text_product_stm"]
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text,
									  reply_markup=markup.product_map())
	except Exception as e:
		logging.error(f'Error in range: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "goods_stock")
def callback_goods_stock(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				text = dopf.storage_text_now()
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in goods_stock: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "return_backpuck")
def callback_return_backpuck(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=None)
				config = dopf.readJs()
				chat_warehouse = config["telegram"]["warehouse_channel"]
				pr = ast.literal_eval(data[5])["product"]
				pr2 = []
				for px in pr:
					if px[1] != "שקל":
						if px[0] != 0:
							pr2.append(px)
				all_active_order = db_cmd.check_cloesd_return_order_courier(uid)
				fgx = 0
				for el in all_active_order:
					order_data = db_cmd.get_order_by_order_id(el[0])
					dtx = ast.literal_eval(order_data[5])
					if "stk" in dtx:
						if dtx["stk"] == 0:
							fgx = 1
							break
				if len(pr2) == 0:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["text_clear_backpuck"])
				elif fgx == 1:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["text_no_comeback_backpuck"])
				else:
					product = str({"product": pr2})
					courier_id = uid
					db_cmd.add_order_warehouse2(courier_id, product)
					order_w = db_cmd.get_last_order_warehouse(courier_id)
					text = dopf.get_text_by_warehouse_order2(order_w)
					msgx = bot.send_message(chat_warehouse,
											text=text,
											parse_mode=None,
											reply_markup=markup.select_storage_worker2(order_w[0]))
					db_cmd.update_order_w(order_w[0], 'message_id_warehouse', msgx.message_id)
					bot.edit_message_reply_markup(chat_id=cid,
												  message_id=mid,
												  reply_markup=markup.backpuck_cr_kb2(uid))
					storage_worker_id = dopf.readJs("worker.json")["worker"]
					if storage_worker_id != 0:
						mid = msgx.message_id
						config = dopf.readJs()
						chat_warehouse = config["telegram"]["warehouse_channel"]
						order_w = db_cmd.get_order_warehouse_by_mid(mid)
						db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
						db_cmd.update_order_w(order_w[0], 'status_order', 5)
						order_w = db_cmd.get_order_warehouse_by_mid(mid)
						text = dopf.get_text_by_warehouse_order2(order_w)
						msg = bot.send_message(
							storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
						bot.edit_message_text(chat_id=chat_warehouse,
											  message_id=mid,
											  text=text,
											  parse_mode=None,
											  reply_markup=markup.menu_cnlwhx())
						db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in return_backpuck: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "courier_management")
def callback_courier_management(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.mng_cur_menu())
	except Exception as e:
		logging.error(f'Error in courier_management: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "general_report")
def callback_general_report(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				text = dopf.all_cur_report_day()
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in general_report: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "auto_storage_worker")
def callback_auto_storage_worker(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_worker"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.mng_worker_menu())
	except Exception as e:
		logging.error(f'Error in auto_storage_worker: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "new_supply")
def callback_new_supply(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				text = text_cnf["text_new_spl"]
				db_cmd.update_user(uid, 'state', 303)
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in new_supply: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "new_product_stm")
def callback_new_product_stm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				text = text_cnf["text_new_stm"]
				db_cmd.update_user(uid, 'state', 313)
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in new_product_stm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "comeback_order_w")
def callback_comeback_order_w(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 44)
				text = text_cnf["input_number_order_w"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in comeback_order_w: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "comeback_order")
def callback_comeback_order(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 144)
				text = text_cnf["input_number_order"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in comeback_order: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "change_order_money")
def callback_change_order_money(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 534)
				text = text_cnf["input_number_order"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in change_order_money: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "complete_order")
def callback_complete_order(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 311)
				text = text_cnf["input_number_order"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in comeplete_order: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "add_city")
def callback_add_city(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, "state", 211)
				text = text_cnf["text_cityf"]
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in add_city: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("switch"))
def callback_switch(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				worker_id = int(call.data.split("#")[1])
				data_u = db_cmd.get_user_data(worker_id)
				x = 9
				if data_u[6] == 9:
					x = 8
				db_cmd.update_user(worker_id, "type_user", x)
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.mng_cur_menu())
	except Exception as e:
		logging.error(f'Error in switch: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("sjubf"))
def callback_sjubf(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				worker_id = int(call.data.split("#")[1])
				cur_x = dopf.readJs("courier.json")
				cur_x["courier"] = worker_id
				with open('courier.json', 'w', encoding='utf-8') as settings_file:
					json.dump(cur_x, settings_file,
							  ensure_ascii=False, indent=2)
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.mng_cur_menu())
	except Exception as e:
		logging.error(f'Error in sjubf: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("kjubf"))
def callback_kjubf(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_worker"]
				worker_id = int(call.data.split("#")[1])
				cur_x = dopf.readJs("worker.json")
				cur_x["worker"] = worker_id
				with open('worker.json', 'w', encoding='utf-8') as settings_file:
					json.dump(cur_x, settings_file,
							  ensure_ascii=False, indent=2)
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.mng_worker_menu())
	except Exception as e:
		logging.error(f'Error in kjubf: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("xluszp"))
def callback_xluszp(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 17] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				worker_id = int(call.data.split("#")[1])
				bot.edit_message_reply_markup(chat_id=cid, message_id=mid,
											  reply_markup=markup.mng_cur_menu2(worker_id))
	except Exception as e:
		logging.error(f'Error in xluszp: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("zpm"))
def callback_zpm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				db_cmd.update_user(uid, "state", 111)
				worker_id = int(call.data.split("#")[1])
				datax = {"select": worker_id}
				db_cmd.update_user(uid, "data", str(datax))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text_cnf["send_worker_zp"],
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in zpm: {e}')

@bot.callback_query_handler(func=lambda call: call.data.startswith("tgy"))
def callback_tgy(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1:
				element_id = int(call.data.split("#")[1])
				#datax = {"element": element_id}
				db_cmd.update_user(uid, "state", 0)
				refill = db_cmd.get_product_refill_by_id(element_id)
				name = db_cmd.get_product_by_num(refill[1])[1]
				textx = text_cnf["size_refill_page"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]))
				#db_cmd.update_user(uid, "data", str(datax))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=textx,
									  reply_markup=markup.main_refill(element_id))
	except Exception as e:
		logging.error(f'Error in tgy: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("csr"))
def callback_csr(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				element_id = int(call.data.split("#")[1])
				datax = {"element": element_id}
				refill = db_cmd.get_product_refill_by_id(element_id)
				name = db_cmd.get_product_by_num(refill[1])[1]
				db_cmd.update_user(uid, "data", str(datax))
				db_cmd.update_user(uid, "state", 173)
				textx = text_cnf["amount_change_refill"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=textx,
									  reply_markup=markup.editprice_refill_kb(element_id))
	except Exception as e:
		logging.error(f'Error in csr: {e}')

@bot.callback_query_handler(func=lambda call: call.data.startswith("csd"))
def callback_csd(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				element_id = int(call.data.split("#")[1])
				datax = {"element": element_id}
				refill = db_cmd.get_product_refill_by_id(element_id)
				name = db_cmd.get_product_by_num(refill[1])[1]
				db_cmd.update_user(uid, "data", str(datax))
				db_cmd.update_user(uid, "state", 174)
				textx = text_cnf["price_change_refill"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[5]) + float(refill[6]))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=textx,
									  reply_markup=markup.editprice_refill_kb(element_id))
	except Exception as e:
		logging.error(f'Error in csd: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("ctw"))
def callback_ctw(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				element_id = int(call.data.split("#")[1])
				datax = {"element": element_id}
				refill = db_cmd.get_product_refill_by_id(element_id)
				name = db_cmd.get_product_by_num(refill[1])[1]
				db_cmd.update_user(uid, "data", str(datax))
				db_cmd.update_user(uid, "state", 175)
				textx = text_cnf["rubbish_change_refill"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=textx,
									  reply_markup=markup.editprice_refill_kb(element_id))
	except Exception as e:
		logging.error(f'Error in ctw: {e}')

@bot.callback_query_handler(func=lambda call: call.data.startswith("pluszp"))
def callback_xluszp(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12] and data[3] == 1 and data[2] == 0:
				text = text_cnf["panel_mng_cur_and_pickup"]
				worker_id = int(call.data.split("#")[1])
				db_cmd.update_bank(902167185, round(
					float(db_cmd.get_user_bank(902167185)[1]), 2) - 250)
				db_cmd.add_financial_operation(
					id_order=-1, user_id=902167185, money=-250)
				# top 2 522350229
				db_cmd.update_bank(522350229, round(
					float(db_cmd.get_user_bank(522350229)[1]), 2) - 250)
				db_cmd.add_financial_operation(
					id_order=-1, user_id=522350229, money=-250)
				db_cmd.update_bank(worker_id, round(
					float(db_cmd.get_user_bank(worker_id)[1]), 2) + 500)
				db_cmd.add_financial_operation(
					id_order=-1, user_id=worker_id, money=500)
				bot.edit_message_reply_markup(chat_id=cid, message_id=mid,
											  reply_markup=markup.mng_cur_menu())
	except Exception as e:
		logging.error(f'Error in xluszp: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "getproducts_courier")
def callback_getproducts_courier(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 41)
				msgx = bot.send_message(uid,
										text=text_cnf["send_list_product"],
										parse_mode=None,
										reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msgx.message_id)
	except Exception as e:
		logging.error(f'Error in getproducts_courier: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("editsm"))
def callback_editsm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				order_id = int(call.data[6:])
				data_order = db_cmd.get_order_by_order_id(order_id)

				if not data_order[7] or dopf.checkxcur(data_order):
					if data_order[4] == 12:
						db_cmd.update_user(uid, 'state', 15)
					elif data_order[4] == 22:
						db_cmd.update_user(uid, 'state', 25)
					elif data_order[4] == 33:
						db_cmd.update_user(uid, 'state', 41)
					elif data_order[4] == 38:
						db_cmd.update_user(uid, 'state', 46)
					mass = {"order_id": order_id}
					db_cmd.update_user(uid, 'data', str(mass))
					bot.send_message(chat_id=cid,
									 text=text_cnf["sm_photo"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in editsm: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("exchangesm"))
def callback_exchangesm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				order_id = int(call.data[10:])
				data_order = db_cmd.get_order_by_order_id(order_id)
				db_cmd.update_user(uid, 'state', 30)
				mass = {"order_id": order_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(chat_id=cid,
								 text=text_cnf["select_type_delivery"],
								 parse_mode=None,
								 reply_markup=markup.select_type_delivery())
	except Exception as e:
		logging.error(f'Error in exchangesm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "earnings_sm")
def callback_earnings_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [7] and data[3] == 1 and data[2] == 0:
				now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
				datax = db_cmd.get_financial_operation_by_user_last(uid)
				money_yd = 0
				for operation in datax:
					try:
						orderx = db_cmd.get_order_by_order_id(operation[1])
						date_operation = datetime.datetime.strptime(
							orderx[8], '%Y-%m-%d %H:%M:%S.%f')
						if date_operation < now + timedelta(hours=9) and date_operation > now - timedelta(hours=15):
							money_yd += float(operation[3])
					except:
						pass
				text = text_cnf["text_money_sm"].format(round(
					float(db_cmd.get_user_bank(uid)[1]), 2), round(money_yd, 2))
				bot.edit_message_text(chat_id=cid, message_id=mid, text=text, parse_mode=None,
									  reply_markup=markup.main_sm_earning())
	except Exception as e:
		logging.error(f'Error in earnings_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "creat_report_sm")
def callback_creat_report_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [7] and data[3] == 1 and data[2] == 0:
				now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
				datax = db_cmd.get_financial_operation_by_user_last(uid)
				list_xxx = []
				for operation in datax:
					orderx = db_cmd.get_order_by_order_id(operation[1])
					date_operation = datetime.datetime.strptime(
						orderx[8], '%Y-%m-%d %H:%M:%S.%f')
					if date_operation < now + timedelta(hours=9) and date_operation > now - timedelta(hours=15) and operation[1] != -1:
						list_xxx.append(operation[1])
				fff = open(f'{uid}.txt', 'w', encoding='utf-8')
				all_cur = 0
				all_money = 0
				all_s = 0
				data_l = []
				all_text = ""
				for el in list_xxx:
					if db_cmd.get_order_by_order_id(el)[3] == 3 and db_cmd.get_order_by_order_id(el)[4] < 30:
						dd = ast.literal_eval(db_cmd.get_order_by_order_id(el)[5])
						try:
							cur = dd["courier"]
						except:
							cur = 0
						try:
							money = dd["money"]
							text = ""
							s = 0
							for el in dd["correct_product"]:
								s += float(el[0]) * float(el[2])
								text += f"{el[0]} x {el[2]} = {float(el[0])*float(el[2])}  {el[1]}\n"
								f = 0
								for x in range(len(data_l)):
									if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
										data_l[x][0] += el[0]
										f = 1
										break
								if f == 0:
									data_l.append(el)
							all_text += 'Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + "Общая цена товара " + str(
								s) + " Прибыль " + str(round(int(money) - s - cur, 2)) + "\n\n"
							all_cur += cur
							all_money += int(money)
							all_s += s
						except:
							print(2)
					elif db_cmd.get_order_by_order_id(el)[3] == 3 and db_cmd.get_order_by_order_id(el)[4] > 30:
						dd = ast.literal_eval(db_cmd.get_order_by_order_id(el)[5])
						try:
							cur = dd["courier"]
						except:
							cur = 0
						text = ""
						s = 0
						money = 0
						for el in dd["correct_product"]:
							if el[1] != "שקל":
								s += float(el[0]) * float(el[2])
								text += f"{el[0]} x {el[2]} = {float(el[0])*float(el[2])}  {el[1]}\n"
								f = 0
								for x in range(len(data_l)):
									if data_l[x][1] == el[1] and data_l[x][2] == el[2]:
										data_l[x][0] += el[0]
										f = 1
										break
								if f == 0:
									data_l.append(el)
							else:
								money -= int(el[0])
						for el in dd["product2"]:
							if el[1] != "שקל":
								s -= float(el[0]) * float(db_cmd.get_product_by_name(el[1])[2])
								text += f"- {el[0]} x {db_cmd.get_product_by_name(el[1])[2]} = -{float(el[0]) * float(db_cmd.get_product_by_name(el[1])[2])}  {el[1]}\n"
								f = 0
								for x in range(len(data_l)):
									if data_l[x][1] == el[1] and data_l[x][2] == db_cmd.get_product_by_name(el[1])[2]:
										data_l[x][0] -= el[0]
										f = 1
										break
								if f == 0:
									data_l.append(
										[-1 * el[0], el[1], db_cmd.get_product_by_name(el[1])[2]])
							else:
								money += int(el[0])

						all_text += 'Деньги = ' + str(money) + " Курьер = " + str(cur) + "\n" + text + "\n" + \
							"Общая цена товара " + str(s) + " Прибыль " + \
							str(round(money - s - cur, 2)) + "\n\n"
						all_cur += cur
						all_money += money
						all_s += s
					else:
						print(1)
						# print(db_cmd.get_order_by_order_id(el))
				all_text += "Общая на курьеров " + str(all_cur) + " Общая сумма " + str(
					all_money) + " Общая цена товара за все заказы " + str(all_s) + " Прибыль " + str(all_money - all_s - all_cur) + "\n\n"

				for y in data_l:
					all_text += f'{y[1]} {y[2]} - {y[0]} грамм\n'
					all_text += f'Стоимость {float(y[0]) * float(y[2])}\n'

				fff.write(all_text)
				fff.close()
				# doc = open('/tmp/file.txt', 'rb')
				fff = open(f'{uid}.txt', 'rb')
				bot.send_document(uid, fff)
				fff.close()
	except Exception as e:
		logging.error(f'Error in creat_report_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("smdlt"))
def callback_smdlt(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				order_id = int(call.data[5:])
				msg = bot.send_message(chat_id=cid,
									   text=text_cnf["confirm_dlt_sm"],
									   parse_mode=None,
									   reply_markup=markup.confirm_dlt_sm(order_id))
				db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in smdlt: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("confirmdltsm"))
def callback_confirmdltsm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(uid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				order_id = int(call.data[12:])
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["dlt_order_sm2"],
									  parse_mode=None,
									  reply_markup=None)
				db_cmd.update_order(order_id, 'status_order', 6)
				db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
				data_order = db_cmd.get_order_by_order_id(order_id)
				data_orderx = ast.literal_eval(data_order[5])
				data_orderx["courier"] = 0
				db_cmd.update_order(order_id, 'data', str(data_orderx))
				config = dopf.readJs()
				if data_order[4] in [12, 33]:
					type = 12
					chat_order = config["telegram"]["сourier_channel"]
				elif data_order[4] in [22, 38]:
					type = 22
					chat_order = config["telegram"]["pickup_channel"]
				text2 = dopf.get_text_order_next_step(data_order)
				bot.edit_message_caption(
					chat_id=chat_order, message_id=data_order[1], caption=text2, parse_mode=None, reply_markup=markup.change_pay_cur(type, data_orderx["courier"], order_id))
				if data_order[7]:
					text3 = dopf.get_text_order_next_step33(db_cmd.get_order_by_order_id(order_id))
					msgxx = bot.send_message(
						chat_id=data_order[7], text=text3)
					db_cmd.add_to_dlt_list(data_order[7], msgxx.message_id)
				if type == 12:
					mng_curs= db_cmd.get_user_data_by_role(12)
					url_orderf = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
					for fxx in mng_curs:
						mng_cur_id = fxx[0]
						try:
							bot.send_message(mng_cur_id, text=text_cnf["dltordersm"].format(url_orderf))
						except:
							pass
				else:
					mng_curs= db_cmd.get_user_data_by_role(17)
					url_orderf = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
					for fxx in mng_curs:
						mng_cur_id = fxx[0]
						try:
							bot.send_message(mng_cur_id, text=text_cnf["dltordersm"].format(url_orderf))
						except:
							pass
				if data_order[6] == 2:
					ow_list = db_cmd.get_last10_order_warehouse(data_order[7])
					for ow in ow_list:
						dtx = ast.literal_eval(ow[4])
						if "order_id" in dtx:
							if dtx["order_id"] == order_id:
								mng_st_list = db_cmd.get_user_data_by_role(5)
								text_fmng = text_cnf["mng_delete_order"].format(
									ow[0], str(config["telegram"]["warehouse_channel"])[4:], ow[1])

								for mng in mng_st_list:
									try:
										bot.send_message(mng[0], text=text_fmng)
									except:
										print(mng[0])
								break
	except Exception as e:
		logging.error(f'Error in confirmdltsm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "active_order_courier")
def callback_active_order_courier(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_active_order = db_cmd.check_active_order_courier(uid)
				for order in all_active_order:
					text = dopf.get_text_order_for_courier(order)
					photox = ast.literal_eval(order[5])["photo"]
					msg = bot.send_photo(chat_id=uid,
										 photo=photox,
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.active_order_cr_kb(order[0]))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in active_order_courier: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "completed_order_courier")
def callback_completed_order_courier(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_active_order = db_cmd.check_cloesd_return_order_courier(uid)
				for order in all_active_order:
					try:
						text = dopf.get_text_order_for_courier(order)
						photox = ast.literal_eval(order[5])["photo"]
						msg = bot.send_photo(chat_id=uid,
											 photo=photox,
											 caption=text,
											 parse_mode=None,
											 reply_markup=markup.closed_order_kb_c(order[0]))
						db_cmd.add_to_dlt_list(uid, msg.message_id)
					except Exception as e:
						print(e, "completed_order_courier2")
				if not all_active_order or len(all_active_order) == 0:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["not_completed_order_c"])
	except Exception as e:
		logging.error(f'Error in completed_order_courier: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "report_cur_cur")
def callback_report_cur_cur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				list_orders = db_cmd.get_last200_order_cur(uid)
				textf = dopf.text_report_cur(list_orders, uid)
				lensx = len(textf)
				for i in range(lensx):
					if i == lensx - 1:
						msg = bot.send_message(uid, text=textf,
										 reply_markup=markup.cur_cur_order_kb())
						db_cmd.add_to_dlt_list(uid, msg.message_id)
					else:
						msg = bot.send_message(uid, text=textf,
										 reply_markup=None)
						db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in report_cur_cur: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "report_cur_cur_ystd")
def callback_report_cur_cur_ystd(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				list_orders = db_cmd.get_last200_order_cur(uid)
				textf = dopf.text_report_cur_ystd(list_orders, uid)
				lensx = len(textf)
				for i in range(lensx):
					if i == lensx - 1:
						msg = bot.send_message(uid, text=textf, parse_mode="Markdown",
										 reply_markup=markup.cur_cur_order_kb())
						db_cmd.add_to_dlt_list(uid, msg.message_id)
					else:
						msg = bot.send_message(uid, text=textf, parse_mode="Markdown",
										 reply_markup=None)
						db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in report_cur_cur_ystd: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "now_products_courier")
def callback_now_products_courier(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 0)
				config = dopf.readJs()
				cur_backpuck = ast.literal_eval(db_cmd.get_user_data(uid)[5])["product"]
				text, money, bank = dopf.cur_backpuck_text(cur_backpuck, uid)
				text = text_cnf["earnings_cur"].format(bank) + text
				msg = bot.send_message(chat_id=uid,
									   text=text,
									   parse_mode=None,
									   reply_markup=markup.backpuck_cr_kb(uid))
				db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in now_products_courier: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "get_cash_cur")
def callback_get_cash_cur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, "state", 51)
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=markup.backpuck_cr_kb(uid))
			elif data[6] in [8, 9] and data[3] == 1 and data[2] == 51:
				db_cmd.update_user(uid, "state", 0)
				cur_backpuck = ast.literal_eval(db_cmd.get_user_data(uid)[5])["product"]
				for el in cur_backpuck:
					if el[1] == "שקל":
						el[0] = round(float(el[0]) - float(db_cmd.get_user_bank(uid)[1]), 2)
						db_cmd.update_bank(uid, 0)
				datax = ast.literal_eval(db_cmd.get_user_data(uid)[5])
				datax["product"] = cur_backpuck
				db_cmd.update_user(uid, 'on_hands', str(datax))
				text, money, bank = dopf.cur_backpuck_text(cur_backpuck, uid)
				text = text_cnf["earnings_cur"].format(bank) + text
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text,
									  parse_mode=None,
									  reply_markup=markup.backpuck_cr_kb(uid))
	except Exception as e:
		logging.error(f'Error in get_cash_cur: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "complite_storage_order")
def callback_complite_storage_order(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_complite_order_w = db_cmd.get_complite_order_warehouse(uid)
				for order_w in all_complite_order_w:
					text = dopf.get_text_by_warehouse_order_next(order_w)
					msg = bot.send_message(uid,
										   text=text,
										   parse_mode=None,
										   reply_markup=markup.complite_order_w(order_w[0]))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in complite_storage_order: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "active_order_storage_w")
def callback_active_order_storage_w(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [10] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_active_order = db_cmd.check_new_order_sw(uid)
				for order in all_active_order:
					if order[3] == 1:
						try:
							if ast.literal_eval(order[4])["correct_product"]:
								text = dopf.get_text_by_warehouse_order_next2(order)
							else:
								text = dopf.get_text_by_warehouse_order_next(order)
						except:
							text = dopf.get_text_by_warehouse_order_next(order)
						msg = bot.send_message(uid,
											   text=text,
											   parse_mode=None,
											   reply_markup=markup.active_order_sw(order[0]))
						db_cmd.add_to_dlt_list(uid, msg.message_id)
					elif order[3] == 5:
						text = dopf.get_text_by_warehouse_order2(order)
						msg = bot.send_message(uid,
											   text=text,
											   parse_mode=None,
											   reply_markup=markup.active_order_sw2(order[0]))
						db_cmd.add_to_dlt_list(uid, msg.message_id)

	except Exception as e:
		logging.error(f'Error in active_order_storage_w: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "active_order_sm")
def callback_active_order_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [7] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_active_order = db_cmd.get_active_order_sm(uid)
				for order in all_active_order:
					text = dopf.get_text_order_next_step_sm(order)
					photo = ast.literal_eval(order[5])["photo"]
					msg = bot.send_photo(chat_id=uid,
										 photo=photo,
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.client_now(order[0]))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
				if not all_active_order:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["donothave_active_order_sm"])
	except Exception as e:
		logging.error(f'Error in active_order_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "history_order_sm")
def callback_history_order_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [7] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_cloesed_order = db_cmd.get_cloesed_order_sm(uid)
				day1to2 = []
				for order in all_cloesed_order:
					try:
						datax = datetime.datetime.now() - timedelta(days=2)
						datax2 = datetime.datetime.strptime(order[9], '%Y-%m-%d %H:%M:%S.%f')
						if datax2 > datax:
							day1to2.append(order)
					except:
						pass
				for order in day1to2:
					text = dopf.get_text_order_next_step_sm(order)
					photo = ast.literal_eval(order[5])["photo"]
					msg = bot.send_photo(chat_id=uid,
										 photo=photo,
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.cloesed_order_sm_kb(order[0]))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
				if not day1to2:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["donothave_closed_order_sm"])
	except Exception as e:
		logging.error(f'Error in history_order_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "history_order_sm2")
def callback_history_order_sm2(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [7] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_cloesed_order = db_cmd.get_cloesed_order_sm(uid)
				day1to2 = []
				for order in all_cloesed_order:
					datax = datetime.datetime.now() - timedelta(days=7)
					datax2 = datetime.datetime.strptime(order[9], '%Y-%m-%d %H:%M:%S.%f')
					if datax2 > datax:
						day1to2.append(order)
				for order in day1to2:
					text = dopf.get_text_order_next_step_sm(order)
					photo = ast.literal_eval(order[5])["photo"]
					msg = bot.send_photo(chat_id=uid,
										 photo=photo,
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.cloesed_order_sm_kb(order[0]))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
					time.sleep(0.2)
				if not day1to2:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["donothave_closed_order_sm"])
	except Exception as e:
		logging.error(f'Error in history_order_sm2: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "back_main_sm")
def callback_back_main_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] in [0, 15, 25, 16, 26, 30]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["menu_sales_manager"],
									  reply_markup=markup.menu_sales_manager(uid))
			elif data[6] == 10 and data[3] == 1 and data[2] in [3]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  parse_mode=None,
									  text=text_cnf["menu_storage_worker"],
									  reply_markup=markup.menu_storage(uid))
			elif data[6] in [8, 9]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["menu_courier"],
									  parse_mode=None,
									  reply_markup=markup.menu_courier(uid))
			elif data[6] in [12]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["menu_manager_courier_and_pickup"],
									  parse_mode=None,
									  reply_markup=markup.menu_manager_courier_and_pickup())
			elif data[6] in [5]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["menu_sales_manager"],
									  parse_mode=None,
									  reply_markup=markup.menu_storage_manager())
			elif data[6] in [17]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["menu_top_mng"],
									  parse_mode=None,
									  reply_markup=markup.menu_top_mng())
			elif data[6] in [6]:
				db_cmd.update_user(uid, 'state', 0)
				money = ast.literal_eval(data[4])['money']
				textx = text_cnf["cashier_menu"].format(money)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=textx,
									  parse_mode=None,
									  reply_markup=markup.menu_cashier())
			elif data[6] in [15]:
				db_cmd.update_user(uid, 'state', 0)
				money = ast.literal_eval(data[4])['money']
				textx = text_cnf["accountant_menu"].format(money)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=textx,
									  parse_mode=None,
									  reply_markup=markup.menu_accountant())
	except Exception as e:
		logging.error(f'Error in back_main_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "back_sm")
def callback_back_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] in [10, 20]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["select_type_delivery"],
									  reply_markup=markup.select_type_delivery())
			elif data[6] == 7 and data[3] == 1 and data[2] in [11, 21]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [15, 25]:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
	except Exception as e:
		logging.error(f'Error in back_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "courier_sm")
def callback_courier_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 10)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] == 30:
				db_cmd.update_user(uid, 'state', 31)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in courier_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "pickup_sm")
def callback_pickup_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 20)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [30, 35]:
				db_cmd.update_user(uid, 'state', 36)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_photo"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in pickup_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "cancel_sm")
def callback_cancel_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1:
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["menu_sales_manager"],
									  parse_mode=None,
									  reply_markup=markup.menu_sales_manager(uid))
	except Exception as e:
		logging.error(f'Error in cancel_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "try_sm")
def callback_try_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] in [12]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [22]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order_pu"],
									  parse_mode=None,
									  reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [17]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [27]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order_pu"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [33]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [38]:
				db_cmd.update_user(uid, 'state', data[2] - 1)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_cnf["sm_text_order_pu"],
									  parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in try_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "confirm_sm")
def callback_confirm_sm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			x = data[2]
			if data[6] == 7 and data[3] == 1 and data[2] in [12, 22]:
				config = dopf.readJs()
				if data[2] == 12:
					cidx = config["telegram"]["сourier_channel"]
				else:
					cidx = config["telegram"]["pickup_channel"]
				photo = ast.literal_eval(data[4])["new_order"]["photo"]
				dataxx = ast.literal_eval(data[4])["new_order"]
				if dopf.check_storage_now_xt(dataxx["data"]):
					db_cmd.add_order(uid, data[4], data[2])
					order_id = db_cmd.get_last_order(uid)[0]
					text = dopf.get_text_order_from_mk(data[4], username, data[2], order_id)
					message_ch = bot.send_photo(cidx, photo, caption=text,
												parse_mode=None, reply_markup=markup.select_courier_or_pickup(data[2], order_id))
					db_cmd.update_order(order_id, 'message_id_express', message_ch.message_id)
					db_cmd.update_user(uid, 'state', 0)
					bot.edit_message_reply_markup(chat_id=cid,
												  message_id=mid,
												  reply_markup=None)
					bot.send_message(cid,
									 text=text_cnf["confirm_order_dm"],
									 parse_mode=None,
									 reply_markup=None)
					bot.send_message(cid,
									 text=text_cnf["menu_sales_manager"],
									 parse_mode=None,
									 reply_markup=markup.menu_sales_manager(uid))
					cur_x = dopf.readJs("courier.json")["courier"]
					if x == 12 and cur_x != 0:
						courier_id = cur_x
						config = dopf.readJs()
						data_courier = db_cmd.get_user_data(courier_id)
						db_cmd.set_courier_or_pickup_order(
							message_ch.message_id, courier_id, data_courier[6])
						msg = bot.send_message(
							courier_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
						chat_order = config["telegram"]["сourier_channel"]
						order = db_cmd.get_order_by_message_id(
							message_ch.message_id, data_courier[6])
						db_cmd.update_order(order[0], "status_order", 1)
						text = dopf.get_text_order_next_step(
							db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6]))
						bot.edit_message_caption(chat_id=chat_order,
												 message_id=message_ch.message_id,
												 caption=text,
												 parse_mode=None,
												 reply_markup=markup.recourier_order(db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])[0]))
						db_cmd.add_to_dlt_list(courier_id, msg.message_id)
					elif len(db_cmd.get_user_data_by_role(9)) == 1 and x == 22:
						courier_id = db_cmd.get_user_data_by_role(9)[0][0]
						data_courier = db_cmd.get_user_data(courier_id)
						db_cmd.set_courier_or_pickup_order(
							message_ch.message_id, courier_id, data_courier[6])
						msg = bot.send_message(
							courier_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
						chat_order = config["telegram"]["pickup_channel"]
						order = db_cmd.get_order_by_message_id(
							message_ch.message_id, data_courier[6])
						db_cmd.update_order(order[0], "status_order", 1)
						text = dopf.get_text_order_next_step(
							db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6]))
						bot.edit_message_caption(chat_id=chat_order,
													message_id=message_ch.message_id,
													caption=text,
													parse_mode=None,
													reply_markup=markup.recourier_order(db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])[0]))
						db_cmd.add_to_dlt_list(courier_id, msg.message_id)
				else:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["no_products_by_order_warhous"])
			elif data[6] == 7 and data[3] == 1 and data[2] in [17, 27]:
				config = dopf.readJs()
				if data[2] == 17:
					cidx = config["telegram"]["сourier_channel"]
				else:
					cidx = config["telegram"]["pickup_channel"]
				data_new_order = ast.literal_eval(data[4])
				photo = data_new_order["new_order"]["photo"]
				datax = data_new_order["new_order"]["data"]
				datax["photo"] = photo
				order_id = data_new_order["order_id"]
				data_order = db_cmd.get_order_by_order_id(order_id)
				if not data_order[7]:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["no_curier_order"])
				elif dopf.checkxcur2(data_order, datax["product"]):
					datafx = ast.literal_eval(data_order[5])
					if "correct_product" in datafx:
						neww_data = datafx["correct_product"]
						old_data = datafx["product"]
						oldw_data = datax["product"]
						for el in old_data:
							for el2 in oldw_data:
								if el[1] == el2[1]:
									el[0] = round(float(el[0]) - float(el2[0]), 1)
									break
						for enn in old_data:
							for en in neww_data:
								if en[1] == enn[1] and enn[0] < en[0] and enn[0] >= 0:
									en[0] = round(en[0] - x, 1)
						datax["correct_product"] = neww_data
					if dopf.check_storage_now_xt(datax):
						db_cmd.update_order(order_id, 'data', str(datax))
						db_cmd.update_user(uid, 'state', 0)
						order_data = db_cmd.get_order_by_order_id(order_id)
						text = dopf.get_text_order_next_step(order_data)
						media = types.InputMediaPhoto(media=photo, caption=text, parse_mode=None)
						if data[2] == 17:
							top_curs = db_cmd.get_user_data_by_role(12)
							url_orderf = f'https://t.me/c/{str(cidx)[4:]}/{order_data[1]}'
							textfffx = text_cnf["mngeditordert"].format(url_orderf)
							for fxx in top_curs:
								top_cur_id = fxx[0]
								try:
									bot.send_message(chat_id=top_cur_id, text=textfffx)
								except:
									pass
						else:
							top_curs = db_cmd.get_user_data_by_role(17)
							url_orderf = f'https://t.me/c/{str(cidx)[4:]}/{order_data[1]}'
							textfffx = text_cnf["mngeditordert"].format(url_orderf)
							for fxx in top_curs:
								top_cur_id = fxx[0]
								try:
									bot.send_message(chat_id=top_cur_id, text=textfffx)
								except:
									pass
						bot.edit_message_media(chat_id=cidx,
											   message_id=order_data[1],
											   media=media,
											   reply_markup=markup.select_courier_or_pickup(data[2], order_id))
						bot.send_message(cid,
										 text=text_cnf["edit_order_dm"],
										 parse_mode=None,
										 reply_markup=None)
						bot.send_message(cid,
										 text=text_cnf["menu_sales_manager"],
										 parse_mode=None,
										 reply_markup=markup.menu_sales_manager(uid))
					else:
						bot.answer_callback_query(
							callback_query_id=call.id, text=text_cnf["no_products_by_order_warhous"])
				else:
					bot.answer_callback_query(
						callback_query_id=call.id, text=text_cnf["text_alert_ff2"])

			elif data[6] == 7 and data[3] == 1 and data[2] in [33, 38]:
				config = dopf.readJs()
				if data[2] == 33:
					cidx = config["telegram"]["сourier_channel"]
				else:
					cidx = config["telegram"]["pickup_channel"]
				data_new_order = ast.literal_eval(data[4])
				photo = data_new_order["new_order"]["photo"]
				datax = data_new_order["new_order"]["data"]
				datax["photo"] = photo
				datax["order_id"] = data_new_order["order_id"]
				db_cmd.add_order(uid, data[4], data[2])
				order_id = db_cmd.get_last_order(uid)[0]
				text = dopf.get_text_order_from_mk(data[4], username, data[2], order_id)
				message_ch = bot.send_photo(cidx, photo, caption=text,
											parse_mode=None, reply_markup=markup.select_courier_or_pickup(data[2], order_id))
				db_cmd.update_order(order_id, 'message_id_express', message_ch.message_id)
				db_cmd.update_user(uid, 'state', 0)
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=None)
				bot.send_message(cid,
								 text=text_cnf["confirm_order_dm"],
								 parse_mode=None,
								 reply_markup=None)
				bot.send_message(cid,
								 text=text_cnf["menu_sales_manager"],
								 parse_mode=None,
								 reply_markup=markup.menu_sales_manager(uid))
				cur_x = dopf.readJs("courier.json")["courier"]
				if x == 33 and cur_x != 0:
					courier_id = cur_x
					config = dopf.readJs()
					data_courier = db_cmd.get_user_data(courier_id)
					db_cmd.set_courier_or_pickup_order(
						message_ch.message_id, courier_id, data_courier[6])
					msg = bot.send_message(
						courier_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
					chat_order = config["telegram"]["сourier_channel"]
					order = db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])
					db_cmd.update_order(order[0], "status_order", 1)
					text = dopf.get_text_order_next_step(
						db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6]))
					bot.edit_message_caption(chat_id=chat_order,
											 message_id=message_ch.message_id,
											 caption=text,
											 parse_mode=None,
											 reply_markup=markup.recourier_order(db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])[0]))
				elif x == 38 and len(db_cmd.get_user_data_by_role(9)) == 1:
					courier_id = db_cmd.get_user_data_by_role(9)[0][0]
					data_courier = db_cmd.get_user_data(courier_id)
					db_cmd.set_courier_or_pickup_order(
						message_ch.message_id, courier_id, data_courier[6])
					msg = bot.send_message(
						courier_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
					chat_order = config["telegram"]["pickup_channel"]
					order = db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])
					db_cmd.update_order(order[0], "status_order", 1)
					text = dopf.get_text_order_next_step(
						db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6]))
					bot.edit_message_caption(chat_id=chat_order,
											 message_id=message_ch.message_id,
											 caption=text,
											 parse_mode=None,
											 reply_markup=markup.recourier_order(db_cmd.get_order_by_message_id(message_ch.message_id, data_courier[6])[0]))                             
			elif data[6] == 7 and data[3] == 1 and data[2] in [43, 48]:
				config = dopf.readJs()
				if data[2] == 43:
					cidx = config["telegram"]["сourier_channel"]
				else:
					cidx = config["telegram"]["pickup_channel"]
				data_new_order = ast.literal_eval(data[4])
				photo = data_new_order["new_order"]["photo"]
				datax = data_new_order["new_order"]["data"]
				datax["photo"] = photo
				datax["order_id"] = data_new_order["order_id"]
				order_id = data_new_order["order_id"]
				data_order = db_cmd.get_order_by_order_id(order_id)
				db_cmd.update_order(order_id, 'data', str(datax))
				db_cmd.update_user(uid, 'state', 0)
				order_data = db_cmd.get_order_by_order_id(order_id)
				text = dopf.get_text_order_next_step(order_data)
				media = types.InputMediaPhoto(media=photo, caption=text, parse_mode=None)
				if data[2] == 43:
					top_curs = db_cmd.get_user_data_by_role(12)
					url_orderf = f'https://t.me/c/{str(cidx)[4:]}/{order_data[1]}'
					textfffx = text_cnf["mngeditordert"].format(url_orderf)
					for fxx in top_curs:
						top_cur_id = fxx[0]
						try:
							bot.send_message(chat_id=top_cur_id, text=textfffx)
						except:
							pass
				else:
					top_curs = db_cmd.get_user_data_by_role(17)
					url_orderf = f'https://t.me/c/{str(cidx)[4:]}/{order_data[1]}'
					textfffx = text_cnf["mngeditordert"].format(url_orderf)
					for fxx in top_curs:
						top_cur_id = fxx[0]
						try:
							bot.send_message(chat_id=top_cur_id, text=textfffx)
						except:
							pass
				bot.edit_message_media(chat_id=cidx,
									   message_id=order_data[1],
									   media=media,
									   reply_markup=markup.select_courier_or_pickup(data[2], order_id))
				bot.send_message(cid,
								 text=text_cnf["edit_order_dm"],
								 parse_mode=None,
								 reply_markup=None)
				bot.send_message(cid,
								 text=text_cnf["menu_sales_manager"],
								 parse_mode=None,
								 reply_markup=markup.menu_sales_manager(uid))

	except Exception as e:
		logging.error(f'Error in confirm_sm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "new_order_cr")
def callback_new_order_cr(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [8, 9] and data[3] == 1 and data[2] == 0:
				config = dopf.readJs()
				all_new_order = db_cmd.check_new_order_courier(uid)
				msg_list = []
				for order in all_new_order:
					text = dopf.get_text_order_for_courier(order)
					photox = ast.literal_eval(order[5])["photo"]
					msg = bot.send_photo(chat_id=uid,
										 photo=photox,
										 caption=text,
										 parse_mode=None,
										 reply_markup=markup.courier_order_kb(order))
					db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in new_order_cr: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "mass_message_mng")
def callback_mass_message_mng(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 5] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 91)
				bot.send_message(chat_id=uid, text=text_cnf["send_msg_for_mng"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 91)
				msg = bot.send_message(chat_id=uid, text=text_cnf["send_msg_for_mng"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(cid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in mass_message_mng: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("tgy"))
def callback_tgy(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [5] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 86)
				if_refill = call.data[3:]
				bot.send_message(chat_id=uid, text=text_cnf["send_msg_for_mng"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in tgy(card_refill): {e}')



@bot.callback_query_handler(func=lambda call: call.data == "mass_message_cur")
def callback_mass_message_cur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 5] and data[3] == 1 and data[2] == 0:
				db_cmd.update_user(uid, 'state', 191)
				bot.send_message(chat_id=uid, text=text_cnf["send_msg_for_cur"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in mass_message_cur: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "cnlwhx")
def callback_cnlwhx(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(cid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [5] and data[3] == 1:
			db_cmd.delete_order_wh(mid)
			bot.delete_message(cid, mid)
	except Exception as e:
		logging.error(f'Error in cnlwhx: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "redlv")
def callback_redlv(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [12, 17] and data[3] == 1:
			config = dopf.readJs()
			if cid == config["telegram"]["сourier_channel"]:
				type_cur = 8
				xtype = 12
			elif cid == config["telegram"]["pickup_channel"]:
				type_cur = 9
				xtype = 22
			order = db_cmd.get_order_by_message_id(mid, type_cur)
			db_cmd.update_order(order[0], 'time', 0)
			db_cmd.update_order(order[0], 'status_order', 0)
			prod = ast.literal_eval(order[5])
			try:
				del prod["correct_product"]
			except:
				pass
			db_cmd.update_order(order[0], 'data', str(prod))
			orderx = db_cmd.get_order_by_order_id(order[0])
			textf = dopf.get_text_order_next_step(orderx)
			bot.edit_message_caption(chat_id=cid,
									 message_id=mid,
									 caption=textf,
									 parse_mode=None,
									 reply_markup=markup.select_courier_or_pickup(xtype, orderx[0]))
	except Exception as e:
		logging.error(f'Error in redlv: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("corr"))
def callback_cur_ordes_reposts(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [12, 17] and data[3] == 1:
			uidx = int(call.data.split("#")[1])
			text_n = text_cnf["select_cur_for_order"] + "\n\n"
			if uidx != 0:
				list_order = db_cmd.get_last200_order_cur(uidx)
				text_mass = dopf.text_report_cur(list_order, uidx)
				lensx = len(text_mass)
				bot.delete_message(chat_id=cid, message_id=mid)
				for i in range(lensx):
					if i == lensx - 1:
						bot.send_message(chat_id=cid,
										 text=f"```{text_mass[i]}```",
										 parse_mode="Markdown",
										 reply_markup=markup.report_cur_kb(uidx))
					else:
						bot.send_message(chat_id=cid,
										 text=f"```{text_mass[i]}```",
										 parse_mode="Markdown",
										 reply_markup=None)
			else:
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_n,
									  parse_mode="Markdown",
									  reply_markup=markup.report_cur_kb(uidx))
	except Exception as e:
		logging.error(f'Error in cur_ordes_reposts: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("cxrr"))
def callback_cur_ordes_reposts(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [12, 17] and data[3] == 1:
			uidx = int(call.data.split("#")[1])
			text_n = text_cnf["select_cur_for_order"] + "\n\n"
			if uidx != 0:
				list_order = db_cmd.get_last200_order_cur(uidx)
				text_mass = dopf.text_report_cur_ystd(list_order, uidx)
				lensx = len(text_mass)
				bot.delete_message(chat_id=cid, message_id=mid)
				for i in range(lensx):
					if i == lensx - 1:
						bot.send_message(chat_id=cid,
										 text=f"```{text_mass[i]}```",
										 parse_mode="Markdown",
										 reply_markup=markup.report_cur_kb(uidx))
					else:
						bot.send_message(chat_id=cid,
										 text=f"```{text_mass[i]}```",
										 parse_mode="Markdown",
										 reply_markup=None)
			else:
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text_n,
									  parse_mode="Markdown",
									  reply_markup=markup.report_cur_kb(uidx))
	except Exception as e:
		logging.error(f'Error in cur_ordes_reposts: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "rewhx")
def callback_rewhx(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [5, 12] and data[3] == 1:
			order_w = db_cmd.get_order_warehouse_by_mid(mid)
			if order_w[3] == 5:
				db_cmd.update_order_w(order_w[0], 'status_order', 4)
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=markup.select_storage_worker2(order_w[0]))
			elif order_w[3] in [1, 2]:
				db_cmd.update_order_w(order_w[0], 'status_order', 0)
				bot.edit_message_reply_markup(chat_id=cid,
											  message_id=mid,
											  reply_markup=markup.select_storage_worker(order_w[0]))
	except Exception as e:
		logging.error(f'Error in rewhx: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "trucash")
def callback_trucash(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [6] and data[3] == 1 and data[2] == 71:
			datax = ast.literal_eval(data[4])
			mch = config['telegram']['money_channel']
			money = datax["take"]
			cur_id = datax["cur"]
			datax["money"] += money
			cur_data = ast.literal_eval(db_cmd.get_user_data(cur_id)[5])
			cur_data["product"][0][0] = round(float(cur_data["product"][0][0] - money), 1)
			db_cmd.update_user(cur_id, 'on_hands', str(cur_data))
			db_cmd.update_user(uid, 'state', 0)
			db_cmd.update_user(uid, 'data', str(datax))
			bot.edit_message_text(chat_id=cid,
								  message_id=mid,
								  text=text_cnf["take_money_confirm"],
								  reply_markup=markup.main_sm())
			bot.send_message(chat_id=mch, text=text_cnf["info_for_cur_money"].format(
				db_cmd.get_user_data(cur_id)[1], money))
		if data[6] in [15] and data[3] == 1 and data[2] == 72:
			datax = ast.literal_eval(data[4])
			mch = config['telegram']['money_channel']
			money = datax["take"]
			cashx = db_cmd.get_user_data_by_role(6)[0]
			datax["money"] += money
			cur_data = ast.literal_eval(cashx[4])
			cur_data["money"] = round(float(cur_data["money"] - money), 1)
			db_cmd.update_user(cashx[0], 'data', str(cur_data))
			db_cmd.update_user(uid, 'state', 0)
			db_cmd.update_user(uid, 'data', str(datax))
			bot.edit_message_text(chat_id=cid,
								  message_id=mid,
								  text=text_cnf["take_money_confirm"],
								  reply_markup=markup.main_sm())
			bot.send_message(
				chat_id=mch, text=text_cnf["info_for_cur_money2"].format(cashx[1], money))
	except Exception as e:
		logging.error(f'Error in trucash: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "control_storage_worker")
def callback_control_storage_worker(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [5] and data[3] == 1:
			bot.edit_message_text(chat_id=cid, message_id=mid, text=text_cnf["select_worker_for_zp"],
								  reply_markup=markup.mng_worker_kb())
	except Exception as e:
		logging.error(f'Error in control_storage_worker: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "workon_with_kur")
def callback_workon_with_kur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [6] and data[3] == 1:
			bot.edit_message_text(chat_id=cid, message_id=mid, text=text_cnf["select_delivery_officer"],
								  reply_markup=markup.delivery_officer_kb())
	except Exception as e:
		logging.error(f'Error in workon_with_kur: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "warehouse_consumption")
def callback_warehouse_consumption(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		db_cmd.check_user_id(uid, username)
		data = db_cmd.get_user_data(uid)
		if data[6] in [5] and data[3] == 1:
			nowx = []
			now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
			textxx = ""
			datax = db_cmd.get_order_wh_by_yestrd()
			list_xxx = []
			for operation in datax:
				date_operation = datetime.datetime.strptime(
					operation[6], '%Y-%m-%d %H:%M:%S.%f')
				if date_operation < now + timedelta(hours=9) and date_operation > now - timedelta(hours=15):
					list_xxx.append(operation[0])
			for i in list_xxx:
				try:
					data = db_cmd.get_order_warehouse_by_id(i)
					if data[3] == 3 or data[3] == 2:
						datax = ast.literal_eval(data[4])["correct_product"]
						nowx = dopf.plus_ss(datax, nowx)
					elif data[3] == 6:
						datax = ast.literal_eval(data[4])["true_product"]
						nowx = dopf.minus_ss(datax, nowx)
				except Exception as e:
					print(e)
			for el in nowx:
				textxx += str(el[1]) + " (" + str(el[2]) + ") " + str(el[0]) + "\n"
			bot.edit_message_text(chat_id=cid, message_id=mid, text=textxx,
								  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in warehouse_consumption: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("cooc"))
def callback_cooc(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data.split('#')[0][4:])
			time = call.data.split('#')[1]
			db_cmd.update_order(order_id, 'time', time)
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if data_order[4] in [12, 33]:
				chat_order = config["telegram"]["сourier_channel"]
			elif data_order[4] in [22, 38]:
				chat_order = config["telegram"]["pickup_channel"]
			db_cmd.update_order(order_id, 'status_order', 2)
			text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
			bot.edit_message_caption(chat_id=chat_order,
									 message_id=data_order[1],
									 caption=text,
									 parse_mode=None,
									 reply_markup=markup.recourier_order(order_id))
			text2 = dopf.get_text_order_for_courier(db_cmd.get_order_by_order_id(order_id))
			bot.edit_message_caption(chat_id=cid,
									 message_id=mid,
									 caption=text2,
									 parse_mode=None,
									 reply_markup=markup.active_order_cr_kb(order_id))
	except Exception as e:
		logging.error(f'Error in cooc: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("mxm"))
def callback_mxm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [6] and data[3] == 1:
			cur_id = int(call.data.split('#')[1])
			bank = db_cmd.get_user_bank(cur_id)[1]
			if float(bank) > 0 and db_cmd.get_user_data(cur_id)[6] == 8:
				bot.answer_callback_query(
					callback_query_id=call.id, text=text_cnf["nogetmoney_cur"])
			else:
				money = ast.literal_eval(db_cmd.get_user_data(cur_id)[5])["product"][0][0]
				need_comeback = round(float(money) - float(bank), 2)
				datax = ast.literal_eval(data[4])
				datax["cur"] = cur_id
				db_cmd.update_user(uid, 'state', 71)
				db_cmd.update_user(uid, 'data', str(datax))
				if db_cmd.get_user_data(cur_id)[6] == 8:
					text2 = text_cnf["comeback_money_text2"].format(
						db_cmd.get_user_data(cur_id)[1], need_comeback)
				else:
					text2 = text_cnf["comeback_money_text2"].format(
						db_cmd.get_user_data(cur_id)[1], round(float(money), 2))
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text2,
									  parse_mode=None,
									  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in mxm: {e}')


@bot.callback_query_handler(func=lambda call: call.data == "workon_with_cashier")
def callback_workon_with_cashier(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [15] and data[3] == 1:
			cashx = db_cmd.get_user_data_by_role(6)[0]
			money = ast.literal_eval(cashx[4])["money"]
			db_cmd.update_user(uid, 'state', 72)
			text2 = text_cnf["comeback_money_text2"].format(
				cashx[1], money)
			bot.edit_message_text(chat_id=cid,
								  message_id=mid,
								  text=text2,
								  parse_mode=None,
								  reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in workon_with_cashier: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("csoc"))
def callback_csoc(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_w_id = int(call.data.split('#')[0][4:])
			config = dopf.readJs()
			order_w = db_cmd.get_order_warehouse_by_id(order_w_id)
			db_cmd.update_order_w(order_w[0], 'status_order', 3)
			text = dopf.get_text_by_warehouse_order_next(
				db_cmd.get_order_warehouse_by_id(order_w_id))
			text2 = dopf.get_text_by_warehouse_order_next2(
				db_cmd.get_order_warehouse_by_id(order_w_id))
			bot.edit_message_text(chat_id=cid,
								  message_id=mid,
								  text=text,
								  parse_mode=None,
								  reply_markup=None)
			bot.edit_message_text(chat_id=config["telegram"]["warehouse_channel"],
								  message_id=order_w[1],
								  text=text2,
								  parse_mode=None,
								  reply_markup=None)

	except Exception as e:
		logging.error(f'Error in csoc: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("order_sw_confirm"))
def callback_order_sw_confirm(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [10] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[16:])
			try:
				config = dopf.readJs()
				order_w = db_cmd.get_order_warehouse_by_id(order_id)
				if order_w[3] == 2:
					return
				db_cmd.update_order_w(order_w[0], 'status_order', 2)
				order_data = ast.literal_eval(order_w[4])
				order_id_dlv = order_data["order_id"]
				datadlv = db_cmd.get_order_by_order_id(order_id_dlv)
				datadlvxx = ast.literal_eval(datadlv[5])
				for el in datadlvxx["product"]:
					if el[1] == "שקל":
						order_data["correct_product"].append(el)
				datadlvxx["correct_product"] = order_data["correct_product"]
				db_cmd.update_order(order_id_dlv, 'data', str(datadlvxx))
				dopf.take_warehouse(order_w)
				text = dopf.get_text_by_warehouse_order_next2(
					db_cmd.get_order_warehouse_by_id(order_id))
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text,
									  parse_mode=None,
									  reply_markup=None)
				bot.edit_message_text(chat_id=config["telegram"]["warehouse_channel"],
									  message_id=order_w[1],
									  text=text,
									  parse_mode=None,
									  reply_markup=None)
				msg = bot.send_message(
					order_w[2], text=text_cnf["new_order_courier_msg"], parse_mode=None)
				db_cmd.add_to_dlt_list(order_w[2], msg.message_id)
			except:
				config = dopf.readJs()
				order_w = db_cmd.get_order_warehouse_by_id(order_id)
				dataxxf = ast.literal_eval(order_w[4])['correct_product']
				dopf.take_warehouse(order_w)
				db_cmd.update_order_w(order_w[0], 'status_order', 2)
				text = dopf.get_text_by_warehouse_order_next2(
					db_cmd.get_order_warehouse_by_id(order_id))
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text,
									  parse_mode=None,
									  reply_markup=None)
				bot.edit_message_text(chat_id=config["telegram"]["warehouse_channel"],
									  message_id=order_w[1],
									  text=text,
									  parse_mode=None,
									  reply_markup=None)
				msg = bot.send_message(
					order_w[2], text=text_cnf["new_order_courier_msg"], parse_mode=None)
				db_cmd.add_to_dlt_list(order_w[2], msg.message_id)
	except Exception as e:
		logging.error(f'Error in order_sw_confirm: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("adjust_delivery"))
def callback_adjust_delivery(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [10] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[15:])
			datax = {"active": order_id}
			db_cmd.update_user(uid, 'data', str(datax))
			db_cmd.update_user(uid, 'state', 3)
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=None)
			msg = bot.send_message(
				cid, text=text_cnf["text_corect_delivery_storage1"], parse_mode=None, reply_markup=markup.main_sm())
			db_cmd.add_to_dlt_list(cid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in adjust_delivery: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("takeprcur"))
def callback_takeprcur(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [10] and data[3] == 1 and data[2] == 0:
			order_id = int(call.data[9:])
			datax = {"active": order_id}
			db_cmd.update_user(uid, 'data', str(datax))
			db_cmd.update_user(uid, 'state', 13)
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=None)
			msg = bot.send_message(
				cid, text=text_cnf["list_product_and_price"], parse_mode=None, reply_markup=markup.main_sm())
			db_cmd.add_to_dlt_list(cid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in takeprcur: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("client_cancel"))
def callback_client_cancel(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[13:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if data_order[4] in [12, 33]:
				chat_order = config["telegram"]["сourier_channel"]
				type = 1
			elif data_order[4] in [22, 38]:
				chat_order = config["telegram"]["pickup_channel"]
				type = 2
			data_orderx = ast.literal_eval(data_order[5])
			grm = 0
			for product in data_orderx["product"]:
				if product[1] != "שקל":
					grm += product[0]
			try:
				if grm <= 60:
					data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[2]
				else:
					data_orderx["courier"] = db_cmd.get_data_city(data_orderx["city"])[3]
			except:
				data_orderx["courier"] = 0
			db_cmd.update_order(order_id, 'data', str(data_orderx))
			db_cmd.update_order(order_id, 'status_order', 5)
			db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
			text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
			bot.edit_message_caption(chat_id=chat_order,
									 message_id=data_order[1],
									 caption=text,
									 parse_mode=None,
									 reply_markup=markup.comment_to_cancel(order_id))
			if type == 2:
				bot.edit_message_caption(chat_id=cid,
										 message_id=mid,
										 caption=text_cnf["delivery_cancel_noc"],
										 parse_mode=None,
										 reply_markup=None)

			else:
				bot.edit_message_caption(chat_id=cid,
										 message_id=mid,
										 caption=text_cnf["delivery_cancel_nocx"].format(
											 data_orderx["courier"]),
										 parse_mode=None,
										 reply_markup=None)
			if type == 1:
				top_curs = db_cmd.get_user_data_by_role(12)
				url_order = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
				for fxx in top_curs:
					top_courier_id = fxx[0]
					try:
						bot.send_message(chat_id=top_courier_id,
										text=text_cnf["delivery_cancel_noc2"].format(
											username, url_order),
										parse_mode=None,
										reply_markup=markup.main_menu())
					except:
						pass
			else:
				top_curs = db_cmd.get_user_data_by_role(17)
				url_order = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
				for fxx in top_curs:
					top_courier_id = fxx[0]
					try:
						bot.send_message(chat_id=top_courier_id,
										text=text_cnf["delivery_cancel_noc2"].format(
											username, url_order),
										parse_mode=None,
										reply_markup=markup.main_menu())
					except:
						pass
	except Exception as e:
		logging.error(f'Error in client_cancel: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("xlient_cancel"))
def callback_xlient_cancel(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[13:])
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=markup.active_order_cr_kb2(order_id))
	except Exception as e:
		logging.error(f'Error in xlient_cancel: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("xaoc"))
def callback_xaoc(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[4:])
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=markup.active_order_cr_kb3(order_id))
	except Exception as e:
		logging.error(f'Error in xaoc: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("xar_crash"))
def callback_xaoc(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[9:])
			bot.edit_message_reply_markup(chat_id=cid,
										  message_id=mid,
										  reply_markup=markup.active_order_cr_kb4(order_id))
	except Exception as e:
		logging.error(f'Error in xaoc: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("kurwin"))
def callback_kurwin(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8] and data[3] == 1:
			order_id = int(call.data[6:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			bot.answer_callback_query(
				callback_query_id=call.id, text=text_cnf["kurwing"])
			bot.send_message(chat_id=data_order[2],
							 text=text_cnf["kurwinx"].format(order_id),
							 parse_mode=None,
							 reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in kurwin: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("caoc"))
def callback_caoc(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [8, 9] and data[3] == 1:
			order_id = int(call.data[4:])
			config = dopf.readJs()
			data_order = db_cmd.get_order_by_order_id(order_id)
			if data_order[4] in [12, 33]:
				chat_order = config["telegram"]["сourier_channel"]
			elif data_order[4] in [22, 38]:
				chat_order = config["telegram"]["pickup_channel"]
			db_cmd.update_order(order_id, 'status_order', 0)
			text = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
			bot.edit_message_caption(chat_id=chat_order,
									 message_id=data_order[1],
									 caption=text,
									 parse_mode=None,
									 reply_markup=markup.select_courier_or_pickup(data_order[4], order_id))
			text2 = dopf.get_text_order_for_courier(db_cmd.get_order_by_order_id(order_id))
			bot.edit_message_caption(chat_id=cid,
									 message_id=mid,
									 caption=text_cnf["delivery_cancel_no"],
									 parse_mode=None,
									 reply_markup=None)
			if data_order[4] in [12, 33]:
				top_curs = db_cmd.get_user_data_by_role(12)
				url_order = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
				for fxx in top_curs:
					top_courier_id = fxx[0]
					try:
						bot.send_message(chat_id=top_courier_id,
										text=text_cnf["delivery_cancel_no_need_info"].format(
											username, url_order),
										parse_mode=None,
										reply_markup=markup.main_menu())
					except:
						pass
			else:
				top_curs = db_cmd.get_user_data_by_role(17)
				url_order = f'https://t.me/c/{str(chat_order)[4:]}/{data_order[1]}'
				for fxx in top_curs:
					top_courier_id = fxx[0]
					try:
						bot.send_message(chat_id=top_courier_id,
										text=text_cnf["delivery_cancel_no_need_info"].format(
											username, url_order),
										parse_mode=None,
										reply_markup=markup.main_menu())
					except:
						pass
	except Exception as e:
		logging.error(f'Error in caoc: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("dlv"))
def callback_dlv(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [12, 17]:
			courier_id = int(call.data[3:])
			config = dopf.readJs()
			data_courier = db_cmd.get_user_data(courier_id)
			db_cmd.set_courier_or_pickup_order(mid, courier_id, data_courier[6])
			msg = bot.send_message(
				courier_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
			if data_courier[6] == 8:
				chat_order = config["telegram"]["сourier_channel"]
			elif data_courier[6] == 9:
				chat_order = config["telegram"]["pickup_channel"]
			order = db_cmd.get_order_by_message_id(mid, data_courier[6])
			db_cmd.update_order(order[0], "status_order", 1)
			if data_courier[6] == 9:
				db_cmd.update_order(order[0], "status_order", 2)
			text = dopf.get_text_order_next_step(
				db_cmd.get_order_by_message_id(mid, data_courier[6]))
			bot.edit_message_caption(chat_id=chat_order,
									 message_id=mid,
									 caption=text,
									 parse_mode=None,
									 reply_markup=markup.recourier_order(db_cmd.get_order_by_message_id(mid, data_courier[6])[0]))
			db_cmd.add_to_dlt_list(courier_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in dlv: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("strg"))
def callback_strg(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] in [5, 12]:
			storage_worker_id = int(call.data[4:])
			config = dopf.readJs()
			order_w = db_cmd.get_order_warehouse_by_mid(mid)
			db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
			db_cmd.update_order_w(order_w[0], 'status_order', 1)
			dataxx = ast.literal_eval(order_w[4])
			correct_product = []
			check_k = 0
			for el in dataxx["product"]:
				if el[1] != "שקל":
					name_id = db_cmd.get_product_by_name(el[1])[0]
					list_ref = db_cmd.get_product_refill_active(name_id)
					ffx = 0
					for ref in list_ref:
						if float(ref[3]) >= float(el[0]) and float(ref[5]) + float(ref[6]) == float(db_cmd.get_product_by_name(el[1])[2]):
							price = str(float(ref[5]) + float(ref[6]))
							correct_product.append([el[0], el[1], price])
							ffx = 1
							break
					if ffx == 0:
						check_k += 1
			if check_k > 0:
				db_cmd.update_order_w(order_w[0], 'status_order', 0)
				bot.answer_callback_query(
					callback_query_id=call.id, text=text_cnf["no_products_by_order_warhous"])
			else:
				dataxx["correct_product"] = correct_product
				db_cmd.update_order_w(order_w[0], 'data', str(dataxx))
				order_w = db_cmd.get_order_warehouse_by_mid(mid)
				text = dopf.get_text_by_warehouse_order_next(order_w)
				msg = bot.send_message(
					storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
				bot.edit_message_text(chat_id=cid,
									  message_id=mid,
									  text=text,
									  parse_mode=None,
									  reply_markup=markup.menu_cnlwhx())
				db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in strg: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith("rtrn"))
def callback_rtrn(call):
	try:
		cid = call.message.chat.id
		uid = call.from_user.id
		mid = call.message.message_id
		username = call.from_user.username
		text_cnf = dopf.readJs("text.json")
		data = db_cmd.get_user_data(uid)
		if data[6] == 5 or data[6] == 12:
			storage_worker_id = int(call.data[4:])
			config = dopf.readJs()
			order_w = db_cmd.get_order_warehouse_by_mid(mid)
			db_cmd.update_order_w(order_w[0], 'storage_id', storage_worker_id)
			db_cmd.update_order_w(order_w[0], 'status_order', 5)
			order_w = db_cmd.get_order_warehouse_by_mid(mid)
			text = dopf.get_text_by_warehouse_order2(order_w)
			msg = bot.send_message(
				storage_worker_id, text=text_cnf["new_order_courier_msg"], parse_mode=None)
			bot.edit_message_text(chat_id=cid,
								  message_id=mid,
								  text=text,
								  parse_mode=None,
								  reply_markup=markup.menu_cnlwhx())
			db_cmd.add_to_dlt_list(storage_worker_id, msg.message_id)
	except Exception as e:
		logging.error(f'Error in rtrn: {e}')


@bot.message_handler(content_types=['video'])
def handler_video(message):
	print(message)


@bot.message_handler(content_types=['photo'])
def handler_photo(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		username = message.from_user.username
		image_id = message.photo[len(message.photo) - 1].file_id
		text_cnf = dopf.readJs("text.json")
		caption = message.caption
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] in [10]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = {"new_order": {"photo": image_id}}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order"],
								 parse_mode=None,
								 reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [20]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = {"new_order": {"photo": image_id}}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order_pu"],
								 parse_mode=None,
								 reply_markup=markup.back_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [15]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [25]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order_pu"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [31]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [36]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order_pu"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [41]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [46]:
				db_cmd.update_user(uid, 'state', data[2] + 1)
				mass = ast.literal_eval(data[4])
				mass["new_order"] = {"photo": image_id}
				db_cmd.update_user(uid, 'data', str(mass))
				bot.send_message(cid,
								 text=text_cnf["sm_text_order_pu"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[2] == 6:
				dataxx = ast.literal_eval(data[4])
				order_id = dataxx["sndmsg"]
				config = dopf.readJs()
				data_order = db_cmd.get_order_by_order_id(order_id)
				manager_id = data_order[2]
				db_cmd.update_user(uid, 'state', 0)
				bot.send_photo(chat_id=manager_id,
							   photo=image_id,
							   caption=text_cnf["text_for_mng_by_mk"].format(
								   order_id, message.caption),
							   parse_mode=None,
							   reply_markup=markup.main_menu())
				bot.send_message(chat_id=uid,
								 text=text_cnf["msg_confirm"],
								 parse_mode=None,
								 reply_markup=markup.main_menu())
			elif data[6] in [12, 5] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_photo(chat_id=el[0], photo=image_id, caption=caption)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_photo(chat_id=el[0], photo=image_id, caption=caption)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [12, 5] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_photo(chat_id=el[0], photo=image_id, caption=caption)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_photo(chat_id=el[0], photo=image_id, caption=caption)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
	except Exception as e:
		logging.error(f'Error in photo: {e}')


@bot.message_handler(content_types=['voice'])
def handler_voice(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		username = message.from_user.username
		voice_id = message.voice.file_id
		text_cnf = dopf.readJs("text.json")
		if uid == cid:
			db_cmd.check_user_id(cid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] in [12, 5] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_voice(chat_id=el[0], photo=voice_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [12, 5] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_voice(chat_id=el[0], photo=voice_id)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_voice(chat_id=el[0], photo=voice_id)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [17] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_voice(chat_id=el[0], photo=voice_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
					
	except Exception as e:
		logging.error(f'Error in voice: {e}')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		text = message.text
		username = message.from_user.username
		text_cnf = dopf.readJs("text.json")
		if uid == cid and text.isdigit() and len(text) == 4:
			db_cmd.check_user_id(uid, username)
			data = db_cmd.get_user_data(uid)
			if data[3] == 1 and not(data[6] in [12, 5, 17]) and not(data[2] in [144, 44, 311, 534]):
				if db_cmd.check_activate_code(uid, text):
					if data[6] == 4:
						pass
					elif data[6] == 6:
						db_cmd.update_user(uid, 'state', 0)
						money = ast.literal_eval(data[4])['money']
						text = text_cnf["cashier_menu"].format(money)
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_cashier())
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 15:
						db_cmd.update_user(uid, 'state', 0)
						money = ast.literal_eval(data[4])['money']
						text = text_cnf["accountant_menu"].format(money)
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_accountant())
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 8:
						db_cmd.update_user(uid, 'state', 0)
						if db_cmd.check_new_order_courier(uid):
							text = f'{text_cnf["menu_courier"]}.\n{text_cnf["have_new_order_courier"]}'
						else:
							text = text_cnf["menu_courier"]
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_courier(uid))
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 9:
						db_cmd.update_user(uid, 'state', 0)
						if db_cmd.check_new_order_courier(uid):
							text = f'{text_cnf["menu_courier"]}.\n{text_cnf["have_new_order_courier"]}'
						else:
							text = text_cnf["menu_courier"]
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_courier(uid))
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 10:
						db_cmd.update_user(uid, 'state', 0)
						msg_del = bot.send_message(cid,
												   text=text_cnf["menu_storage_worker"],
												   parse_mode=None,
												   reply_markup=markup.menu_storage(uid))
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 14:
						bank = db_cmd.get_user_bank(uid)[1]
						bank_storage = db_cmd.get_user_bank(0)[1]
						bot.send_message(cid,
										 text=text_cnf["boss_text"].format(bank, bank_storage),
										 parse_mode=None,
										 reply_markup=None)
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 144:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] > 2:
							bot.send_message(chat_id=uid,
											 text=text_cnf["wait_comeback_order"],
											 parse_mode=None,
											 reply_markup=None)
							dopf.return_order(text)
							order_id = text
							config = dopf.readJs()
							data_order = db_cmd.get_order_by_order_id(order_id)
							if data_order[4] in [12, 33]:
								chat_order = config["telegram"]["сourier_channel"]
							elif data_order[4] in [22, 38]:
								chat_order = config["telegram"]["pickup_channel"]
							db_cmd.update_order(order_id, 'status_order', 2)
							text = dopf.get_text_order_next_step(
								db_cmd.get_order_by_order_id(order_id))
							bot.edit_message_caption(chat_id=chat_order,
													 message_id=data_order[1],
													 caption=text,
													 parse_mode=None,
													 reply_markup=markup.recourier_order(order_id))
							bot.send_message(chat_id=uid,
											 text=text_cnf["comeback_order_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_no_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 534:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] != 3:
							datax = ast.order_data.literal_eval([5])
							datax["money"] = text
							db_cmd.update_order(int(text),"data", str(datax))
							bot.send_message(chat_id=uid,
												text=text_cnf["order_confirmy"],
												parse_mode=None,
												reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_confirmy"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 311:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] == 2:
							close(order_data[7],text, uid)
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_confirmx"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_confirmx"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [5] and data[3] == 1 and data[2] == 44:
				if text.isdigit():
					orderw_data = db_cmd.get_order_warehouse_by_id(text)
					if orderw_data:
						if orderw_data[3] in [2, 3, 6]:
							bot.send_message(chat_id=uid,
											 text=text_cnf["wait_comeback_order"],
											 parse_mode=None,
											 reply_markup=None)
							order_w_id = text
							dopf.return_order_w(order_w_id, bot)
							bot.send_message(chat_id=uid,
											 text=text_cnf["comeback_order_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_no_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[3] in [0, 3, 4, 5]:
				if db_cmd.check_noactivate_code(uid, text):
					data = db_cmd.get_user_data(uid)
					db_cmd.update_user(uid, 'state', 0)
					if data[6] == 1:
						pass
					elif data[6] == 2:
						pass
					elif data[6] == 3:
						pass
					elif data[6] == 4:
						pass
					elif data[6] == 5:
						db_cmd.add_user_bank(uid)
						bot.send_message(cid,
										 text=text_cnf["menu_sales_manager"],
										 parse_mode=None,
										 reply_markup=None)
					elif data[6] == 6:
						db_cmd.add_user_bank(uid)
						db_cmd.update_user(uid, 'state', 0)
						db_cmd.update_user(uid, 'data', str({'money': 0}))
						text = text_cnf["cashier_menu"].format(0)
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_cashier())
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 15:
						db_cmd.add_user_bank(uid)
						db_cmd.update_user(uid, 'state', 0)
						db_cmd.update_user(uid, 'data', str({'money': 0}))
						text = text_cnf["accountant_menu"].format(0)
						msg_del = bot.send_message(cid,
												   text=text,
												   parse_mode=None,
												   reply_markup=markup.menu_accountant())
						for i in range(msg_del.message_id - 2, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 7:
						db_cmd.add_user_bank(uid)
						bot.send_message(cid,
										 text=text_cnf["menu_sales_manager"],
										 parse_mode=None,
										 reply_markup=markup.menu_sales_manager(uid))
					elif data[6] == 8:
						db_cmd.add_user_bank(uid)
						datax = {'product': [[0, 'שקל']]}
						db_cmd.update_user(uid, 'on_hands', str(datax))
						msg_del = bot.send_message(cid,
												   text=text_cnf["menu_courier"],
												   parse_mode=None,
												   reply_markup=markup.menu_courier(uid))
						for i in range(msg_del.message_id - 1, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 17:
						db_cmd.add_user_bank(uid)
						msg_del = bot.send_message(cid,
												   text=text_cnf["menu_top_mng"],
												   parse_mode=None,
												   reply_markup=markup.menu_top_mng())
						for i in range(msg_del.message_id - 1, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 9:
						db_cmd.add_user_bank(uid)
						datax = {'product': [[0, 'שקל']]}
						db_cmd.update_user(uid, 'on_hands', str(datax))
						msg_del = bot.send_message(cid,
												   text=text_cnf["menu_courier"],
												   parse_mode=None,
												   reply_markup=markup.menu_courier(uid))
						for i in range(msg_del.message_id - 1, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 10:
						db_cmd.add_user_bank(uid)
						msg_del = bot.send_message(cid,
												   text=text_cnf["menu_storage_worker"],
												   parse_mode=None,
												   reply_markup=markup.menu_storage(uid))
						for i in range(msg_del.message_id - 1, msg_del.message_id + 1):
							db_cmd.add_to_dlt_list(uid, i)
					elif data[6] == 11:
						pass
					elif data[6] == 12:
						db_cmd.add_user_bank(uid)
						bot.send_message(cid,
										 text=text_cnf["menu_manager_courier_and_pickup"],
										 parse_mode=None,
										 reply_markup=markup.menu_manager_courier_and_pickup())
					elif data[6] == 14:
						db_cmd.add_user_bank(uid)
						bank = db_cmd.get_user_bank(uid)[1]
						bank_storage = db_cmd.get_user_bank(0)[1]
						bot.send_message(cid,
										 text=text_cnf["boss_text"].format(bank, bank_storage),
										 parse_mode=None,
										 reply_markup=None)
				else:
					if data[3] == 0:
						db_cmd.update_user(uid, 'status', 3)
					else:
						db_cmd.update_user(uid, 'status', data[3] + 1)
		elif uid == cid:
			db_cmd.check_user_id(uid, username)
			data = db_cmd.get_user_data(uid)
			if data[6] == 7 and data[3] == 1 and data[2] in [11, 21]:
				if data[2] == 11:
					check, text, data_order = dopf.check_data_order(text)
				elif data[2] == 21:
					check, text, data_order = dopf.check_data_order2(text)
				if check == False:
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.cancel_order_sm())
				else:
					db_cmd.update_user(uid, 'state', data[2] + 1)
					new_data_order = ast.literal_eval(data[4])
					new_data_order["new_order"]["data"] = data_order
					db_cmd.update_user(uid, 'data', str(new_data_order))
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.confirm_order_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [16, 26]:
				if data[2] == 16:
					check, text, data_order = dopf.check_data_order(text)
				elif data[2] == 26:
					check, text, data_order = dopf.check_data_order2(text)
				if check == False:
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.cancel_order_sm())
				else:
					db_cmd.update_user(uid, 'state', data[2] + 1)
					new_data_order = ast.literal_eval(data[4])
					new_data_order["new_order"]["data"] = data_order
					db_cmd.update_user(uid, 'data', str(new_data_order))
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.confirm_order_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [42, 47]:
				if data[2] == 42:
					check, text, data_order = dopf.check_data_order3(text)
				elif data[2] == 47:
					check, text, data_order = dopf.check_data_order4(text)
				if check == False:
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.cancel_order_sm())
				else:
					db_cmd.update_user(uid, 'state', data[2] + 1)
					new_data_order = ast.literal_eval(data[4])
					new_data_order["new_order"]["data"] = data_order
					db_cmd.update_user(uid, 'data', str(new_data_order))
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.confirm_order_sm())
			elif data[6] == 7 and data[3] == 1 and data[2] in [32, 37]:
				if data[2] == 32:
					check, text, data_order = dopf.check_data_order3(text)
				elif data[2] == 37:
					check, text, data_order = dopf.check_data_order4(text)
				if check == False:
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.cancel_order_sm())
				else:
					db_cmd.update_user(uid, 'state', data[2] + 1)
					new_data_order = ast.literal_eval(data[4])
					new_data_order["new_order"]["data"] = data_order
					db_cmd.update_user(uid, 'data', str(new_data_order))
					bot.send_message(cid,
									 text=text,
									 parse_mode=None,
									 reply_markup=markup.confirm_order_sm())
			elif data[6] in [12, 17] and data[2] == 5:
				dataxx = ast.literal_eval(data[4])
				order_id = dataxx["cnlorder"]
				config = dopf.readJs()
				data_order = db_cmd.get_order_by_order_id(order_id)
				if data_order[4] in [12, 33]:
					chat_order = config["telegram"]["сourier_channel"]
					type = 12
				elif data_order[4] in [22, 38]:
					type = 22
					chat_order = config["telegram"]["pickup_channel"]
				if data_order[3] != 5:
					db_cmd.update_order(order_id, "status_order", 4)
					db_cmd.update_order(order_id, 'date_close', str(datetime.datetime.now()))
				datax = ast.literal_eval(data_order[5])
				datax["cnlorder"] = text
				datax["courier"] = 0
				db_cmd.update_order(order_id, "data", str(datax))
				text2 = dopf.get_text_order_next_step(db_cmd.get_order_by_order_id(order_id))
				bot.edit_message_caption(chat_id=chat_order,
										 message_id=data_order[1],
										 caption=text2,
										 parse_mode=None,
										 reply_markup=markup.change_pay_cur(type, datax["courier"], order_id))
				bot.send_message(
					chat_id=data_order[2], text=text_cnf["cncl_order_info"].format(order_id, text))
				if data_order[7]:
					text3 = dopf.get_text_order_next_step33(db_cmd.get_order_by_order_id(order_id))
					msgxx = bot.send_message(
						chat_id=data_order[7], text=text3)
					db_cmd.add_to_dlt_list(data_order[7], msgxx.message_id)
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=cid,
								 text=text_cnf["delivery_cancel_mk"].format(order_id),
								 parse_mode=None,
								 reply_markup=markup.main_menu())
			elif data[6] == 12 and data[2] == 6:
				dataxx = ast.literal_eval(data[4])
				order_id = dataxx["sndmsg"]
				config = dopf.readJs()
				data_order = db_cmd.get_order_by_order_id(order_id)
				manager_id = data_order[2]
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=manager_id,
								 text=text_cnf["text_for_mng_by_mk"].format(order_id, text),
								 parse_mode=None,
								 reply_markup=markup.main_menu())
				bot.send_message(chat_id=uid,
								 text=text_cnf["msg_confirm"],
								 parse_mode=None,
								 reply_markup=markup.main_menu())
			elif data[6] == 12 and data[2] == 77:
				dataxx = ast.literal_eval(data[4])
				order_id = dataxx["sndmsg"]
				config = dopf.readJs()
				data_order = db_cmd.get_order_by_order_id(order_id)
				manager_id = data_order[2]
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=manager_id,
								 text=text_cnf["text_for_mng_by_mk"].format(order_id, text),
								 parse_mode=None,
								 reply_markup=markup.main_menu())
				bot.send_message(chat_id=uid,
								 text=text_cnf["msg_confirm"],
								 parse_mode=None,
								 reply_markup=markup.main_menu())
			elif data[6] == 10 and data[3] == 1 and data[2] == 3:
				order_id_w = ast.literal_eval(data[4])["active"]
				data_order_w = db_cmd.get_order_warehouse_by_id(order_id_w)
				datax, text_next, check = dopf.check_order_for_sw(data_order_w, text)
				if check == True:
					dataxx = ast.literal_eval(data[4])
					dataxx["correct_order"] = datax
					db_cmd.update_user(uid, 'data', str(dataxx))
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["recognition_successful"].format(
											   text_next),
										   parse_mode=None,
										   reply_markup=markup.confirm_sw())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
				else:
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["text_error_sw_adjust"],
										   parse_mode=None,
										   reply_markup=markup.main_sm())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 144:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] > 2:
							bot.send_message(chat_id=uid,
											 text=text_cnf["wait_comeback_order"],
											 parse_mode=None,
											 reply_markup=None)
							dopf.return_order(text)
							order_id = text
							config = dopf.readJs()
							data_order = db_cmd.get_order_by_order_id(order_id)
							if data_order[4] in [12, 33]:
								chat_order = config["telegram"]["сourier_channel"]
							elif data_order[4] in [22, 38]:
								chat_order = config["telegram"]["pickup_channel"]
							db_cmd.update_order(order_id, 'status_order', 2)
							text = dopf.get_text_order_next_step(
								db_cmd.get_order_by_order_id(order_id))
							bot.edit_message_caption(chat_id=chat_order,
													 message_id=data_order[1],
													 caption=text,
													 parse_mode=None,
													 reply_markup=markup.recourier_order(order_id))
							bot.send_message(chat_id=uid,
											 text=text_cnf["comeback_order_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_no_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			
			elif data[6] in [5] and data[3] == 1 and data[2] == 44:
				if text.isdigit():
					orderw_data = db_cmd.get_order_warehouse_by_id(text)
					if orderw_data:
						if orderw_data[3] in [2, 3, 6]:
							bot.send_message(chat_id=uid,
											 text=text_cnf["wait_comeback_order"],
											 parse_mode=None,
											 reply_markup=None)
							order_w_id = text
							dopf.return_order_w(order_w_id, bot)
							bot.send_message(chat_id=uid,
											 text=text_cnf["comeback_order_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_no_confirm"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 311:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] == 2:
							close(order_data[7],text, uid)
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_confirmx"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [12, 17] and data[3] == 1 and data[2] == 534:
				if text.isdigit():
					order_data = db_cmd.get_order_by_order_id(text)
					if order_data:
						if order_data[3] != 3:
							datax = ast.order_data.literal_eval([5])
							datax["money"] = text
							db_cmd.update_order(int(text),"data", str(datax))
							bot.send_message(chat_id=uid,
												text=text_cnf["order_confirmy"],
												parse_mode=None,
												reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["order_confirmy"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["no_order_by_id"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["no_order_by_id"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] == 10 and data[3] == 1 and data[2] == 13:
				order_id_w = ast.literal_eval(data[4])["active"]
				data_order_w = db_cmd.get_order_warehouse_by_id(order_id_w)
				datax, text_next, check = dopf.check_order_for_sw2(data_order_w, text)
				if check == True:
					dataxx = ast.literal_eval(data[4])
					dataxx["true_order"] = datax
					db_cmd.update_user(uid, 'data', str(dataxx))
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["recognition_successful2"].format(
											   text_next),
										   parse_mode=None,
										   reply_markup=markup.confirm_sw())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
				else:
					msg = bot.send_message(chat_id=uid,
										   text=text_next,
										   parse_mode=None,
										   reply_markup=markup.main_sm())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [8, 9] and data[3] == 1 and data[2] == 41:
				check, datax, textx = dopf.get_pr_cur_asm(text, data[0])
				if check:
					x = {"productx": datax}
					db_cmd.update_user(uid, 'data', str(x))
					msg = bot.send_message(chat_id=uid,
										   text=textx,
										   parse_mode=None,
										   reply_markup=markup.confirm_s_request())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
				else:
					msg = bot.send_message(chat_id=uid,
										   text=textx,
										   parse_mode=None,
										   reply_markup=markup.main_sm())
					db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [12, 5] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_message(chat_id=el[0], text=text)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 91:
				data = db_cmd.get_users_for_delivery(7)
				for el in data:
					try:
						bot.send_message(chat_id=el[0], text=text)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [5] and data[3] == 1 and data[2] == 303:
				datax = text.split(',')
				if len(datax) == 3:
					if db_cmd.get_product_by_name(datax[0]):
						if dopf.is_number(datax[1]):
							data_price = datax[2].split("+")
							if len(data_price) == 2 and dopf.is_number(data_price[0]) and dopf.is_number(data_price[1]):
								db_cmd.add_refill(db_cmd.get_product_by_name(datax[0])[
												  0], datax[1], data_price[0], data_price[1])
								db_cmd.update_user(uid, 'state', 0)
								bot.send_message(chat_id=uid,
												 text=text_cnf["text_refill_true"],
												 parse_mode=None,
												 reply_markup=markup.main_sm())
							else:
								bot.send_message(chat_id=uid,
												 text=text_cnf["text_refill_error4"],
												 parse_mode=None,
												 reply_markup=markup.main_sm())
						else:
							bot.send_message(chat_id=uid,
											 text=text_cnf["text_refill_error3"],
											 parse_mode=None,
											 reply_markup=markup.main_sm())
					else:
						bot.send_message(chat_id=uid,
										 text=text_cnf["text_refill_error2"],
										 parse_mode=None,
										 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["text_refill_error1"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [5] and data[3] == 1 and data[2] == 313:
				datax = text
				db_cmd.update_user(uid, 'state', 0)
				db_cmd.add_product_new(datax)
				bot.send_message(chat_id=uid,
								 text=text_cnf["add_new_product"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [5] and data[3] == 1 and data[2] == 173:
				element_id = ast.literal_eval(data[4])["element"]
				refill = db_cmd.get_product_refill_by_id(element_id)
				if text[0] in ["-", "+"] and dopf.is_number(text[1:]):
					numx = float(text[1:])
					if text[0] == "-":
						numx = -1 * numx
					now = float(refill[3])
					if now + numx >= 0:
						y = float(refill[3]) + numx
						x = float(refill[2]) + numx
						db_cmd.update_refill(element_id, "number_start", x)
						db_cmd.update_refill(element_id, "number_now", y)
						db_cmd.update_user(uid, 'state', 0)
						name = db_cmd.get_product_by_num(refill[1])[1]
						textx = text_cnf["amount_change_refill"].format(name, float(x), float(y), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
						bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
					else:
						name = db_cmd.get_product_by_num(refill[1])[1]
						textx = text_cnf["amount_change_refill_not_correct"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
						bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
				else:
					name = db_cmd.get_product_by_num(refill[1])[1]
					textx = text_cnf["amount_change_refill_not_correct"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
					bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
			elif data[6] in [5] and data[3] == 1 and data[2] == 174:
				element_id = ast.literal_eval(data[4])["element"]
				refill = db_cmd.get_product_refill_by_id(element_id)
				text_d = text.split("+")
				if len(text_d) == 2 and dopf.is_number(text_d[0]) and dopf.is_number(text_d[1]) and (float(text_d[0]) + float(text_d[1])) == (float(refill[5]) + float(refill[6])):
					db_cmd.update_refill(element_id, "price", text_d[0])
					db_cmd.update_refill(element_id, "added_value", text_d[1])
					db_cmd.update_user(uid, 'state', 0)
					name = db_cmd.get_product_by_num(refill[1])[1]
					textx = text_cnf["price_change_refill"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(text_d[0]), float(text_d[1]), float(text_d[0]) + float(text_d[1]), float(refill[3]))
					bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
				else:
					name = db_cmd.get_product_by_num(refill[1])[1]
					textx = text_cnf["price_change_refill_not_correct"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
					bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
			elif data[6] in [5] and data[3] == 1 and data[2] == 175:
				element_id = ast.literal_eval(data[4])["element"]
				refill = db_cmd.get_product_refill_by_id(element_id)
				if text[0] == "#" and dopf.is_number(text[1:]):
					db_cmd.update_refill(element_id, "number_now", float(refill[3]) - float(text[1:]))
					rez = float(text[1:]) * float(refill[6])
					main = float(text[1:]) * float(refill[5])
					db_cmd.update_bank(1,round(
						float(db_cmd.get_user_bank(1)[1]), 2) - round(main - rez, 2))
					db_cmd.update_bank(1,round(
						float(db_cmd.get_user_bank(1)[1]), 2) + round(main, 2))
					db_cmd.update_user(uid, 'state', 0)
					name = db_cmd.get_product_by_num(refill[1])[1]
					textxy = text_cnf["rubish_confirm"].format(name, float(text[1:]), float(refill[5]), float(refill[6]), (float(refill[5]) - float(refill[6])) * float(text[1:]))
					textx = text_cnf["rubbish_change_refill"].format(name, float(refill[2]), float(refill[3]) - float(text[1:]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]) - float(text[1:]))
					bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
					config = dopf.readJs()
					bot.send_message(chat_id=config["telegram"]["penalties_channel"],text=textxy)
				else:
					name = db_cmd.get_product_by_num(refill[1])[1]
					textx = text_cnf["rubbish_change_refill_not_correct"].format(name, float(refill[2]), float(refill[3]), float(refill[4]), float(refill[5]), float(refill[6]), float(refill[5]) + float(refill[6]), float(refill[3]))
					bot.send_message(chat_id=cid, text=textx, reply_markup=markup.editprice_refill_kb(element_id))
			elif data[6] in [12, 5] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_message(chat_id=el[0], text=text)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
			elif data[6] in [17] and data[3] == 1 and data[2] == 191:
				data = db_cmd.get_users_for_delivery(8)
				for el in data:
					try:
						msg = bot.send_message(chat_id=el[0], text=text)
						db_cmd.add_to_dlt_list(el[0], msg.message_id)
					except:
						pass
				db_cmd.update_user(uid, 'state', 0)
				msg = bot.send_message(chat_id=uid,
								 text=text_cnf["mas_msg_true"],
								 parse_mode=None,
								 reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [12] and data[3] == 1 and data[2] == 211:
				dataf = text.split(" ")
				if dataf[-1].isdigit() and dataf[-2].isdigit and len(dataf) >= 3:
					numdo = int(dataf[-2])
					numposle = int(dataf[-1])
					del dataf[-1]
					del dataf[-1]
					city = ' '.join(dataf)
					if not db_cmd.check_city(city):
						db_cmd.add_city(city, numdo, numposle)
					db_cmd.update_user(uid, 'state', 0)
					bot.send_message(chat_id=uid,
									 text=text_cnf["city_add_now"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
				else:
					bot.send_message(chat_id=uid,
									 text=text_cnf["incorrect_city"],
									 parse_mode=None,
									 reply_markup=markup.main_sm())
			elif data[6] in [6] and data[3] == 1 and data[2] == 71:
				if dopf.is_number(text):
					datax = ast.literal_eval(data[4])
					datax["take"] = round(float(text), 2)
					db_cmd.update_user(uid, 'data', str(datax))
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["take_money_cur"].format(
											   db_cmd.get_user_data(datax["cur"])[1], text),
										   parse_mode=None,
										   reply_markup=markup.confirm_cashir_operation())
				else:
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["nodigit_worker"],
										   parse_mode=None,
										   reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [15] and data[3] == 1 and data[2] == 72:
				if dopf.is_number(text):
					cashx = db_cmd.get_user_data_by_role(6)[0]
					datax = ast.literal_eval(data[4])
					datax["take"] = round(float(text), 2)
					db_cmd.update_user(uid, 'data', str(datax))
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["take_money_cur"].format(
											   cashx[1], text),
										   parse_mode=None,
										   reply_markup=markup.confirm_cashir_operation())
				else:
					msg = bot.send_message(chat_id=uid,
										   text=text_cnf["nodigit_worker"],
										   parse_mode=None,
										   reply_markup=markup.main_sm())
				db_cmd.add_to_dlt_list(uid, msg.message_id)
			elif data[6] in [5] and data[3] == 1 and data[2] == 111:
				if text.isdigit() or (text[0] == "-" and text[1:].isdigit()):
					num = int(text)
					worker_id = ast.literal_eval(data[4])["select"]
					db_cmd.update_bank(902167185, round(
						float(db_cmd.get_user_bank(902167185)[1]), 2) - num / 2)
					db_cmd.add_financial_operation(
						id_order=-1, user_id=902167185, money=-num / 2)
					# top 2 522350229
					db_cmd.update_bank(522350229, round(
						float(db_cmd.get_user_bank(522350229)[1]), 2) - num / 2)
					db_cmd.add_financial_operation(
						id_order=-1, user_id=522350229, money=-num / 2)
					db_cmd.update_bank(worker_id, round(
						float(db_cmd.get_user_bank(worker_id)[1]), 2) + num)
					db_cmd.add_financial_operation(
						id_order=-1, user_id=worker_id, money=num)
					db_cmd.update_user(uid, "state", 0)
					bot.send_message(
						chat_id=uid, text=text_cnf["confirm_pay_worker"], reply_markup=markup.main_sm())
				else:
					bot.send_message(
						chat_id=uid, text=text_cnf["nodigit_worker"], reply_markup=markup.main_sm())
	except Exception as e:
		logging.error(f'Error in all_message_handler: {e}')


"""@bot.channel_post_handler(func=lambda m: True)
def channel_msg(message):
	try:
		print(message)
	except:
		print("error11")"""

logging.info('Workspace-bot RUN!')
if mod == 1:
	bot.polling(none_stop=True)
elif mod == 0:
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			logging.error(f'Error reboot: {e}')
			time.sleep(60)
