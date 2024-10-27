import sqlite3 as sql
import os
from data import data

class Database:
    def __init__(self, path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(script_dir, path)
        self.con = sql.connect(self.path)

    def create_table(self):
        with self.con:
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name VARCHAR(50) NOT NULL,
                permissions TEXT
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                role_id INTEGER,
                balance DECIMAL DEFAULT 0,
                successful_bids INTEGER DEFAULT 0,
                auto_bid_access BOOLEAN DEFAULT 0,
                is_banned BOOLEAN DEFAULT 0,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(12) NOT NULL,
                balance DECIMAL DEFAULT 0,
                role_id INTEGER,
                commission_rate DECIMAL DEFAULT 5,
                penalties INTEGER DEFAULT 0,
                FOREIGN KEY (role_id) REFERENCES roles(role_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL NOT NULL,
                quantity INTEGER NOT NULL
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Product_images (
                image_tg VARCHAR(40),
                image_pt VARCHAR(255) NOT NULL,
                product_id INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Lots(
                lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                starting_price DECIMAL NOT NULL,
                seller_id INTEGER,
                start_time DATETIME,
                end_time DATETIME,
                document_type VARCHAR(50) CHECK(document_type IN ('Ювелирный', 'Историч ценный', 'Стандартный')),
                status VARCHAR(20) CHECK(status IN ('в процессе', 'продан', 'не продан')) DEFAULT 'в процессе',
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (seller_id) REFERENCES users(user_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Bids (
                bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                user_id INTEGER,
                bid_amount DECIMAL NOT NULL,
                bid_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Auction_history  (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                winner_id INTEGER,
                final_price DECIMAL NOT NULL,
                completion_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id),
                FOREIGN KEY (winner_id) REFERENCES users(user_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Complaints_strikes   (
                complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
                complainant_id INTEGER,
                target_admin_id INTEGER,
                reason TEXT NOT NULL,
                status VARCHAR(20) CHECK(status IN ('в ожидании', 'решена')) DEFAULT 'в ожидании',
                strike_count INTEGER DEFAULT 0,
                FOREIGN KEY (complainant_id) REFERENCES users(user_id),
                FOREIGN KEY (target_admin_id) REFERENCES admins(admin_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Strikes   (
                strike_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                admin_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                strike_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (admin_id) REFERENCES admins(admin_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Transfer_documents    (
                document_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                buyer_id INTEGER,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES lots(lot_id),
                FOREIGN KEY (buyer_id) REFERENCES users(user_id)
                )
                ''')

    def get_data(self, table, name_table, data):
        for item in data[name_table]:
            self.con.execute(table, item)
    def fill_table(self, data):
        sql_insert_roles = "INSERT INTO roles (role_name, permissions) values(?, ?)"
        sql_insert_users = "INSERT INTO users (username, role_id, balance, successful_bids, auto_bid_access, is_banned) values(?, ?, ?, ?, ?, ?)"
        sql_insert_admins = "INSERT INTO admins (username, password, balance, role_id, commission_rate, penalties) values(?, ?, ?, ?, ?, ?)"
        sql_insert_products = "INSERT INTO products (title, description, price, quantity) values(?, ?, ?, ?)"
        sql_insert_product_images = "INSERT INTO product_images (image_tg, image_pt, product_id) values(?, ?, ?)"
        sql_insert_lots = "INSERT INTO lots (product_id, starting_price, seller_id, start_time, end_time, document_type, status) values(?, ?, ?, ?, ?, ?, ?)"
        sql_insert_bids = "INSERT INTO bids (lot_id, user_id, bid_amount) values(?, ?, ?)"
        sql_insert_auction_history = "INSERT INTO auction_history (lot_id, winner_id, final_price) values(?, ?, ?)"
        sql_insert_complaints_strikes = "INSERT INTO complaints_strikes (complainant_id, target_admin_id, reason, status, strike_count) values(?, ?, ?, ?, ?)"
        sql_insert_strikes = "INSERT INTO strikes (user_id, admin_id, reason) values(?, ?, ?)"
        sql_insert_transfer_documents = "INSERT INTO transfer_documents (lot_id, buyer_id) values(?, ?)"

        self.get_data(sql_insert_roles, 'roles', data)
        self.get_data(sql_insert_users, 'users', data)
        self.get_data(sql_insert_admins, 'admins', data)
        self.get_data(sql_insert_products, 'products', data)
        self.get_data(sql_insert_product_images, 'product_images', data)
        self.get_data(sql_insert_lots, 'lots', data)
        self.get_data(sql_insert_bids, 'bids', data)
        self.get_data(sql_insert_auction_history, 'auction_history', data)
        self.get_data(sql_insert_complaints_strikes, 'complaints_strikes', data)
        self.get_data(sql_insert_strikes, 'strikes', data)
        self.get_data(sql_insert_transfer_documents, 'transfer_documents', data)
        self.con.commit()

    def clear_data(self):
        with self.con:
            self.con.execute("DELETE FROM Roles")
            self.con.execute("DELETE FROM Users")
            self.con.execute("DELETE FROM Admins")
            self.con.execute("DELETE FROM Products")
            self.con.execute("DELETE FROM Product_images")
            self.con.execute("DELETE FROM Lots")
            self.con.execute("DELETE FROM Bids")
            self.con.execute("DELETE FROM Auction_history")
            self.con.execute("DELETE FROM Complaints_strikes")
            self.con.execute("DELETE FROM Strikes")
            self.con.execute("DELETE FROM Transfer_documents")
        self.con.commit()
    def delete_table(self):
        with self.con:
            self.con.execute("DROP TABLE IF EXISTS Roles")
            self.con.execute("DROP TABLE IF EXISTS Users")
            self.con.execute("DROP TABLE IF EXISTS Admins")
            self.con.execute("DROP TABLE IF EXISTS Products")
            self.con.execute("DROP TABLE IF EXISTS Product_images")
            self.con.execute("DROP TABLE IF EXISTS Lots")
            self.con.execute("DROP TABLE IF EXISTS Bids")
            self.con.execute("DROP TABLE IF EXISTS Auction_history")
            self.con.execute("DROP TABLE IF EXISTS Complaints_strikes")
            self.con.execute("DROP TABLE IF EXISTS Strikes")
            self.con.execute("DROP TABLE IF EXISTS Transfer_documents")
        self.con.commit()


db = Database('my_database.db')


# db.clear_data()
# db.delete_table()
# db.create_table()
# db.fill_table(data)
