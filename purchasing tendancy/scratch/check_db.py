import sqlite3
import os

db_path = 'data/ecommerce.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    print(f"Products: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"Users: {cursor.fetchone()[0]}")
    conn.close()
