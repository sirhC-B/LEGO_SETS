from bs4 import BeautifulSoup
import sqlite3
import requests
import re

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
        db.execute(f"""INSERT INTO lego_themes VALUES ("{themeNameTO}","{subThemeTO}"
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
