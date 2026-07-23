import sqlite3

db_path = 'data/ecommerce_ai.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Set specific product names and categories to ensure search works for common terms
cursor.execute("UPDATE products SET category = 'Mobiles', name = 'iPhone 15 Pro' WHERE product_id % 10 = 1")
cursor.execute("UPDATE products SET category = 'Mobiles', name = 'Samsung Galaxy S24' WHERE product_id % 10 = 2")
cursor.execute("UPDATE products SET category = 'Electronics', name = 'MacBook Air M2' WHERE product_id % 10 = 3")
cursor.execute("UPDATE products SET category = 'Appliances', name = 'LG Smart Washer' WHERE product_id % 10 = 4")
cursor.execute("UPDATE products SET category = 'Furniture', name = 'Ergonomic Office Chair' WHERE product_id % 10 = 5")
cursor.execute("UPDATE products SET category = 'Daily Needs', name = 'Organic Rice 5kg' WHERE product_id % 10 = 6")
cursor.execute("UPDATE products SET category = 'Sports', name = 'Adidas Running Shoes' WHERE product_id % 10 = 7")
cursor.execute("UPDATE products SET category = 'Beauty', name = 'Maybelline Lip Gloss' WHERE product_id % 10 = 8")
cursor.execute("UPDATE products SET category = 'Fashion', name = 'Zara Slim Fit Jeans' WHERE product_id % 10 = 9")
cursor.execute("UPDATE products SET category = 'Home Decor', name = 'Minimalist Floor Lamp' WHERE product_id % 10 = 0")

conn.commit()
conn.close()
print("Database updated with search-friendly names and categories.")
