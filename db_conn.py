from tkinter import Tk, messagebox
import psycopg2
import os
from dotenv import load_dotenv

import functions

ENDPOINT = "lego-oos.cwe1ewbx6zz5.us-east-1.rds.amazonaws.com"
PORT = "5432"
USR = "postgresOOS"
REGION = "us-east-1"
DBNAME = "postgresSQL"
load_dotenv()
PASS = os.environ.get('PASS')
try:
    db = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
    db.autocommit =True;
except Exception as e:
    rootWin = Tk()
    rootWin.withdraw()
    messagebox.showerror("Fehler", "Fehler beim Verbindungsaufbau zur Datenbank aufgrund von {}".format(e),
                         parent=rootWin)
    rootWin.destroy()

# themeNameTO = "THEMA!"
# subThemeTO=""
# c = db.cursor()
# c.execute(f"""INSERT INTO lego_themes(themeName, subTheme) VALUES ('{themeNameTO}','{subThemeTO}'
#                )""")
# db.commit()
# c.close()
# db.close()