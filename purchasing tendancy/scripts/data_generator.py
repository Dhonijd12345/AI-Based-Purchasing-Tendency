import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_USERS = 500
NUM_PRODUCTS = 100
NUM_TRANSACTIONS = 5000
CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur"]
CATEGORIES = ["Electronics", "Fashion", "Home Decor", "Beauty", "Groceries", "Books", "Sports"]

def generate_users(num_users):
    users = []
    users.append({
        'user_id': 1,
        'username': 'dhoni',
        'password': '098765',
        'role': 'admin',
        'location': random.choice(CITIES),
        'email': 'dhoni@example.com'
    })
    for i in range(2, num_users + 1):
        role = random.choices(['buyer', 'seller', 'admin'], weights=[0.85, 0.1, 0.05])[0]
        users.append({
            'user_id': i,
            'username': f"user_{i}",
            'password': f"pass_{i}", # In production, this would be hashed
            'role': role,
            'location': random.choice(CITIES),
            'email': f"user_{i}@example.com"
        })
    return pd.DataFrame(users)

def generate_products(num_products, seller_ids):
    products = []
    for i in range(1, num_products + 1):
        products.append({
            'product_id': i,
            'name': f"Product_{i}",
            'category': random.choice(CATEGORIES),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'stock': random.randint(10, 500),
            'seller_id': random.choice(seller_ids)
        })
    return pd.DataFrame(products)

def generate_transactions(num_transactions, user_ids, product_ids):
    transactions = []
    start_date = datetime.now() - timedelta(days=90)
    for i in range(1, num_transactions + 1):
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        timestamp = start_date + timedelta(seconds=random.randint(0, 90 * 24 * 3600))
        transactions.append({
            'transaction_id': i,
            'user_id': user_id,
            'product_id': product_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'quantity': random.randint(1, 5)
        })
    return pd.DataFrame(transactions)

def generate_behavior(num_records, user_ids, product_ids):
    behaviors = []
    actions = ['view', 'search', 'add_to_cart', 'purchase']
    # Higher weights for view/search, lower for purchase
    weights = [0.5, 0.3, 0.15, 0.05]
    start_date = datetime.now() - timedelta(days=90)
    for i in range(1, num_records + 1):
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        action = random.choices(actions, weights=weights)[0]
        timestamp = start_date + timedelta(seconds=random.randint(0, 90 * 24 * 3600))
        behaviors.append({
            'behavior_id': i,
            'user_id': user_id,
            'product_id': product_id,
            'action': action,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return pd.DataFrame(behaviors)

if __name__ == "__main__":
    print("Generating synthetic data...")
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    df_users = generate_users(NUM_USERS)
    seller_ids = df_users[df_users['role'] == 'seller']['user_id'].tolist()
    buyer_ids = df_users[df_users['role'] == 'buyer']['user_id'].tolist()
    
    df_products = generate_products(NUM_PRODUCTS, seller_ids)
    product_ids = df_products['product_id'].tolist()
    
    df_transactions = generate_transactions(NUM_TRANSACTIONS, buyer_ids, product_ids)
    df_behaviors = generate_behavior(NUM_TRANSACTIONS * 2, buyer_ids, product_ids)
    
    # Save to CSV
    df_users.to_csv(f"{data_dir}/users.csv", index=False)
    df_products.to_csv(f"{data_dir}/products.csv", index=False)
    df_transactions.to_csv(f"{data_dir}/transactions.csv", index=False)
    df_behaviors.to_csv(f"{data_dir}/user_behavior.csv", index=False)
    
    print(f"Data saved to {data_dir}")
