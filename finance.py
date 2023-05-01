import json
import dopf
import ast
import time
import db_cmd
import markup
from datetime import datetime
from datetime import timedelta

GOD_LIST = [943897396, 719635830, 932866767, 1000251170,
            381499787, 1318278301, 979349073, 1277296968, 489485939, 1422172936]
# GODLIST den #Johnsnoweed, Mefal_Aerek, TimTam4, pusidon666, DonaldTrump1337, niggabooo, joki43, Roshtov, bototvorec, Baruhdduv

CHIKIPIKIG = [1293237995, 766424933, 958814863, 894934571, 773524265,
              998337831, 1016199704, 996892694, 828310620, 948401846, 493415671, 979982576, 1435675317, 1473014265]
# CHIKIPIKI #glcomp, HaperaH_BegaNi, TeresaaMendoza, Deltakush, BatzBunny, KennyMccormickWeed, ScoobiDooandShagi, TeresaaMendoza, shiriazugi, xJohnnyBravo, ChikiPiki420, sabalemotek, GreenGoblinExpress, TimonWeedPumba

SHAKIRAGROUP = [1264354421, 1334948631, 1006361936, 864165375]
# SHAKIRAGROUP #Goldofweed_420, Dislekt, SHAKIRAB7, funnybunny420

GODCHIKI = [923214158, 1323210200, 1396652821]
# GODCHIKI  #laboutiqueweed, Ogmakakim, bennykadosh

SOLO50 = [814657552, 1362512129,
          805208754, 866596289, 897249365, 1209899043, 1339297729, 1196849771, 1252130570, 902219478, 945389520, 1282013231, 1178117660]
# SOLO50 #Squid_WeeD, Ghost_247, MEDICAPTAIN, CHANELWeeD, Satlanic, acaMma7, bahurgadol, White_Walker14, Simharif788, Jamaica_Weed, barkohva, WW420g, Weedfactory

SOLO40 = [797754997, 1572988315]
# SOLO40 #TravkaPT_Express, OffWhite_WEED

SOLO35 = [1066714037, 1435948710]
# SOLO35 #Johnnyweed5, Kitty_Boutique

MEDICAPTAINGR = [532945079]
# MEDICAPTAINGR #BoutiCannaAdmin

JAMAIKAGR = [845926934]
# JAMAIKAGR #Pneahshaf

MANIAKGR = [918794435]
# MANIAKGR #Honey420PT

WW420GR = []
# WW420GR #

BORKOHVAG = [1178407871]
# BORKOHVAG #  xweedx

RUSASKMEWM = [995098986, 1496622684, 1526187080, 1593673858, 1410702178]
# RUSASKMEWM #svitayameri

RUSASKMELM = [1496622684, 1526187080, 1593673858, 1410702178]
# RUSASKMEWM #bugsbunnyweeed, magicsnowweed, badgirlweeds, docweed11

RUSASKMEMM = [1393367499]
# RUSASKMEMM #smokingsuperman

SHABAEN_VLADELCI = 1181520364
PIFPAF = 563355705

BARKHV = 945389520
SUPERMAN = 1393367499
TOPMNG = 765382321
ASKME = 871500685
BOODU = 941204671
VLADELEC1 = 902167185
VLADELEC2 = 522350229
MEDICAPTAIN = 805208754
JAMAIKA = 902219478
MANIAK_KATAN = 961357327
SHAKIRA = 1006361936
CHIKIPIKI = 948401846
WW420 = 1282013231

