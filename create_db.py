#import psycopg2
import sqlite3




def create_table(db):
    c = db.cursor()
    c.execute('''

                CREATE TABLE lego_sets(
                    setID int NOT NULL,
                    setName varchar(30),
                    setUvp float,
                    setYear int,
                    setTheme varchar(30),
                    PRIMARY KEY (setID),
                    FOREIGN KEY (setTheme) REFERENCES lego_themes(themeName)
                ); 
                ''')
    c.execute('''
                
                CREATE TABLE lego_themes(
                    themeName varchar(30) NOT NULL ,
                    subTheme varchar(30),
                    PRIMARY KEY (themeName)
                );
                ''')
    c.execute('''
                CREATE TABLE lego_shops(
                    shopName varchar(30) NOT NULL ,
                    shopUrl varchar(80),
                    PRIMARY KEY (shopName)
                );
                ''')
    c.execute('''
                CREATE TABLE lego_purchases(
                    purchaseID int NOT NULL,
                    purchasePrice float,
                    purchaseDate date,
                    purchaseDisc float,
                    purchaseAmount int,
                    purchaseSet varchar(30),
                    purchaseShop varchar(30),
                    PRIMARY KEY (purchaseID),
                    FOREIGN KEY (purchaseSet) REFERENCES lego_sets(setID),
                    FOREIGN KEY (purchaseShop) REFERENCES lego_shops(shopName)  
                );
                ''')

    db.commit()


if __name__ == '__main__':
    db = sqlite3.connect('lego_db')

    create_table(db)