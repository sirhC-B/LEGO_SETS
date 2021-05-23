import db_conn

def create_table(db):
    c = db.cursor()
    c.execute('''CREATE SCHEMA IF NOT EXISTS lego; ''')
    c.execute('''SET schema 'lego'; ''')

    c.execute('''
                CREATE TABLE IF NOT EXISTS lego_themes(
                    themeID SERIAL PRIMARY KEY,
                    themeName varchar(60) unique not null ,
                    subTheme varchar(60)
                );
                ''')
    c.execute('''

                CREATE TABLE IF NOT EXISTS lego_sets(
                    setID int NOT NULL unique ,
                    setName varchar(60) NOT NULL ,
                    setUvp float,
                    setYear int,
                    setTheme int,
                    PRIMARY KEY (setID),
                    FOREIGN KEY (setTheme) REFERENCES lego_themes(themeID)
                ); 
                ''')
    c.execute('''
                CREATE TABLE IF NOT EXISTS lego_shops(
                    shopID SERIAL PRIMARY KEY, 
                    shopName varchar(30) NOT NULL unique ,
                    shopUrl varchar(80)
                );
                ''')
    c.execute('''
                CREATE TABLE IF NOT EXISTS lego_purchases(
                    purchaseID SERIAL PRIMARY KEY,
                    purchasePrice float,
                    purchaseDate date,
                    purchaseDisc float,
                    purchaseAmount int,
                    purchaseSet int NOT NULL ,
                    purchaseShop int,
                    FOREIGN KEY (purchaseSet) REFERENCES lego_sets(setID),
                    FOREIGN KEY (purchaseShop) REFERENCES lego_shops(shopID)  
                );
                ''')

    db.commit()
    c.close()
    #db.close()


# if __name__ == '__main__':
#     create_table(db_conn.db)
