from bs4 import BeautifulSoup
import sqlite3
import requests
import re

import LEGO
import db_conn
from LEGO import *

global db
db = db_conn.db


def get_details_from_web(set_nr):
    if not str(set_nr).isdigit() or int(set_nr) < 1000:
        return None
    details_dict = {"Setnummer": set_nr, "Name": "", "Erscheinungsjahr": "", "UVP": "", "Thema": "", }
    url = "https://www.brickmerge.de/" + str(set_nr)
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    if source.status_code > 400 or str(set_nr) + " Preisvergleich" in soup.title.string:
        # print("Die gesuche SET-Nummer ist nicht vorhanden")
        return None
    text = soup.find_all(text=True)
    for index, elem in enumerate(text):
        if "| Artikel-Nr:" in elem:
            name = str(text[index - 1])
            if (name.find(str(set_nr)) != -1):
                set_nr_pos = name.find(str(set_nr))
            details_dict["Name"] = name[set_nr_pos + len(str(set_nr)) + 1:]
        elif "| Erscheinungsjahr: " in elem:
            pubYear = str(text[index + 1])
            details_dict["Erscheinungsjahr"] = pubYear
        elif "| UVP:" in elem:
            uvp = str(text[index + 1])
            details_dict["UVP"] = uvp

        elif "LEGO Themen" in elem:
            thema = text[index + 3]
            thema = thema[5:]
            details_dict["Thema"] = thema

    return details_dict


def add_theme_to_DB(themeNameTO, subThemeTO):
    if themeNameTO:
        try:
            c = db.cursor()
            c.execute(f"""INSERT INTO lego_themes(themeName, subTheme) VALUES ('{themeNameTO}','{subThemeTO}'
                           )""")
            db.commit()
            c.close()
            text = f"Thema {themeNameTO} erfolgreich in die Datenbank hinzugefuegt."
        except Exception as e:
            text = "Fehler beim anlegen des Themas."
            print(format(e))

        finally:
            return text
    else:
        return "Bitte Name des Themas angeben."


def add_shop_to_DB(shopNameTO, urlTO):
    if shopNameTO:
        try:
            c = db.cursor()
            c.execute(f"""INSERT INTO lego_shops(shopName, shopUrl) VALUES ('{shopNameTO}','{urlTO}'
                           )""")
            db.commit()
            c.close()
            text = f"Shop {shopNameTO} erfolgreich in die Datenbank hinzugefuegt."
        except Exception as e:
            text = "Fehler beim anlegen des Shops."
            print(format(e))

        finally:
            return text
    else:
        return "Bitte Namen des Shops angeben."


def add_set_to_DB(id, name, retail, theme, release, subtheme):
    if id and name and retail and theme and release:
        try:
            c = db.cursor()
            text = ""
            if not theme in get_theme_list() and theme != "Neues Thema anlegen":
                add_theme_to_DB(theme, subtheme)
                text = f"Neues Thema '{theme}' wurde hinzugefuegt.\n"

            c.execute(f"SELECT themeid FROM lego_themes WHERE themename='{theme}';")
            themeid = c.fetchone()


            retail_float = float(retail[:-2].replace(",", "."))

            c.execute(f"""INSERT INTO lego_sets VALUES ('{id}','{name}','{retail_float}','{release}','{themeid[0]}'
                           )""")
            db.commit()
            c.close()
            text = text + f"SET {id} erfolgreich in die Datenbank hinzugefuegt."


        except Exception as e:
            print(e)
            text += f"Das Set {id} ist bereits in der Datenbank vorhanden."

        except Exception as e:
            print(format(e))
            text += "Fehler beim anlegen des Sets."

        finally:
            return text
    else:
        return "Bitte Textfelder fuellen.\n"