while True:
    orders = db_cmd.get_all_confirm_order_no_check2()
    for order in orders:
        d1 = datetime.strptime(order[9], '%Y-%m-%d %H:%M:%S.%f')
        d2 = datetime.now() - timedelta(minutes=10)
        if d2 >= d1:
            if order[3] in [4, 5, 6]:
                try:
                    datax = int(ast.literal_eval(order[5])["courier"])
                    profit = float(datax) * -1
                    if order[2] in GOD_LIST:
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.175), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')

                    elif order[2] in RUSASKMEWM:
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                        db_cmd.update_bank(SUPERMAN, round(
                            float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in RUSASKMELM:
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        db_cmd.update_bank(SUPERMAN, round(
                            float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.175), 2))
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in RUSASKMEMM:
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.125), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.125), 2))
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.125), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.125), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in MEDICAPTAINGR:
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # god_partner 2
                        db_cmd.update_bank(MEDICAPTAIN, round(
                            float(db_cmd.get_user_bank(MEDICAPTAIN)[1]), 2) + round(float(profit * 0.15), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=MEDICAPTAIN, money=round(float(profit * 0.15), 2))
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in JAMAIKAGR:
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # god_partner 2
                        db_cmd.update_bank(JAMAIKA, round(
                            float(db_cmd.get_user_bank(JAMAIKA)[1]), 2) + round(float(profit * 0.15), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=JAMAIKA, money=round(float(profit * 0.15), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in MANIAKGR:
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # god_partner 2
                        db_cmd.update_bank(MANIAK_KATAN, round(
                            float(db_cmd.get_user_bank(MANIAK_KATAN)[1]), 2) + round(float(profit * 0.15), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=MANIAK_KATAN, money=round(float(profit * 0.15), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] == TOPMNG:
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                    elif order[2] in CHIKIPIKIG:
                        # cur
                        db_cmd.update_bank(order[7], round(
                            float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        # CHIKIPIKI
                        db_cmd.update_bank(CHIKIPIKI, round(
                            float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit), 2))
                    elif order[2] in GODCHIKI:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(CHIKIPIKI, round(
                            float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit)*0.35, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit)*0.35, 2))
                        # CHIKIPIKI
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit)*0.35, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit)*0.35, 2))
                        # CHIKIPIKI
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit)*0.1, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit)*0.1, 2))
                        # CHIKIPIKI
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit)*0.2, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit)*0.2, 2))
                    elif order[2] in SHAKIRAGROUP:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(SHAKIRA, round(
                            float(db_cmd.get_user_bank(SHAKIRA)[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=SHAKIRA, money=round(float(profit), 2))
                    elif order[2] in BORKOHVAG:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(BARKHV, round(
                            float(db_cmd.get_user_bank(BARKHV)[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BARKHV, money=round(float(profit), 2))
                    elif order[2] in WW420GR:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(WW420, round(
                            float(db_cmd.get_user_bank(WW420)[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=WW420, money=round(float(profit), 2))
                    elif order[2] == PIFPAF:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.20), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.20), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.40), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.40), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.40), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.40), 2))
                    elif order[2] in SOLO50:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] in SOLO40:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # CHIKIPIKI
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] in SOLO35:
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] == SHABAEN_VLADELCI:
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit)*0.5, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit)*0.5, 2))
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit)*0.5, 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit)*0.5, 2))
                        # cur
                        try:
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(datax), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=1 * round(float(datax), 2), payer_id=order[2])
                        except Exception as e:
                            print(e, 'no_cur')
                except:
                    pass
                db_cmd.update_order(order[0], "time", 1)
            elif order[3] == 3:

                if order[4] in [33, 38]:
                    try:
                        stk = ast.literal_eval(order[5])["stk"]
                    except:
                        stk = 0
                        print(order)
                    if stk == 1:
                        profit, product_price, cur, checkx = dopf.get_profit_exchange(order)
                        if order[2] in GOD_LIST:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.175), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in RUSASKMEWM:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(SUPERMAN, round(
                                float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in RUSASKMELM:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.175), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(SUPERMAN, round(
                                float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in RUSASKMEMM:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.125), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.125), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.125), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.125), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in GODCHIKI:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                            # god_partner CHIKIPIKI
                            db_cmd.update_bank(CHIKIPIKI, round(
                                float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.175), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in MEDICAPTAINGR:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(MEDICAPTAIN, round(
                                float(db_cmd.get_user_bank(MEDICAPTAIN)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MEDICAPTAIN, money=round(float(profit * 0.15), 2))
                        elif order[2] in JAMAIKAGR:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(JAMAIKA, round(
                                float(db_cmd.get_user_bank(JAMAIKA)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=JAMAIKA, money=round(float(profit * 0.15), 2))
                        elif order[2] in MANIAKGR:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(MANIAK_KATAN, round(
                                float(db_cmd.get_user_bank(MANIAK_KATAN)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MANIAK_KATAN, money=round(float(profit * 0.15), 2))
                        elif order[2] == TOPMNG:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in CHIKIPIKIG:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # CHIKIPIKI
                                db_cmd.update_bank(CHIKIPIKI, round(
                                    float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.45), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.45), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.275), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.275), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.275), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.275), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # CHIKIPIKI
                                db_cmd.update_bank(CHIKIPIKI, round(
                                    float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.45) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.45) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.275), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.275), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.275), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.275), 2))
                        elif order[2] == PIFPAF:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # CHIKIPIKI
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.4), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.4), 2))
                        elif order[2] in SHAKIRAGROUP:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(SHAKIRA, round(
                                    float(db_cmd.get_user_bank(SHAKIRA)[1]), 2) + round(float(profit * 0.5), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=SHAKIRA, money=round(float(profit * 0.5), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(SHAKIRA, round(
                                    float(db_cmd.get_user_bank(SHAKIRA)[1]), 2) + round(float(profit * 0.5) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=SHAKIRA, money=round(float(profit * 0.5) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in BORKOHVAG:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(BARKHV, round(
                                    float(db_cmd.get_user_bank(BARKHV)[1]), 2) + round(float(profit * 0.5), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=BARKHV, money=round(float(profit * 0.5), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(BARKHV, round(
                                    float(db_cmd.get_user_bank(BARKHV)[1]), 2) + round(float(profit * 0.5) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=BARKHV, money=round(float(profit * 0.5) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in WW420GR:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(WW420, round(
                                    float(db_cmd.get_user_bank(WW420)[1]), 2) + round(float(profit * 0.35), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=WW420, money=round(float(profit * 0.35), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                db_cmd.update_bank(WW420, round(
                                    float(db_cmd.get_user_bank(WW420)[1]), 2) + round(float(profit * 0.35) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=WW420, money=round(float(profit * 0.35) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                        elif order[2] in SOLO50:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.5), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.5), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.5) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.5) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif order[2] in SOLO40:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.4), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.4), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.3), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.3), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.3), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.3), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # SHAKIRA
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.4) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.4) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.3), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.3), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.3), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.3), 2))
                        elif order[2] in SOLO35:
                            if checkx:
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # mng
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.35), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.35), 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                            else:
                                profit = profit + cur
                                # storage
                                db_cmd.update_bank(
                                    0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=0, money=round(float(product_price), 2))
                                # cur
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                                # mng
                                db_cmd.update_bank(order[2], round(
                                    float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.35) - cur, 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[2], money=round(float(profit * 0.35) - cur, 2))
                                # top 1 VLADELEC1
                                db_cmd.update_bank(VLADELEC1, round(
                                    float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                                # top 2 VLADELEC2
                                db_cmd.update_bank(VLADELEC2, round(
                                    float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                        elif order[2] == SHABAEN_VLADELCI:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.5), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.5), 2))

                        db_cmd.update_order(order[0], "time", 1)
                elif order[4] in [12, 22]:
                    money, profit, product_price, cur = dopf.get_profit(order)
                    city = ast.literal_eval(order[5])['city']
                    k = 0
                    if order[2] in GOD_LIST:
                        if money < 0:
                            money = -1 * money - 1
                            profit += money + 1
                        # storage
                        db_cmd.update_bank(
                            0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=0, money=round(float(product_price), 2))
                        # cur
                        db_cmd.update_bank(order[7], round(
                            float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(BOODU, round(
                            float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=BOODU, money=round(float(profit * 0.175), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                    elif order[2] in RUSASKMEWM:
                        if money < 0:
                            money = -1 * money - 1
                            profit += money + 1
                        # storage
                        db_cmd.update_bank(
                            0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=0, money=round(float(product_price), 2))
                        # cur
                        db_cmd.update_bank(order[7], round(
                            float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(SUPERMAN, round(
                            float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                    elif order[2] in RUSASKMELM:
                        if money < 0:
                            money = -1 * money - 1
                            profit += money + 1
                        # storage
                        db_cmd.update_bank(
                            0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=0, money=round(float(product_price), 2))
                        # cur
                        db_cmd.update_bank(order[7], round(
                            float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.175), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                        # god_partner BOODU
                        db_cmd.update_bank(SUPERMAN, round(
                            float(db_cmd.get_user_bank(SUPERMAN)[1]), 2) + round(float(profit * 0.05), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=SUPERMAN, money=round(float(profit * 0.05), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                    elif order[2] in RUSASKMEMM:
                        if money < 0:
                            money = -1 * money - 1
                            profit += money + 1
                        # storage
                        db_cmd.update_bank(
                            0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=0, money=round(float(product_price), 2))
                        # cur
                        db_cmd.update_bank(order[7], round(
                            float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                        # mng
                        db_cmd.update_bank(order[2], round(
                            float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=order[2], money=round(float(profit * 0.25), 2))
                        # top_mng TOPMNG
                        db_cmd.update_bank(TOPMNG, round(
                            float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.125), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.125), 2))
                        # god ASKME
                        db_cmd.update_bank(ASKME, round(
                            float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.125), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=ASKME, money=round(float(profit * 0.125), 2))
                        # top 1 VLADELEC1
                        db_cmd.update_bank(VLADELEC1, round(
                            float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                        # top 2 VLADELEC2
                        db_cmd.update_bank(VLADELEC2, round(
                            float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                        db_cmd.add_financial_operation(
                            id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                    elif order[2] in GODCHIKI:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.175), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(CHIKIPIKI, round(
                                float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.175), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.175), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.35), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.35), 2))
                            # god_partner CHIKIPIKI
                            db_cmd.update_bank(CHIKIPIKI, round(
                                float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.35), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.35), 2))
                    elif order[2] == PIFPAF:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.4), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.4), 2))
                        elif profit < 0 and money >= 0:
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.4), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.4), 2))
                    elif order[2] in MEDICAPTAINGR:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner CHIKIPIKI
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(MEDICAPTAIN, round(
                                float(db_cmd.get_user_bank(MEDICAPTAIN)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MEDICAPTAIN, money=round(float(profit * 0.15), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                            # god_partner 2
                            db_cmd.update_bank(MEDICAPTAIN, round(
                                float(db_cmd.get_user_bank(MEDICAPTAIN)[1]), 2) + round(float(profit * 0.3), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MEDICAPTAIN, money=round(float(profit * 0.3), 2))
                    elif order[2] in JAMAIKAGR:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(JAMAIKA, round(
                                float(db_cmd.get_user_bank(JAMAIKA)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=JAMAIKA, money=round(float(profit * 0.15), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                            # god_partner 2
                            db_cmd.update_bank(JAMAIKA, round(
                                float(db_cmd.get_user_bank(JAMAIKA)[1]), 2) + round(float(profit * 0.3), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=JAMAIKA, money=round(float(profit * 0.3), 2))
                    elif order[2] in MANIAKGR:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.05), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.05), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.1), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.1), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                            # god_partner 2
                            db_cmd.update_bank(MANIAK_KATAN, round(
                                float(db_cmd.get_user_bank(MANIAK_KATAN)[1]), 2) + round(float(profit * 0.15), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MANIAK_KATAN, money=round(float(profit * 0.15), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # top_mng TOPMNG
                            db_cmd.update_bank(TOPMNG, round(
                                float(db_cmd.get_user_bank(TOPMNG)[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=TOPMNG, money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                            # god_partner 2
                            db_cmd.update_bank(MANIAK_KATAN, round(
                                float(db_cmd.get_user_bank(MANIAK_KATAN)[1]), 2) + round(float(profit * 0.3), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=MANIAK_KATAN, money=round(float(profit * 0.3), 2))
                    elif order[2] == TOPMNG:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.1), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.1), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.2), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.2), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.2), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.2), 2))
                            # god ASKME
                            db_cmd.update_bank(ASKME, round(
                                float(db_cmd.get_user_bank(ASKME)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=ASKME, money=round(float(profit * 0.4), 2))
                            # god_partner BOODU
                            db_cmd.update_bank(BOODU, round(
                                float(db_cmd.get_user_bank(BOODU)[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BOODU, money=round(float(profit * 0.4), 2))
                    elif order[2] in CHIKIPIKIG:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            try:
                                db_cmd.update_bank(order[7], round(
                                    float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                                db_cmd.add_financial_operation(
                                    id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            except Exception as e:
                                print(r, "nocur")
                            # CHIKIPIKI
                            db_cmd.update_bank(CHIKIPIKI, round(
                                float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit * 0.45), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit * 0.45), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.275), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.275), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.275), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.275), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(CHIKIPIKI, round(
                                float(db_cmd.get_user_bank(CHIKIPIKI)[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=CHIKIPIKI, money=round(float(profit), 2))
                    elif order[2] in SHAKIRAGROUP:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # SHAKIRA
                            db_cmd.update_bank(SHAKIRA, round(
                                float(db_cmd.get_user_bank(SHAKIRA)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=SHAKIRA, money=round(float(profit * 0.5), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(SHAKIRA, round(
                                float(db_cmd.get_user_bank(SHAKIRA)[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=SHAKIRA, money=round(float(profit), 2))
                    elif order[2] in BORKOHVAG:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # SHAKIRA
                            db_cmd.update_bank(BARKHV, round(
                                float(db_cmd.get_user_bank(BARKHV)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BARKHV, money=round(float(profit * 0.5), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(BARKHV, round(
                                float(db_cmd.get_user_bank(BARKHV)[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=BARKHV, money=round(float(profit), 2))
                    elif order[2] in WW420GR:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            db_cmd.update_bank(WW420, round(
                                float(db_cmd.get_user_bank(WW420)[1]), 2) + round(float(profit * 0.35), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=WW420, money=round(float(profit * 0.35), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(WW420, round(
                                float(db_cmd.get_user_bank(WW420)[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=WW420, money=round(float(profit), 2))
                    elif order[2] in SOLO50:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:

                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # SHAKIRA
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.5), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.25), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.25), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.25), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] in SOLO40:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:

                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # SHAKIRA
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.4), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.4), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.3), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.3), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.3), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.3), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] in SOLO35:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit * 0.35), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit * 0.35), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.325), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.325), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.325), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.325), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # mng
                            db_cmd.update_bank(order[2], round(
                                float(db_cmd.get_user_bank(order[2])[1]), 2) + round(float(profit), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[2], money=round(float(profit), 2))
                    elif order[2] == SHABAEN_VLADELCI:
                        if (profit >= 0 and money > 0) or (profit < 0 and money < 0) or city in ['צילומים', 'צילומים2', 'צילומים3']:
                            if money < 0:
                                money = -1 * money - 1
                                profit += money + 1
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.5), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.5), 2))
                        elif profit < 0 and money >= 0:
                            # storage
                            db_cmd.update_bank(
                                0, round(float(db_cmd.get_user_bank(0)[1]), 2) + round(float(product_price), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=0, money=round(float(product_price), 2))
                            # cur
                            db_cmd.update_bank(order[7], round(
                                float(db_cmd.get_user_bank(order[7])[1]), 2) + round(float(cur), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=order[7], money=round(float(cur), 2))
                            # top 1 VLADELEC1
                            db_cmd.update_bank(VLADELEC1, round(
                                float(db_cmd.get_user_bank(VLADELEC1)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC1, money=round(float(profit * 0.5), 2))
                            # top 2 VLADELEC2
                            db_cmd.update_bank(VLADELEC2, round(
                                float(db_cmd.get_user_bank(VLADELEC2)[1]), 2) + round(float(profit * 0.5), 2))
                            db_cmd.add_financial_operation(
                                id_order=order[0], user_id=VLADELEC2, money=round(float(profit * 0.5), 2))
                    else:
                        k = 1

                    if k == 0:
                        db_cmd.update_order(order[0], "time", 1)
    print('sleepnow')
    time.sleep(300)
    print('work')
