#import psycopg2
import sqlite3




def create_table(db):
    c = db.cursor()
    c.execute('''

                CREATE TABLE IF NOT EXISTS lego_sets(
                    setID int NOT NULL,
                    setName varchar(30) NOT NULL ,
                    setUvp float,
                    setYear int,
                    setTheme varchar(30),
                    PRIMARY KEY (setID),
                    FOREIGN KEY (setTheme) REFERENCES lego_themes(themeName)
                ); 
                ''')
    c.execute('''
                
                CREATE TABLE IF NOT EXISTS lego_themes(
                    themeID INTEGER PRIMARY KEY AUTOINCREMENT,
                    themeName varchar(30) NOT NULL ,
                    subTheme varchar(30)
                );
                ''')
    c.execute('''
                CREATE TABLE IF NOT EXISTS lego_shops(
                    shopName varchar(30) NOT NULL ,
                    shopUrl varchar(80),
                    PRIMARY KEY (shopName)
                );
                ''')
    c.execute('''
                CREATE TABLE IF NOT EXISTS lego_purchases(
                    purchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
                    purchasePrice float,
                    purchaseDate date,
                    purchaseDisc float,
                    purchaseAmount int,
                    purchaseSet int NOT NULL ,
                    purchaseShop varchar(30),
                    FOREIGN KEY (purchaseSet) REFERENCES lego_sets(setID),
                    FOREIGN KEY (purchaseShop) REFERENCES lego_shops(shopName)  
                );
                ''')

    db.commit()


if __name__ == '__main__':
    db = sqlite3.connect('lego_db')

    create_table(db)
