
from bs4 import BeautifulSoup
import sqlite3
import requests
import re

import LEGO
from LEGO import *



def get_details_from_web(set_nr):
    details_dict = {"Setnummer": set_nr, "Name": "", "Erscheinungsjahr": "", "UVP": "", "Thema": "", }
    url = "https://www.brickmerge.de/" + str(set_nr)
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    if source.status_code > 400 or str(set_nr) + " Preisvergleich" in soup.title.string:
        #print("Die gesuche SET-Nummer ist nicht vorhanden")
        return None
    text = soup.find_all(text=True)
    for index, elem in enumerate(text):
        if "| Artikel-Nr:" in elem:
            name = str(text[index - 1])
            pure_name_pos = re.match('.+([0-9])[^0-9]*$', name)
            details_dict["Name"] = name[pure_name_pos.end(1) + 1:]
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
    try:
        db = sqlite3.connect('lego_db')
        db.cursor()
        db.execute(f"""INSERT INTO lego_themes(themeName, subTheme) VALUES ("{themeNameTO}","{subThemeTO}"
                       )""")
        db.commit()
        text = f"Thema {themeNameTO} erfolgreich in die Datenbank hinzugefuegt."
    except:
        text = "Fehler beim anlegen des Themas."

    finally:
        return text

def add_shop_to_DB(shopNameTO, urlTO):
    try:
        db = sqlite3.connect('lego_db')
        db.cursor()
        db.execute(f"""INSERT INTO lego_shops VALUES ("{shopNameTO}","{urlTO}"
                       )""")
        db.commit()
        text = f"Shop {shopNameTO} erfolgreich in die Datenbank hinzugefuegt."
    except:
        text = "Fehler beim anlegen des Shops."

    finally:
        return text

def add_set_to_DB(id,name,retail,theme,release,subtheme):
    if id:
        try:
            db = sqlite3.connect('lego_db')
            db.cursor()
            text=""
            if not theme in get_theme_list() and theme != "" and theme != "Neues Thema anlegen":
                add_theme_to_DB(theme,subtheme)
                text=f"Neues Thema '{theme}' wurde hinzugefuegt.\n"

            db.execute(f"""INSERT INTO main.lego_sets VALUES ("{id}","{name}","{retail}","{release}","{theme}"
                           )""")
            db.commit()
            text = text + f"SET {id} erfolgreich in die Datenbank hinzugefuegt."
        except Exception as e:
            text = text + "Fehler beim anlegen des Sets."
            print(e)

        finally:
            return text
    else:
        return "Bitte Textfelder fuellen.\n"

def add_purchase_to_db(cost,date,shop,amount,id,retail):
    if cost:
        discountE = int(retail)-int(cost)
        discountP = (1-int(cost)/int(retail))*100

        try:
            db = sqlite3.connect('lego_db')
            db.cursor()
            text = ""
            if not shop in get_shop_list() and shop != "" and shop != "Neuen Shop anlegen":
                add_shop_to_DB(shop)
                text = f"Neuer Shop '{shop}' wurde hinzugefuegt.\n"

            db.execute(f"""INSERT INTO main.lego_purchases(purchasePrice,purchaseDate,purchaseDisc,purchaseAmount,purchaseSet,purchaseShop) 
                            VALUES ("{cost}","{date}","{discountP}","{amount}","{id}","{shop}"
                               )""")
            db.commit()
            text = text + f"Kauf von {id} erfolgreich in das Depot hinzugefuegt."
        except Exception as e:
            text = text + "Fehler beim anlegen des Sets."
            print(e)

        finally:
            return text
    else:
        return "Bitte Textfelder fuellen.\n"



def get_shop_list():
    db = sqlite3.connect('lego_db')
    cursor = db.cursor()
    cursor.execute("SELECT shopName FROM lego_shops;")
    shopList = list()

    for index in cursor.fetchall():
        shopList.append(str(index)[2:-3])

    return shopList

def get_theme_list():
    db = sqlite3.connect('lego_db')
    cursor = db.cursor()
    cursor.execute("SELECT themeName FROM lego_themes;")
    themeList = list()

    for index in cursor.fetchall():
        themeList.append(str(index)[2:-3])

    return themeList

def get_set_records():
    db = sqlite3.connect('lego_db')
    cursor = db.cursor()
    cursor.execute("""SELECT setID,setName,setTheme,setUvp,setYear FROM lego_sets""")
    setList = cursor.fetchall()
    cursor.close()

    return setList

def get_theme_records():
    db = sqlite3.connect('lego_db')
    cursor = db.cursor()
    cursor.execute("SELECT themeName,subTheme FROM lego_themes;")
    themeList = cursor.fetchall()
    cursor.close()

    return themeList
