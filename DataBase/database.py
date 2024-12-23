import sqlite3 as sql
import os
from PyQt5 import QtCore
import datetime, time

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'my_database.db')


def item_is_not_editable(table):
    for row in range(table.rowCount()):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is not None:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)


class Database:
    def __init__(self):
        self.con = sql.connect(db_path)

    def create_table(self):
        with sql.connect(db_path) as self.con:
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Auto_bids (
                lot_id INTEGER,
                user_id INTEGER,
                max_bid INTEGER,
                current_bid INTEGER,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id),
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER,
                lot_id INTEGER,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id)
                )
                ''')
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
                user_tg_id INTEGER,
                role_id INTEGER,
                balance DECIMAL DEFAULT 0,
                successful_bids INTEGER DEFAULT 0,
                auto_bid_access BOOLEAN DEFAULT 0,
                is_banned BOOLEAN DEFAULT 0,
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)
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
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Lot_images (
                image_tg VARCHAR(40),
                image_pt VARCHAR(255) NOT NULL,
                lot_id INTEGER,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Lots(
                lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                location VARCHAR(50) NOT NULL,
                starting_price DECIMAL NOT NULL,
                seller_id INTEGER,
                start_time DATETIME,
                end_time DATETIME,
                document_type VARCHAR(50) CHECK(document_type IN ('Ювелирный', 'Историч ценный', 'Стандартный')),
                status VARCHAR(20) CHECK(status IN ('В процессе', 'Продан', 'Не продан')) DEFAULT 'В процессе',
                FOREIGN KEY (seller_id) REFERENCES Admins(admin_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Bids (
                bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                user_id INTEGER,
                bid_amount DECIMAL NOT NULL,
                bid_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id),
                FOREIGN KEY (user_id) REFERENCES Users(user_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Auction_history  (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                winner_id INTEGER,
                final_price DECIMAL NOT NULL,
                completion_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id),
                FOREIGN KEY (winner_id) REFERENCES Users(user_id)
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
                FOREIGN KEY (complainant_id) REFERENCES Users(user_id),
                FOREIGN KEY (target_admin_id) REFERENCES Admins(admin_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Strikes   (
                strike_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                admin_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                strike_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (admin_id) REFERENCES Admins(admin_id)
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Transfer_documents    (
                document_id INTEGER PRIMARY KEY AUTOINCREMENT,
                lot_id INTEGER,
                buyer_id INTEGER,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lot_id) REFERENCES Lots(lot_id),
                FOREIGN KEY (buyer_id) REFERENCES Users(user_id)
                )
                ''')
            self.con.commit()

    def get_data(self, table, name_table, data):
        for item in data[name_table]:
            self.con.execute(table, item)

    def fill_table(self, data):
        sql_insert_roles = "INSERT INTO Roles (role_name, permissions) values(?, ?)"
        sql_insert_users = "INSERT INTO Users (username, user_tg_id, role_id, balance, successful_bids, auto_bid_access, is_banned) values(?, ?, ?, ?, ?, ?, ?)"
        sql_insert_admins = "INSERT INTO Admins (username, password, balance, role_id, commission_rate, penalties) values(?, ?, ?, ?, ?, ?)"
        sql_insert_lot_images = "INSERT INTO Lot_images (image_tg, image_pt, lot_id) values(?, ?, ?)"
        sql_insert_lots = "INSERT INTO Lots (title, description, location, starting_price, seller_id, start_time, end_time, document_type, status) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        sql_insert_bids = "INSERT INTO Bids (lot_id, user_id, bid_amount) values(?, ?, ?)"
        sql_insert_auction_history = "INSERT INTO Auction_history (lot_id, winner_id, final_price) values(?, ?, ?)"
        sql_insert_complaints_strikes = "INSERT INTO Complaints_strikes (complainant_id, target_admin_id, reason, status, strike_count) values(?, ?, ?, ?, ?)"
        sql_insert_strikes = "INSERT INTO Strikes (user_id, admin_id, reason) values(?, ?, ?)"
        sql_insert_transfer_documents = "INSERT INTO Transfer_documents (lot_id, buyer_id) values(?, ?)"

        self.get_data(sql_insert_roles, 'roles', data)
        self.get_data(sql_insert_users, 'users', data)
        self.get_data(sql_insert_admins, 'admins', data)
        self.get_data(sql_insert_lot_images, 'lot_images', data)
        self.get_data(sql_insert_lots, 'lots', data)
        self.get_data(sql_insert_bids, 'bids', data)
        self.get_data(sql_insert_auction_history, 'auction_history', data)
        self.get_data(sql_insert_complaints_strikes, 'complaints_strikes', data)
        self.get_data(sql_insert_strikes, 'strikes', data)
        self.get_data(sql_insert_transfer_documents, 'transfer_documents', data)
        self.con.commit()

    def clear_data(self):
        with self.con:
            self.con.execute("DELETE FROM Auto_bids")
            self.con.execute("DELETE FROM Messages")
            self.con.execute("DELETE FROM Roles")
            self.con.execute("DELETE FROM Users")
            self.con.execute("DELETE FROM Admins")
            self.con.execute("DELETE FROM Lot_images")
            self.con.execute("DELETE FROM Lots")
            self.con.execute("DELETE FROM Bids")
            self.con.execute("DELETE FROM Auction_history")
            self.con.execute("DELETE FROM Complaints_strikes")
            self.con.execute("DELETE FROM Strikes")
            self.con.execute("DELETE FROM Transfer_documents")
        self.con.commit()

    def delete_table(self):
        with self.con:
            self.con.execute("DROP TABLE IF EXISTS Auto_bids")
            self.con.execute("DROP TABLE IF EXISTS Messages")
            self.con.execute("DROP TABLE IF EXISTS Roles")
            self.con.execute("DROP TABLE IF EXISTS Users")
            self.con.execute("DROP TABLE IF EXISTS Admins")
            self.con.execute("DROP TABLE IF EXISTS Lot_images")
            self.con.execute("DROP TABLE IF EXISTS Lots")
            self.con.execute("DROP TABLE IF EXISTS Bids")
            self.con.execute("DROP TABLE IF EXISTS Auction_history")
            self.con.execute("DROP TABLE IF EXISTS Complaints_strikes")
            self.con.execute("DROP TABLE IF EXISTS Strikes")
            self.con.execute("DROP TABLE IF EXISTS Transfer_documents")
        self.con.commit()

    def get_table_data(self, table_name):
        data = self.con.execute(f'''SELECT * FROM {table_name}''')
        data = data.fetchall()
        return data

    def get_user_data(self):
        data = self.con.execute('''
            SELECT u.username, r.role_name, u.balance, u.successful_bids, u.auto_bid_access, u.is_banned 
            FROM Users u
            JOIN Roles r ON u.role_id = r.role_id

        ''')
        data = data.fetchall()
        return data

    def get_admin_id(self, username):
        query = '''SELECT admin_id FROM Admins WHERE username = ?'''
        data = self.con.execute(query, (username,)).fetchone()
        return data[0]

    def get_admin_data(self):
        data = self.con.execute('''
            SELECT a.username, a.password, r.role_name, a.balance, a.commission_rate, a.penalties
            FROM Admins a
            JOIN Roles r ON a.role_id = r.role_id
        ''')
        data = data.fetchall()
        return data

    def get_lot_data(self):
        data = self.con.execute('''
            SELECT l.title, l.description, l.location, l.starting_price, a.username,
                    l.start_time, l.end_time, l.document_type, i.image_pt, l.status
            FROM Lots l
            JOIN Admins a ON l.seller_id = a.admin_id
            JOIN Lot_images i ON l.lot_id = i.lot_id
        ''')
        data = data.fetchall()
        return data

    def get_id_lot(self, title, description):
        title = f'{title}'
        description = f'{description}'
        query = '''
            SELECT lot_id 
            FROM Lots 
            WHERE title = ? AND description = ?'''
        data = self.con.execute(query, (title, description)).fetchone()
        return data[0]

    def create_lot(self, title, description, location, starting_price, seller_id, start_time, end_time, document_type,
                   status):
        sql_insert_lots = "INSERT INTO Lots (title, description, location, starting_price, seller_id, start_time, end_time, document_type, status) values(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.con.execute(sql_insert_lots,
                         [title, description, location, starting_price, seller_id, start_time, end_time, document_type,
                          status])
        self.con.commit()

    def add_lot_image(self, image_pt, lot_id):
        sql_insert_product_images = "INSERT INTO Lot_images (image_pt, lot_id) values(?, ?)"
        self.con.execute(sql_insert_product_images,
                         [image_pt, lot_id])
        self.con.commit()

    def update_lot(self, lot_id, title, description, location, starting_price, seller_id, start_time, end_time,
                   document_type, status):
        query = """UPDATE Lots 
                   SET title = ?, description = ?, location = ?, starting_price = ?, seller_id = ?, start_time = ?, end_time = ?, 
                   document_type = ?, status = ? 
                   WHERE lot_id = ?"""
        self.con.execute(query, (
        title, description, location, starting_price, seller_id, start_time, end_time, document_type, status, lot_id))
        self.con.commit()

    def update_lot_image(self, image_path, lot_id):
        query = """UPDATE Lot_images 
                   SET image_pt = ? 
                   WHERE lot_id = ?"""
        self.con.execute(query, (image_path, lot_id))
        self.con.commit()

    def delete_lot_and_images(self, lot_id):

        self.con.execute("BEGIN TRANSACTION")

        delete_images_query = """DELETE FROM Lot_images WHERE lot_id = ?"""
        self.con.execute(delete_images_query, (lot_id,))

        delete_product_query = """DELETE FROM Lots WHERE lot_id = ?"""
        self.con.execute(delete_product_query, (lot_id,))

        self.con.commit()
        self.con.rollback()

    def add_user(self, username, user_tg_id):
        with sql.connect(db_path) as self.con:
            sql_insert_users = "INSERT INTO Users (username, user_tg_id, role_id, balance, successful_bids, auto_bid_access, is_banned) values(?, ?, ?, ?, ?, ?, ?)"
            self.con.execute(sql_insert_users,
                             [username, user_tg_id, 1, 0, 0, 0, 0])
            self.con.commit()
            self.check_user(username, user_tg_id)
    def get_user_id(self, username):
        with sql.connect(db_path) as self.con:
            query = "SELECT user_id FROM Users WHERE username = ?"
            data = self.con.execute(query, (username,)).fetchone()
            return data[0] if data else None

    def check_role(self, name_table, username):
        with sql.connect(db_path) as self.con:
            query = f"SELECT role_id FROM {name_table} WHERE username = ?"
            data = self.con.execute(query, (username,)).fetchone()
            print(data[0])
            return data[0]

    def check_user(self, username, user_tg_id):
        with sql.connect(db_path) as self.con:
            user_query = "SELECT username FROM Users WHERE username = ?"
            data_user = self.con.execute(user_query, (username,)).fetchone()
            print(data_user)
            admin_query = "SELECT username FROM Admins WHERE username = ?"
            data_admin = self.con.execute(admin_query, (username,)).fetchone()
            print(data_admin)
            if data_user is None and data_admin is None:
                self.add_user(username, user_tg_id)
                role = self.check_role('Users', username)
                return role
            elif data_user and data_admin is None:
                print(data_user[0])
                role = self.check_role('Users', data_user[0])
                return role
            elif data_admin and data_user is None:
                role = self.check_role('Admins', data_admin[0])
                return role
            elif data_admin and data_user:
                return 0
            else:
                print('Ошибка')

    def get_lot_data_auction(self):
        with sql.connect(db_path) as self.con:
            query = """
                SELECT l.lot_id, l.starting_price, l.start_time, l.title, l.description, l.location, i.image_pt
                FROM Lots l
                JOIN Lot_images i ON l.lot_id = i.lot_id
                WHERE l.status = 'В процессе'
            """
            data = self.con.execute(query).fetchall()
            return data

    def get_lot_data_by_id(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = """
                SELECT l.lot_id, l.starting_price, l.start_time, l.title, l.description, l.location, i.image_tg
                FROM Lots l
                JOIN Lot_images i ON l.lot_id = i.lot_id
                WHERE l.lot_id = ?
            """
            data = self.con.execute(query, (lot_id,)).fetchall()
            return data
        
    def get_user_lots(self, user_id):
        dt_now = (datetime.datetime.now())  # Определяем текущее время
        with sql.connect(db_path) as self.con:
            query = """
            SELECT l.lot_id, l.title FROM Bids b
                JOIN Lots l 
                    ON b.lot_id = l.lot_id
                WHERE b.user_id = ? and l.end_time > ?   """
            
            data = self.con.execute(query, (user_id, dt_now)).fetchall()
            return data

    def get_end_time(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT end_time FROM Lots WHERE lot_id = ?"
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0]

    def update_image_tg(self, image_tg, image_path):
        with sql.connect(db_path) as self.con:
            query = """UPDATE Lot_images 
                               SET image_tg = ? 
                               WHERE image_pt = ?"""
            self.con.execute(query, (image_tg, image_path))
            self.con.commit()
    def add_message(self, message_id, lot_id):
        with sql.connect(db_path) as self.con:
            sql_insert_users = "INSERT INTO Messages (message_id, lot_id) values(?, ?)"
            self.con.execute(sql_insert_users,[message_id, lot_id])
            self.con.commit()
    def get_message_id(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT message_id FROM Messages WHERE lot_id = ?"
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0]
    def get_bid_lot(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT MAX(bid_amount) FROM Bids WHERE lot_id = ?"
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0] if data else None
        
    def my_get_bid_lot(self, lot_id, user_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT MAX(bid_amount) FROM Bids WHERE lot_id = ? and user_id = ?"
            data = self.con.execute(query, (lot_id, user_id)).fetchone()
            return data[0] if data else None

    def get_user_tg_id_by_bid(self, lot_id, user_id):
        with sql.connect(db_path) as self.con:
            query = """
            SELECT u.user_tg_id 
            FROM Bids b
            JOIN Users u ON b.user_id = u.user_id
            WHERE b.lot_id = ? AND b.user_id = ?
            """
            data = self.con.execute(query, (lot_id, user_id,)).fetchone()
            return data[0]
    def add_bid(self, lot_id, user_id, amount, bid_time):
        with sql.connect(db_path) as self.con:
            sql_insert_bids = "INSERT INTO Bids (lot_id, user_id, bid_amount, bid_time) values(?, ?, ?, ?)"
            self.con.execute(sql_insert_bids, [lot_id, user_id, amount, bid_time])
            self.con.commit()

    def update_bid_user(self, bid_amount, bid_time, user_id, lot_id):
        with sql.connect(db_path) as self.con:
            query = "UPDATE Bids SET bid_amount = ?, bid_time = ? WHERE user_id = ? AND lot_id = ?"
            self.con.execute(query, (bid_amount, bid_time, user_id, lot_id))
            self.con.commit()

    def get_max_bid_auto_bid(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT max_bid FROM Auto_bids WHERE lot_id = ?"
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0] if data else None
    def get_auto_bid(self, lot_id, user_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT max_bid, current_bid FROM Auto_bids WHERE lot_id = ? AND user_id = ?"
            data = self.con.execute(query, (lot_id, user_id)).fetchall()
            return data if data else None
    def get_user_tg_id_by_auto_bid(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = """
            SELECT u.user_tg_id 
            FROM Auto_bids ab
            JOIN Users u ON ab.user_id = u.user_id
            WHERE ab.lot_id = ?
            """
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0]
    def get_user_id_by_auto_bid(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "SELECT user_id FROM Auto_bids WHERE lot_id = ?"
            data = self.con.execute(query, (lot_id,)).fetchone()
            return data[0]

    def add_auto_bid(self, lot_id, user_id, max_bid, current_bid):
        with sql.connect(db_path) as self.con:
            sql_insert_auto_bids = "INSERT INTO Auto_bids (lot_id, user_id, max_bid, current_bid) values(?, ?, ?, ?)"
            self.con.execute(sql_insert_auto_bids,[lot_id, user_id, max_bid, current_bid])
            self.con.commit()
    def update_auto_bid(self, current_bid, user_id, lot_id):
        with sql.connect(db_path) as self.con:
            query = "UPDATE Auto_bids SET current_bid = ? WHERE user_id = ? AND lot_id = ?"
            self.con.execute(query, (current_bid, user_id, lot_id))
            self.con.commit()
    def delete_auto_bid(self, lot_id):
        with sql.connect(db_path) as self.con:
            query = "DELETE FROM Auto_bids WHERE lot_id = ?"
            self.con.execute(query, (lot_id,))
            self.con.commit()

    def addBalance(self, u, amount):
        with sql.connect(db_path) as self.con:
            n = self.con.execute(f"""SELECT balance FROM Users
                                            WHERE Users.username == '{u}'   """)  # Узнаем баланс пользователя
            n = n.fetchall()[0][0]
            n = n + amount  # Суммируем текущий баланс с суммой пополнения
            self.con.execute(f"""UPDATE Users
                                    SET balance = {n}
                                    WHERE Users.username == '{u}'  """)  # Вносим изменения баланса в БД
            return n

    def balance_db(self, u):
        with sql.connect(db_path) as self.con:
            n = self.con.execute(f"""SELECT balance FROM Users
                                            WHERE Users.username == '{u}'  """)  # Узнаем баланс пользователя
            n = n.fetchall()[0][0]
            return n
        
    def newbalance_db(self, id):
        newbalance = self.con.execute(f"""SELECT balance FROM Admins
                                    WHERE admin_id == '{id}'  """)  # Узнаем баланс пользователя
        newbalance = newbalance.fetchall()[0][0]
        return newbalance

    def adminBalance_db(self, id):
        newbalance = self.con.execute(f"""SELECT balance FROM Admins
                                            WHERE admin_id == '{id}'  """)  # Узнаем баланс пользователя
        newbalance = newbalance.fetchall()[0][0]
        return newbalance
    
    # Добавляем баланс 
    def addBalanceMain(self, newBalance, id):
        self.con.execute(f"""UPDATE Admins
                                    SET balance = {newBalance}
                                    WHERE admin_id = {id} """)
        
    def add_delete(self, n, u, newBalance = None, id = None):  # t - индекс товара по выделенной ячейки; u - номер нажатой кнопки
        if u == 8:
            dt_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
            with sql.connect(db_path) as self.con:
                newBalance = round(newBalance, 2)
                self.con.execute(f"""UPDATE Lots
                                    SET end_time = '{dt_now}'
                                    WHERE lot_id = {n} """)
                
                self.con.execute(f"""UPDATE Admins
                                    SET balance = '{newBalance}'
                                    WHERE admin_id = {id} """)
                
                self.con.execute(f"""DELETE FROM Bids  
                                    WHERE lot_id = {n}""")  # Удаляем строчку по индексу чс базы данных                
                
        elif u == 11:
            dt_now = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M')
            with sql.connect(db_path) as self.con:
                self.con.execute(f"""UPDATE Lots
                                    SET end_time = '{dt_now}'
                                    WHERE lot_id = {n} """)

    # Заполнение таблицы товаров на аукционе
    def Auction(self):
        dt_now = (datetime.datetime.now())  # Определяем текущее время
        with sql.connect(db_path) as self.con:
            table = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, MAX(bid_amount), start_time, end_time, username FROM Lots
                                            INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                            INNER JOIN Bids 
                                                ON Lots.lot_id = Bids.lot_id
                                            INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                            WHERE Lots.end_time > '{dt_now}'
                                            GROUP BY Bids.lot_id""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table = table.fetchall()

            tableNULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, start_time, end_time, username FROM Lots
                                            INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                            INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                            LEFT JOIN Bids 
                                                ON Bids.lot_id = Lots.lot_id
                                            WHERE Lots.end_time > '{dt_now}' AND Bids.lot_id IS NULL
                                            """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            tableNULL = tableNULL.fetchall()

            table1 = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, final_price, status, Users.username, Admins.username FROM Lots
                                        INNER JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                        INNER JOIN Users 
                                            ON Auction_history.winner_id = Users.user_id
                                        INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                        WHERE Lots.end_time < '{dt_now}'""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table1 = table1.fetchall()

            table1NULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, status, username  FROM Lots
                                        INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                        INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                        LEFT JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        WHERE Lots.end_time < '{dt_now}'AND Auction_history.lot_id IS NULL""")
            table1NULL = table1NULL.fetchall()

            return [table, tableNULL, table1, table1NULL]

    # Заполнения таблицы моих товаров на аукционе     
    def myProducts_db(self, name):
        dt_now = (datetime.datetime.now())  # Определяем текущее время
        with sql.connect(db_path) as self.con:
            r = self.con.execute(f"""SELECT admin_id FROM Admins
                                                WHERE username = '{name}'   """)
            r = r.fetchall()

            table = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, MAX(bid_amount), start_time, end_time, username FROM Lots
                                            INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                            INNER JOIN Bids 
                                                ON Lots.lot_id = Bids.lot_id
                                            INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                            WHERE Lots.end_time > '{dt_now}' AND seller_id == {r[0][0]}
                                            GROUP BY Bids.lot_id""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table = table.fetchall()

            tableNULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, start_time, end_time, username FROM Lots
                                            INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                            INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                            LEFT JOIN Bids 
                                                ON Bids.lot_id = Lots.lot_id
                                            WHERE Lots.end_time > '{dt_now}' AND seller_id == {r[0][0]} AND Bids.lot_id IS NULL
                                            """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            tableNULL = tableNULL.fetchall()

            table1 = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, final_price, status, Users.username, Admins.username  FROM Lots
                                        INNER JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                        INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                        INNER JOIN Users 
                                            ON Auction_history.winner_id = Users.user_id
                                        WHERE Lots.end_time < '{dt_now}' AND seller_id == {r[0][0]}  """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table1 = table1.fetchall()

            table1NULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, status, username  FROM Lots
                                        INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id
                                        INNER JOIN Admins 
                                                ON Lots.seller_id = Admins.admin_id
                                        LEFT JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        WHERE Lots.end_time < '{dt_now}' AND seller_id == {r[0][0]} AND Auction_history.lot_id IS NULL""")
            table1NULL = table1NULL.fetchall()

            return [table, tableNULL, table1, table1NULL]

    # Функция для заполнения таблицы история торгов 
    def AddTradingHistory_db(self):
        with self.con:
            table = self.con.execute(f"""SELECT bid_id, Bids.lot_id, description, image_pt, username, starting_price, bid_amount FROM Bids
                                            INNER JOIN Lots 
                                                ON Bids.lot_id = Lots.lot_id
                                            INNER JOIN Lot_images
                                                ON Lots.lot_id = Lot_images.lot_id 
                                            INNER JOIN Users 
                                                ON Bids.user_id = Users.user_id""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table = table.fetchall()
            return [table]

    # Функция для заполнения таблицы история торгов после нажатой кнопки поиск      
    def salesSearch_db(self, textSearch, combo):
        with sql.connect(db_path) as self.con:
            if combo == 'Описание':
                table = self.con.execute(f"""SELECT bid_id, Bids.lot_id, description, image_pt, username, starting_price, bid_amount FROM Bids
                                                INNER JOIN Lots 
                                                    ON Bids.lot_id = Lots.lot_id
                                                INNER JOIN Lot_images
                                                    ON Lots.lot_id = Lot_images.lot_id 
                                                INNER JOIN Users 
                                                    ON Bids.user_id = Users.user_id
                                                WHERE description LIKE '%{textSearch}%'   """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
                table = table.fetchall()
                return [table]
            elif combo == 'Номер лота':
                table = self.con.execute(f"""SELECT bid_id, Bids.lot_id, description, image_pt, username, starting_price, bid_amount FROM Bids
                                                INNER JOIN Lots 
                                                    ON Bids.lot_id = Lots.lot_id
                                                INNER JOIN Lot_images
                                                    ON Lots.lot_id = Lot_images.lot_id 
                                                INNER JOIN Users 
                                                    ON Bids.user_id = Users.user_id
                                                WHERE Bids.lot_id = '{textSearch}'   """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
                table = table.fetchall()
                return [table]
            else:
                table = self.con.execute(f"""SELECT bid_id, Bids.lot_id, description, image_pt, username, starting_price, bid_amount FROM Bids
                                                INNER JOIN Lots 
                                                    ON Bids.lot_id = Lots.lot_id
                                                INNER JOIN Lot_images
                                                    ON Lots.lot_id = Lot_images.lot_id 
                                                INNER JOIN Users 
                                                    ON Bids.user_id = Users.user_id
                                                WHERE username = '{textSearch}'   """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
                table = table.fetchall()
                return [table]

    # Функция добавления значений в сам файл SQL
    def add_user_db(self, data):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""INSERT INTO Users (username, role_id, balance, successful_bids, auto_bid_access, is_banned)
                              values('{data[0]}', 1, {data[1]}, {data[2]}, {data[3]}, {data[4]})""")  # Происходит дабовления строки в SQL Таблицу

    def add_user_A_db(self, data):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""INSERT INTO Admins (username, password, balance, role_id,  commission_rate, penalties)
                              values('{data[0]}', '{data[1]}', {data[2]}, {data[3]}, {data[4]}, {data[5]})""")  # Происходит дабовления строки в SQL Таблицу

    def delete_User_db(self, d):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""DELETE FROM Users  
                                     WHERE username = '{d[0]}' and balance = {d[1]} and successful_bids = {d[2]}""")  # Удаляем строчку по индексу чс базы данных

    def delete_Admin_db(self, d):
        with self.con:
            self.con.execute(f"""DELETE FROM Admins  
                                     WHERE username = '{d[0]}' and password = '{d[1]}' and balance = {d[2]}""")  # Удаляем строчку по индексу чс базы данных

    def search_db(self, pe, p):
       with sql.connect(db_path) as self.con:
            if pe[0] == 1:
                r = self.con.execute(f"""SELECT user_id FROM Users
                                                WHERE username = '{p[0]}' and balance = {p[2]} and successful_bids = {p[3]}""")
                r = r.fetchall()
                self.con.execute(f"""UPDATE Users
                                            SET successful_bids = {pe[1]}, auto_bid_access = {pe[2]}, is_banned = {pe[3]}
                                            WHERE user_id = {r[0][0]}""")  # Редактируем данные ячейки
            else:
                self.con.execute(f"""INSERT INTO Admins (username, password, balance, role_id,  commission_rate, penalties)
                              values('{p[0]}', '{pe[4]}', {p[2]}, {pe[0]}, {5}, {0})""")

    def edit_Admin_db(self, p, d):
        with sql.connect(db_path) as self.con:
            r = self.con.execute(f"""SELECT admin_id FROM Admins
                                                WHERE username = '{d[0]}'  and balance = {d[3]} and commission_rate = {d[4]} and penalties == {d[5]}""")
            r = r.fetchall()

            self.con.execute(f"""UPDATE Admins
                                            SET username = '{p[0]}', password == '{p[1]}', role_id = {p[2]}, commission_rate = {p[3]}, penalties = {p[4]}
                                            WHERE admin_id = {r[0][0]}""")  # Редактируем данные ячейки

    def edit_MW1_db(self, p):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""UPDATE Lots
                                        SET description = '{p[1]}', starting_price = {p[3]}, start_time == '{p[4]}', end_time = '{p[5]}'
                                        WHERE lot_id = {p[0]}""")  # Редактируем данные ячейки  

            self.con.execute(f"""UPDATE Lot_images
                                        SET image_pt = '{p[2]}'
                                        WHERE lot_id = {p[0]}""")  # Редактируем данные ячейки

    def edit_MW2_db(self, p):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""UPDATE Lots
                                        SET description = '{p[1]}', starting_price = {p[3]}
                                        WHERE lot_id = {p[0]}""")  # Редактируем данные ячейки

            self.con.execute(f"""UPDATE Lot_images
                                        SET image_pt = '{p[2]}'
                                        WHERE lot_id = {p[0]}""")  # Редактируем данные ячейки

    def findProduct_db(self, id):
        r = self.con.execute(f"""SELECT title, description, location, starting_price, seller_id, start_time, end_time FROM Lots
                                                WHERE lot_id = {id} """)
        r = r.fetchall()
        return [r[0]]

    def addItemToAuction(self, pe):
        with self.con:
            self.con.execute(f"""INSERT INTO Lots (title, description, location, starting_price, seller_id, start_time, end_time, document_type, status)
                              values('{pe[1]}', '{pe[2]}', '{pe[3]}', {pe[4]}, {pe[0]}, '{pe[5]}', '{pe[6]}', '{pe[7]}', 'В процессе') """)  # Происходит дабовления строки в SQL Таблицу

            self.con.execute(f"""INSERT INTO Lot_images SELECT NULL, '{pe[8]}', MAX(lot_id) + 1 FROM Lot_images
                               """)  # Происходит дабовления строки в SQL Табл

    def administratorInformation_db(self, username):
        Information = self.con.execute(f"""SELECT admin_id, username, balance, commission_rate, penalties FROM Admins
                                                WHERE username = '{username}' """)
        Information = Information.fetchall()
        return Information[0]
    
    def lotTime(self):
        dt_now = (datetime.datetime.now())  # Определяем текущее время
        with sql.connect(db_path) as self.con:
            t = self.con.execute(f"""SELECT lot_id, min(end_time) FROM Lots 
                                        WHERE Lots.end_time > '{dt_now}' """)
            t = t.fetchall()
            return t
        
    def history(self, id):
        with sql.connect(db_path) as self.con:
            Information = self.con.execute(f"""SELECT Bids.user_id, max(bid_amount), bid_time, user_tg_id, balance FROM Bids 
                                                    INNER JOIN Users 
                                                        ON Bids.user_id = Users.user_id
                                                    WHERE Bids.lot_id = {id} """)
            Information = Information.fetchall()[0]

            self.con.execute(f"""INSERT INTO Auction_history (lot_id, winner_id, final_price, completion_time)
                                    values({id}, {Information[0]}, {Information[1]}, '{Information[2]}') """)  # Происходит дабовления строки в SQL Таблицу
            
            return Information
        
    def write_offOfFunds(self, bal, id):
        with sql.connect(db_path) as self.con:
            self.con.execute(f"""UPDATE Users
                                        SET balance = '{bal}'
                                        WHERE user_id = {id}""")  # Редактируем данные ячейки
    
    # Отменяем последнюю ставку 
    def cancelBid_db(self, id):
        with sql.connect(db_path) as self.con:
            bet = self.con.execute(f"""SELECT max(bid_amount) FROM Bids
                                            WHERE lot_id = {id}""")
            bet = bet.fetchall()[0][0]
            if bet != None:
                self.con.execute(f"""DELETE FROM Bids  
                                    WHERE lot_id = {id} and bid_amount = {bet}""")  # Удаляем строчку по индексу чс базы данных
                
    # Продлеваем определенным товаром время на торгах (После сбоя)
    def bidsRecovery_db(self, startOfTimeRange , endOfTimeRange):
        with sql.connect(db_path) as self.con:
            bet = self.con.execute(f"""SELECT lot_id FROM Lots
                                            WHERE end_time > '{startOfTimeRange}' AND end_time < '{endOfTimeRange}' """)
            bet = bet.fetchall()

            for id in bet:
                dt_now  = datetime.datetime.now() # Узнаем какое время сейчас
                end_time = dt_now  + datetime.timedelta(days=1) # Добавляем к текущему времени один день
                end_time = end_time.strftime('%Y-%m-%d %H:%M') # Переводим время в строковый формат данного типа 
                self.con.execute(f"""UPDATE Lots
                                        SET end_time = '{end_time}'
                                        WHERE lot_id = {id[0]}""")  # Редактируем данныеячейки
            # 2024-10-30 09:00                 
        



    
    def add_auto_bids(self):
        with self.con:
            self.con.execute(f"""INSERT INTO Auto_bids (lot_id, user_id, max_bid, current_bid)
                              values(9, 1, 20000, 400)""")  # Происходит дабовления строки в SQL Таблицу
            
    def delete_qqqqqqq(self):
        with self.con:
            #self.con.execute(f"""DELETE FROM Auto_bids  """)
            self.con.execute(f"""DELETE FROM Auction_history
                                    WHERE lot_id = 10  
                                     """)
    
db = Database()

data_db = {
    "roles": [
        ("user", '{"create_bid": true, "view_lots": true}'),
        ("admin", '{"create_lot": true, "view_all_lots": true, "manage_bids": true}'),
        ("root", '{"manage_users": true, "manage_admins": true, "view_all_finances": true}'),
    ],
    "users": [
        ("ivanov", 1434208032, 1, 1000.50, 5, 0, 0),
        ("petrov", 1434208032, 1, 2000.00, 2, 1, 0),
        ("sidorov", 1434208032, 1, 1500.75, 3, 0, 0),
        ("fedorov", 1434208032, 1, 500.25, 1, 1, 0),
        ("kuznetsov", 1434208032, 1, 1200.00, 4, 0, 0),
        ("ivanova", 1434208032, 1, 3000.00, 6, 1, 0),
        ("petrova", 1434208032, 1, 800.80, 0, 0, 0),
    ],
    "admins": [
        ("admin1", "12345678", 0, 2, 5.0, 2),
        ("admin", "root", 850, 3, 2.0, 0),
    ],
    "lot_images": [
        ('tg1', "http://example.com/images/painting.jpg", 1),
        ('tg2', "http://example.com/images/watches.jpg", 2),
        ('tg3', "http://example.com/images/spoon.jpg", 3),
        ('tg4', "http://example.com/images/statue.jpg", 4),
        ('tg5', "http://example.com/images/book.jpg", 5),
        ('tg6', "http://example.com/images/coin.jpg", 6),
        ('tg7', "http://example.com/images/vase.jpg", 7),
    ],
    "lots": [
        ("Картина", "Красивая картина маслом.", 'Moscow', 1500.00, 1, "2024-10-24 10:00", "2024-10-30 10:00",
         "Стандартный", "Продан"),
        ("Часы", "Стильные наручные часы.", 'Minsk', 750.50, 2, "2024-10-24 10:00", "2024-10-30 10:00", "Ювелирный",
         "Продан"),
        ("Серебряная ложка", "Ложка из чистого серебра.", 'Vitebsk', 250.00, 2, "2024-10-24 10:00", "2024-11-02 10:00",
         "Стандартный", "Продан"),
        ("Статуэтка", "Статуэтка ручной работы.", 'Grodno', 300.00, 1, "2024-10-24 10:00", "2024-11-05 10:00",
         "Историч ценный", "Продан"),
        ("Книга", "Редкое издание книги.", 'Praga', 500.00, 1, "2024-10-24 10:00", "2024-11-01 10:00", "Стандартный",
         "Продан"),
        (
        "Монета", "Антикварная монета.", 'Berlin', 1200.00, 1, "2024-10-24 10:00", "2024-10-30 10:00", "Историч ценный",
        "Продан"),
        ("Ваза", "Стеклянная ваза ручной работы.", 'Moscow', 400.00, 2, "2024-10-24 10:00", "2024-11-03 10:00",
         "Стандартный", "Продан"),
    ],
    "bids": [
        (1, 1, 1550.00),
        (1, 2, 1600.00),
        (2, 3, 800.00),
        (3, 4, 260.00),
        (4, 5, 310.00),
        (5, 6, 550.00),
        (6, 7, 1300.00),
    ],
    "auction_history": [
        (1, 2, 1600.00),
        (2, 3, 850.00),
        (3, 4, 280.00),
        (4, 5, 350.00),
        (5, 6, 600.00),
        (6, 7, 1350.00),
        (7, 1, 420.00),
    ],
    "complaints_strikes": [
        (1, 1, "Проблема с ответами", "в ожидании", 0),
        (2, 1, "Неудовлетворительное обслуживание", "в ожидании", 0),
        (3, 2, "Игнорирование вопросов", "в ожидании", 0),
        (4, 2, "Запоздалые ответы", "в ожидании", 0),
        (5, 3, "Неправильная информация", "в ожидании", 0),
        (6, 3, "Недостаток помощи", "в ожидании", 0),
        (7, 1, "Проблема с оплатой", "в ожидании", 0),
    ],
    "strikes": [
        (1, 1, "Несоблюдение правил"),
        (2, 1, "Проблема с оплатой"),
        (3, 2, "Нарушение условий аукциона"),
        (4, 2, "Некорректное поведение"),
        (5, 1, "Нарушение тайны торгов"),
        (6, 1, "Отсутствие уважения к другим"),
        (7, 2, "Задержка с подачей заявок"),
    ],
    "transfer_documents": [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 1),
    ]
}



# db.clear_data()
# db.delete_table()
# db.create_table()
# db.fill_table(data_db)

#db.add_auto_bids()
#db.delete_qqqqqqq()
