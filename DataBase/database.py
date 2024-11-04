import sqlite3 as sql
import os
from PyQt5 import QtCore
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'my_database.db')


def item_is_not_editable(table):
    for row in range(table.rowCount() - 1):
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if item is not None:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)


class Database:
    def __init__(self):
        self.con = sql.connect(db_path)

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
                quantity INTEGER NOT NULL,
                location VARCHAR(50) NOT NULL
                )
                ''')
            self.con.execute('''
                CREATE TABLE IF NOT EXISTS Product_images (
                image_tg VARCHAR(40),
                image_pt VARCHAR(255) NOT NULL,
                product_id INTEGER,
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
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
                status VARCHAR(20) CHECK(status IN ('В процессе', 'Продан', 'Не продан')) DEFAULT 'В процессе',
                FOREIGN KEY (product_id) REFERENCES Products(product_id),
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

    def get_data(self, table, name_table, data):
        for item in data[name_table]:
            self.con.execute(table, item)

    def fill_table(self, data):
        sql_insert_roles = "INSERT INTO Roles (role_name, permissions) values(?, ?)"
        sql_insert_users = "INSERT INTO Users (username, role_id, balance, successful_bids, auto_bid_access, is_banned) values(?, ?, ?, ?, ?, ?)"
        sql_insert_admins = "INSERT INTO Admins (username, password, balance, role_id, commission_rate, penalties) values(?, ?, ?, ?, ?, ?)"
        sql_insert_products = "INSERT INTO Products (title, description, price, quantity, location) values(?, ?, ?, ?, ?)"
        sql_insert_product_images = "INSERT INTO Product_images (image_tg, image_pt, product_id) values(?, ?, ?)"
        sql_insert_lots = "INSERT INTO Lots (product_id, starting_price, seller_id, start_time, end_time, document_type, status) values(?, ?, ?, ?, ?, ?, ?)"
        sql_insert_bids = "INSERT INTO Bids (lot_id, user_id, bid_amount) values(?, ?, ?)"
        sql_insert_auction_history = "INSERT INTO Auction_history (lot_id, winner_id, final_price) values(?, ?, ?)"
        sql_insert_complaints_strikes = "INSERT INTO Complaints_strikes (complainant_id, target_admin_id, reason, status, strike_count) values(?, ?, ?, ?, ?)"
        sql_insert_strikes = "INSERT INTO Strikes (user_id, admin_id, reason) values(?, ?, ?)"
        sql_insert_transfer_documents = "INSERT INTO Transfer_documents (lot_id, buyer_id) values(?, ?)"

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

    def get_admin_data(self):
        data = self.con.execute('''
            SELECT a.username, a.password, r.role_name, a.balance, a.commission_rate, a.penalties
            FROM Admins a
            JOIN Roles r ON a.role_id = r.role_id
        ''')
        data = data.fetchall()
        return data

    def get_product_data(self):
        data = self.con.execute('''
            SELECT p.title, p.description, p.price, p.quantity, p.location, i.image_pt
            FROM Product_images i
            JOIN Products p ON i.product_id = p.product_id
        ''')
        data = data.fetchall()
        return data

    def get_id_product(self, title, description):
        title = f'{title}'
        description = f'{description}'
        query = '''
            SELECT product_id 
            FROM Products 
            WHERE title = ? AND description = ?'''
        data = self.con.execute(query, (title, description)).fetchone()
        return data[0]

    def create_lot(self, product_id, starting_price, seller_id, start_time, end_time, document_type, status):
        sql_insert_lots = "INSERT OR IGNORE INTO Lots (product_id, starting_price, seller_id, start_time, end_time, document_type, status) values(?, ?, ?, ?, ?, ?, ?)"
        self.con.execute(sql_insert_lots,
                         [product_id, starting_price, seller_id, start_time, end_time, document_type, status])
        self.con.commit()

    def add_product(self, title, description, price, quantity, location):
        sql_insert_products = "INSERT INTO Products (title, description, price, quantity, location) values(?, ?, ?, ?, ?)"
        self.con.execute(sql_insert_products,
                         [title, description, price, quantity, location])
        self.con.commit()
    def add_product_image(self, image_pt, product_id):
        sql_insert_product_images = "INSERT INTO Product_images (image_pt, product_id) values(?, ?)"
        self.con.execute(sql_insert_product_images,
                         [image_pt, product_id])
        self.con.commit()

    def update_product(self, product_id, title, description, price, quantity, location):
        query = """UPDATE Products 
                   SET title = ?, description = ?, price = ?, quantity = ?, location = ? 
                   WHERE product_id = ?"""
        self.con.execute(query, (title, description, price, quantity, location, product_id))
        self.con.commit()

    def update_product_image(self, image_path, product_id):
        query = """UPDATE Product_images 
                   SET image_pt = ? 
                   WHERE product_id = ?"""
        self.con.execute(query, (image_path, product_id))
        self.con.commit()
    def delete_product_and_images(self, product_id):

        self.con.execute("BEGIN TRANSACTION")

        delete_images_query = """DELETE FROM Product_images WHERE product_id = ?"""
        self.con.execute(delete_images_query, (product_id,))

        delete_product_query = """DELETE FROM Products WHERE product_id = ?"""
        self.con.execute(delete_product_query, (product_id,))

        self.con.commit()
        self.con.rollback()

    def add_delete(self, n, u):  # t - индекс товара по выделенной ячейки; u - номер нажатой кнопки
        if u == 8:
            dt_now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            with self.con:
                self.con.execute(f"""UPDATE Lots
                                    SET end_time = '{dt_now}'
                                    WHERE lot_id = {n} """)

        elif u == 11:
            dt_now = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
            with self.con:
                self.con.execute(f"""UPDATE Lots
                                    SET end_time = '{dt_now}'
                                    WHERE lot_id = {n} """)

    # Заполнение таблицы товаров на аукционе
    def Auction(self):
        dt_now = (datetime.datetime.now())  # Определяем текущее время
        with self.con:
            table = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, MAX(bid_amount), start_time, end_time FROM Lots
                                            INNER JOIN Products 
                                                ON Lots.product_id = Products.product_id
                                            INNER JOIN Product_images 
                                                ON Lots.product_id = Product_images.product_id
                                            INNER JOIN Bids 
                                                ON Lots.lot_id = Bids.lot_id
                                            WHERE Lots.end_time > '{dt_now}'
                                            GROUP BY Bids.lot_id""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table = table.fetchall()

            tableNULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, start_time, end_time FROM Lots
                                            INNER JOIN Products 
                                                ON Lots.product_id = Products.product_id
                                            INNER JOIN Product_images 
                                                ON Lots.product_id = Product_images.product_id
                                            LEFT JOIN Bids 
                                                ON Bids.lot_id = Lots.lot_id
                                            WHERE Lots.end_time > '{dt_now}' AND Bids.lot_id IS NULL
                                            """)  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            tableNULL = tableNULL.fetchall()
            
            table1 = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, final_price, status, username  FROM Lots
                                        INNER JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        INNER JOIN Products 
                                            ON Lots.product_id = Products.product_id
                                        INNER JOIN Product_images 
                                            ON Lots.product_id = Product_images.product_id
                                        INNER JOIN Users 
                                            ON Auction_history.winner_id = Users.user_id
                                        WHERE Lots.end_time < '{dt_now}'""")  # выводим данные из базы данных для заполнения таблицы (товары которые участвуют в аукционе)
            table1 = table1.fetchall()

            table1NULL = self.con.execute(f"""SELECT Lots.lot_id, description, image_pt, starting_price, status  FROM Lots
                                        INNER JOIN Products 
                                            ON Lots.product_id = Products.product_id
                                        INNER JOIN Product_images 
                                            ON Lots.product_id = Product_images.product_id
                                        LEFT JOIN Auction_history 
                                            ON Lots.lot_id = Auction_history.lot_id
                                        WHERE Lots.end_time < '{dt_now}'AND Auction_history.lot_id IS NULL""")
            table1NULL = table1NULL.fetchall()
            print(table1NULL)
            return [table, tableNULL, table1, table1NULL]

