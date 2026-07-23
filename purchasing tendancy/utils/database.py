import sqlite3
import pandas as pd
import os

# Database Configuration
# In a real MySQL setup, you would use mysql.connector
# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'ecommerce_ai'
# }

class Database:
    def __init__(self, db_path="data/ecommerce_ai.db"):
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def get_connection(self):
        # Fallback to SQLite if MySQL is not available for this environment
        # To use MySQL, uncomment the mysql.connector logic
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create Tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'seller', 'buyer')) NOT NULL,
            location TEXT,
            email TEXT
        )'''.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER,
            seller_id INTEGER,
            FOREIGN KEY (seller_id) REFERENCES users(user_id)
        )'''.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            timestamp TEXT,
            quantity INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )'''.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_behavior (
            behavior_id INTEGER PRIMARY KEY AUTO_INCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            action TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )'''.replace('AUTO_INCREMENT', 'AUTOINCREMENT'))
        
        conn.commit()

    def populate_from_csv(self, data_dir="data"):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Clear existing data to prevent IntegrityError on re-runs
        cursor.execute("DELETE FROM user_behavior")
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM users")
        
        # Load and insert users
        users_df = pd.read_csv(os.path.join(data_dir, "users.csv"))
        users_df.to_sql('users', conn, if_exists='append', index=False)
        
        # Load and insert products
        products_df = pd.read_csv(os.path.join(data_dir, "products.csv"))
        products_df.to_sql('products', conn, if_exists='append', index=False)
        
        # Load and insert transactions
        trans_df = pd.read_csv(os.path.join(data_dir, "transactions.csv"))
        trans_df.to_sql('transactions', conn, if_exists='append', index=False)
        
        # Load and insert behavior
        beh_df = pd.read_csv(os.path.join(data_dir, "user_behavior.csv"))
        beh_df.to_sql('user_behavior', conn, if_exists='append', index=False)
        
        conn.commit()

    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def add_user(self, username, password, role, location='Unknown', email=None):
        if not email:
            email = f"{username}@example.com"
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role, location, email) VALUES (?, ?, ?, ?, ?)",
                       (username, password, role, location, email))
        conn.commit()

    def get_next_user_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(user_id) FROM users")
        res = cursor.fetchone()[0]
        return (res + 1) if res else 1

if __name__ == "__main__":
    db = Database()
    db.populate_from_csv()
    print("Database initialized and populated from CSV.")
