from bs4 import BeautifulSoup
import requests
import re
import LEGO
import db_conn
from LEGO import *
from datetime import datetime, timedelta, date

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
            print(type(e))
            if str(type(e)) == "<class 'psycopg2.errors.UniqueViolation'>":
                text += f"Das Set {id} ist bereits in der Datenbank vorhanden."
            elif str(type(e)) == "<class 'ValueError'>":
                text += f"Bitte fuellen sie die Felder mit ein richtigen Datentypen."
            else:
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

        try:
            retail = float(str(retail).replace(',', '.')[:-2])
            cost = float(str(cost).replace(',', '.'))
            discountP = round((1 - (cost / retail)) * 100, 2)
        except Exception as e:
            print(e)
            return "Bitte fuellen sie die Textfelder 'Retail' und 'Cost' mit einer Zahl."

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
    cursor.execute("""SELECT setID,setName,themeName,setUvp,setYear FROM lego_sets
                        JOIN lego_themes ON lego_sets.setTheme = lego_themes.themeID""")
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


def delete_shop_from_db(iid):
    try:
        cursor = db.cursor()
        cursor.execute(f"""DELETE FROM lego_shops WHERE shopName='{iid}'; """)
        db.commit()
        cursor.close()

    except Exception as e:
        print(e)
        if (str(type(e)) == "<class 'psycopg2.errors.ForeignKeyViolation'>"):
            return ("Shop kann nicht geloescht werden weil Abhaengkeiten zur Deoptdatenbank bestehen.")
        else:
            return ("Fehler beim loeschen des Shops.")

    return ("Shop wurde erfolgreich entfernt.")


def delete_theme_from_db(iid):
    try:
        cursor = db.cursor()
        cursor.execute(f"""DELETE FROM lego_themes WHERE themeName='{iid}'; """)
        db.commit()
        cursor.close()

    except Exception as e:
        print(e)
        if (str(type(e)) == "<class 'psycopg2.errors.ForeignKeyViolation'>"):
            return ("Thema kann nicht geloescht werden weil Abhaengkeiten zur Setdatenbank bestehen.")
        else:
            return ("Fehler beim loeschen des Shops.")

    return ("Thema wurde erfolgreich entfernt.")


def search_for_purchase(iid):
    cursor = db.cursor()
    cursor.execute(f"""SELECT purchaseID,purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,purchaseSet,shopName 
                        FROM lego_purchases 
                        JOIN lego_shops ON lego_purchases.purchaseShop = lego_shops.shopID
                        WHERE purchaseID='{iid}'; """)
    result = cursor.fetchall()
    cursor.close()
    return result


def get_lego_purchas_pie():
    cursor = db.cursor()
    cursor.execute("""SELECT  Distinct(themename)  FROM lego_purchases
                    JOIN lego_sets ON lego_purchases.purchaseSet = lego_sets.setID
					JOIN lego_themes ON lego_sets.settheme = lego_themes.themeid""")
    db_data = cursor.fetchall()
    themen = {}
    for x in db_data:
        themen.update({x[0]: 0})
    for y in themen:
        cursor.execute(f"""SELECT  count((settheme)) FROM lego_purchases
                        JOIN lego_sets ON lego_purchases.purchaseSet = lego_sets.setID
                        JOIN lego_themes ON lego_sets.settheme = lego_themes.themeid
                        WHERE themename='{y}' 
                        """)
        themen[y] = int(cursor.fetchone()[0])
    cursor.close()
    return themen


def get_retail_pie():
    last_7days = {}
    for i in range(7):
        last_7days.update({date.today() - timedelta(days=i): 0})

    cursor = db.cursor()
    for day in last_7days:
        cursor.execute(f"""SELECT  cast(sum(purchaseprice*purchaseamount) as integer) FROM lego_purchases
                        WHERE purchasedate='{day}'
                        """)
        sum = (cursor.fetchone()[0])
        if sum:
            last_7days[day] = sum
    cursor.close()

    return last_7days

def get_retail_pie_dic_ar():
    last_7days = {}
    tmp_array = [None] * 7
    for i in range(7):
        tmp_array[i] = date.today() - timedelta(days=i)
    last_7days.update({"Datum": tmp_array})

    tmp_array2 = [0] * 7
    cursor = db.cursor()
    for i in range(7):
        cursor.execute(f"""
        SELECT  cast(sum(purchaseprice*purchaseamount) as integer) FROM lego_purchases
                        WHERE purchasedate='{tmp_array[i]}'
                        """)
        sum = (cursor.fetchone()[0])
        if sum:
            tmp_array2[i] = sum
    last_7days.update({"sum": tmp_array2})
    cursor.close()

    return last_7days