# Функция добавления значений в сам файл SQL               
    def add_user_db(self, data):
        with self.con:
            self.con.execute(f"""INSERT INTO Users (username, role_id, balance, successful_bids, auto_bid_access, is_banned)
                              values('{data[0]}', 1, {data[1]}, {data[2]}, {data[3]}, {data[4]})""") # Происходит дабовления строки в SQL Таблицу  

    def delete_User_db(self, d):
        with self.con:
                self.con.execute(f"""DELETE FROM Users  
                                     WHERE username = '{d[0]}' and balance = {d[1]} and successful_bids = {d[2]}""")  # Удаляем строчку по индексу чс базы данных  
    def edit_User_db(self, p, d):
        with self.con:
                r = self.con.execute(f"""SELECT user_id FROM Users
                                            WHERE username = '{d[0]}' and balance = {d[2]} and successful_bids = {d[3]}""") 
                r = r.fetchall()
                
                self.con.execute(f"""UPDATE Users
                                        SET username = '{p[0]}', balance = {p[2]}, successful_bids = {p[3]}, auto_bid_access = {p[4]}, is_banned = {p[5]}
                                        WHERE user_id = {r[0][0]}""")  # Редактируем данные ячейки      
db = Database()


data_db = {
    "roles": [
        ("user", '{"create_bid": true, "view_lots": true}'),
        ("admin", '{"create_lot": true, "view_all_lots": true, "manage_bids": true}'),
        ("root", '{"manage_users": true, "manage_admins": true, "view_all_finances": true}'),
    ],
    "users": [
        ("ivanov", 1, 1000.50, 5, 0, 0),
        ("petrov", 1, 2000.00, 2, 1, 0),
        ("sidorov", 1, 1500.75, 3, 0, 0),
        ("fedorov", 1, 500.25, 1, 1, 0),
        ("kuznetsov", 1, 1200.00, 4, 0, 0),
        ("ivanova", 1, 3000.00, 6, 1, 0),
        ("petrova", 1, 800.80, 0, 0, 0),
    ],
    "admins": [
        ("admin1", "12345678", 0, 2, 5.0, 2),
        ("admin", "root", 850, 3, 2.0, 0),
    ],
    "products": [
        ("Картина", "Красивая картина маслом.", 1500.00, 1, 'Moscow'),
        ("Часы", "Стильные наручные часы.", 750.50, 5, 'Minsk'),
        ("Серебряная ложка", "Ложка из чистого серебра.", 250.00, 10, 'Vitebsk'),
        ("Статуэтка", "Статуэтка ручной работы.", 300.00, 2, 'Grodno'),
        ("Книга", "Редкое издание книги.", 500.00, 3, 'Praga'),
        ("Монета", "Антикварная монета.", 1200.00, 1, 'Berlin'),
        ("Ваза", "Стеклянная ваза ручной работы.", 400.00, 4, 'Moscow'),
    ],
    "product_images": [
        ('tg1', "http://example.com/images/painting.jpg", 1),
        ('tg2', "http://example.com/images/watches.jpg", 2),
        ('tg3', "http://example.com/images/spoon.jpg", 3),
        ('tg4', "http://example.com/images/statue.jpg", 4),
        ('tg5', "http://example.com/images/book.jpg", 5),
        ('tg6', "http://example.com/images/coin.jpg", 6),
        ('tg7', "http://example.com/images/vase.jpg", 7),
    ],
    "lots": [
        (1, 1500.00, 1, "2024-10-24 10:00:00", "2024-10-30 10:00:00", "Стандартный", "В процессе"),
        (2, 750.50, 2, "2024-10-24 10:00:00", "2024-10-30 10:00:00", "Ювелирный", "В процессе"),
        (3, 250.00, 2, "2024-10-24 10:00:00", "2024-11-29 10:00:00", "Стандартный", "В процессе"),
        (4, 300.00, 2, "2024-10-24 10:00:00", "2024-11-30 10:00:00", "Историч ценный", "В процессе"),
        (5, 500.00, 1, "2024-10-24 10:00:00", "2024-11-30 10:00:00", "Стандартный", "В процессе"),
        (6, 1200.00, 1, "2024-10-24 10:00:00", "2024-10-30 10:00:00", "Историч ценный", "В процессе"),
        (7, 400.00, 2, "2024-10-24 10:00:00", "2024-11-30 10:00:00", "Стандартный", "В процессе"),
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