def add_purchase_to_db(cost, date, shop, amount, id, retail, name, theme, release, subtheme):
    if cost and id and name:
        text = ""
        if id not in get_set_list():
            print(get_set_list())
            text += add_set_to_DB(id, name, retail, theme, release, subtheme) + "\n"

        retail = float(str(retail).replace(',', '.')[:-2])
        cost = float(str(cost).replace(',', '.'))
        discountP = round((1 - (cost / retail)) * 100, 2)

        try:
            c = db.cursor()
            if not shop in get_shop_list() and shop != "" and shop != "Neuen Shop anlegen":
                add_shop_to_DB(shop)
                text = f"Neuer Shop '{shop}' wurde hinzugefuegt.\n"

            c.execute(f"SELECT shopid FROM lego_shops WHERE shopname='{shop}';")
            shop = c.fetchone()[0]

            c.execute(f"""INSERT INTO lego_purchases(purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,purchaseSet,purchaseShop) 
                            VALUES ('{cost}',TO_DATE('{date}','YYYY-MM-DD'),'{discountP}','{amount}','{id}','{shop}')
                               """)
            db.commit()
            c.close()
            text = text + f"Kauf von {id} erfolgreich in das Depot hinzugefuegt."

        except Exception as e:
            text = text + "Fehler beim anlegen des Sets."
            print(e)

        finally:
            return text
    else:
        return "Bitte Textfelder fuellen.\n"


def get_shop_list():
    cursor = db.cursor()
    cursor.execute("SELECT shopName FROM lego_shops;")
    shopList = list()

    for index in cursor.fetchall():
        shopList.append(str(index)[2:-3])
    cursor.close()
    return shopList


def get_theme_list():
    cursor = db.cursor()
    cursor.execute("SELECT themeName FROM lego_themes;")
    themeList = list()

    for index in cursor.fetchall():
        themeList.append(str(index)[2:-3])
    cursor.close()
    return themeList


def get_set_list():
    cursor = db.cursor()
    cursor.execute("SELECT setID FROM lego_sets;")
    setList = list()

    for index in cursor.fetchall():
        setList.append(str(index)[1:-2])
    cursor.close()
    return setList


def get_set_records():
    cursor = db.cursor()
    cursor.execute("""SELECT setID,setName,setTheme,setUvp,setYear FROM lego_sets""")
    setList = cursor.fetchall()
    cursor.close()

    return setList


def get_purchase_records(filter, order='purchaseID'):
    # db2 = db_conn.db
    cursor = db.cursor()
    if (filter == NONE):
        cursor.execute(f"""SELECT purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,
                        purchaseSet,shopName,setName,themeName,setUvp,setYear,purchaseDisc,purchaseID FROM lego_purchases
                        JOIN lego_sets ON lego_purchases.purchaseSet = lego_sets.setID
                        JOIN lego_themes ON lego_sets.setTheme = lego_themes.themeID
                        JOIN lego_shops ON lego_purchases.purchaseShop = lego_shops.shopID
                        ORDER BY {order} """)
    else:
        cursor.execute(f"SELECT themeid FROM lego_themes WHERE themename='{filter}';")
        filter = cursor.fetchone()[0]
        cursor.execute(f"""SELECT purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,
                            purchaseSet,shopName,setName,themeName,setUvp,setYear,purchaseDisc,purchaseID FROM lego_purchases
                            JOIN lego_sets ON lego_purchases.purchaseSet = lego_sets.setID
                            JOIN lego_themes ON lego_sets.setTheme = lego_themes.themeID
                            JOIN lego_shops ON lego_purchases.purchaseShop = lego_shops.shopID
                            WHERE setTheme='{filter}'
                            ORDER BY {order} """)
    purchaseList = cursor.fetchall()


    db.commit()
    cursor.close()

    return purchaseList


def get_theme_records():
    cursor = db.cursor()
    cursor.execute("SELECT themeName,subTheme FROM lego_themes;")
    themeList = cursor.fetchall()
    cursor.close()

    return themeList


def get_shop_records():
    cursor = db.cursor()
    cursor.execute("SELECT shopName,shopUrl FROM lego_shops;")
    shopList = cursor.fetchall()
    cursor.close()

    return shopList


def delete_purchase_from_db(iid):
    try:
        cursor = db.cursor()
        cursor.execute(f"""DELETE FROM lego_purchases WHERE purchaseID='{iid}'; """)
        db.commit()
        cursor.close()

    except Exception as e:
        print(e)
        return ("Fehler beim loeschen des Sets.")

    return ("Set wurde erfolgreich entfernt.")


def search_for_purchase(iid):
    cursor = db.cursor()
    cursor.execute(f"""SELECT purchaseID,purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,purchaseSet,shopName 
                        FROM lego_purchases 
                        JOIN lego_shops ON lego_purchases.purchaseShop = lego_shops.shopID
                        WHERE purchaseID='{iid}'; """)
    result = cursor.fetchall()
    cursor.close()

    return result
