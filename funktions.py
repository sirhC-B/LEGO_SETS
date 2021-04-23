from bs4 import BeautifulSoup
import requests,re

from LEGO import *

def get_details_from_web(set_nr):

    details = []
    details_dict = {"Setnummer":set_nr, "Name" : "", "Erscheinungsjahr" : "", "UVP" : "", "Thema" : "",}
    url = "https://www.brickmerge.de/" + str(set_nr)
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    if source.status_code > 400 or str(set_nr)+ " Preisvergleich" in soup.title.string:
        print("Die gesuche SET-Nummer ist nicht vorhanden")
        return None
    text = soup.find_all(text=True)
    for index, elem in enumerate(text):
        if "| Artikel-Nr:" in elem:
            name = str(text[index - 1])
            #details.append("Name:" + name) # hinzu zu array
            #details_dict["Name"] = name # hinzu zu dict
        elif "| Erscheinungsjahr: " in elem:
            pubYear = str(text[index + 1])
            details.append("Erscheinungsjahr: " + pubYear)
            details_dict["Erscheinungsjahr"] = pubYear
        elif "| UVP:" in elem:
            uvp = str(text[index + 1])
            details.append("UVP: " + uvp)
            details_dict["UVP"] = uvp

        elif "LEGO Themen" in elem:
            thema = text[index + 3]
            thema = thema[5:]
            details.append("LEGO Thema: " + thema)
            details_dict["Thema"] = thema
    pure_name_pos = re.match('.+([0-9])[^0-9]*$', name)
    details.append("Name:" + name)
    details_dict["Name"] = name[pure_name_pos.end(1)+1:]

    return details_dict


