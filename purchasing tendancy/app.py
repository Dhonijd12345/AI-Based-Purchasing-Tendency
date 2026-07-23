from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import numpy as np
from utils.database import Database
from utils.inference import InferenceService
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"

db = Database()
inference = InferenceService()

SEARCH_CATEGORY_HINTS = {
    'belt': 'Fashion',
    'belts': 'Fashion',
    'wallet': 'Fashion',
    'wallets': 'Fashion',
    'shoe': 'Fashion',
    'shoes': 'Fashion',
    'sandal': 'Fashion',
    'sandals': 'Fashion',
    'shirt': 'Fashion',
    'shirts': 'Fashion',
    'dress': 'Fashion',
    'dresses': 'Fashion',
    'bag': 'Fashion',
    'bags': 'Fashion',
    'phone': 'Mobiles',
    'phones': 'Mobiles',
    'mobile': 'Mobiles',
    'mobiles': 'Mobiles',
    'laptop': 'Electronics',
    'laptops': 'Electronics',
    'computer': 'Electronics',
    'tv': 'Electronics',
    'television': 'Electronics',
    'monitor': 'Electronics',
    'camera': 'Electronics',
    'chair': 'Furniture',
    'chairs': 'Furniture',
    'table': 'Furniture',
    'tables': 'Furniture',
    'sofa': 'Furniture',
    'sofas': 'Furniture',
    'lamp': 'Home Decor',
    'lamps': 'Home Decor',
    'decor': 'Home Decor',
    'fridge': 'Appliances',
    'refrigerator': 'Appliances',
    'washing': 'Appliances',
    'washer': 'Appliances',
    'microwave': 'Appliances',
    'book': 'Books',
    'books': 'Books',
    'novel': 'Books',
    'football': 'Sports',
    'cricket': 'Sports',
    'bat': 'Sports',
    'ball': 'Sports',
    'shampoo': 'Beauty',
    'cream': 'Beauty',
    'cosmetic': 'Beauty',
    'perfume': 'Beauty',
    'grocery': 'Groceries',
    'food': 'Groceries',
    'juice': 'Groceries',
    'milk': 'Groceries',
}


def _build_variant_products(query):
    q = (query or '').strip().lower()
    search_terms = [term for term in q.split() if term]
    if not search_terms:
        return []

    category = None
    for term in search_terms:
        if term in SEARCH_CATEGORY_HINTS:
            category = SEARCH_CATEGORY_HINTS[term]
            break

    if not category:
        return []

    if category == 'Fashion':
        if any(term in {'belt', 'belts'} for term in search_terms):
            items = [
                ('Classic Leather Belt', 'Levi\'s', 1299),
                ('Executive Formal Belt', 'Tommy Hilfiger', 1599),
                ('Casual Canvas Belt', 'Allen Solly', 949),
                ('Premium Reversible Belt', 'Hidesign', 1899),
                ('Metal Buckle Belt', 'Guess', 1399),
                ('Sporty Utility Belt', 'Puma', 1099),
            ]
        elif any(term in {'wallet', 'wallets'} for term in search_terms):
            items = [
                ('Premium Leather Wallet', 'Coach', 1999),
                ('Slim RFID Wallet', 'Tommy Hilfiger', 1599),
                ('Minimalist Card Holder', 'Hidesign', 1699),
                ('Travel Wallet', 'American Tourister', 1299),
            ]
        elif any(term in {'shoe', 'shoes', 'sandal', 'sandals'} for term in search_terms):
            items = [
                ('Running Sports Shoe', 'Nike', 3499),
                ('Formal Leather Shoe', 'Bata', 2799),
                ('Casual Slip-On Shoe', 'Adidas', 2599),
                ('Comfort Sandal', 'Crocs', 1999),
            ]
        else:
            items = [
                ('Premium Fashion Item', 'Zara', 1999),
                ('Contemporary Style Piece', 'H&M', 1599),
                ('Everyday Fashion Essential', 'Ray-Ban', 2499),
            ]
    elif category == 'Mobiles':
        items = [
            ('Smart Mobile Phone', 'Samsung', 24999),
            ('Premium Smartphone', 'Apple', 79999),
            ('Camera Phone', 'OnePlus', 32999),
        ]
    elif category == 'Electronics':
        items = [
            ('Slim Laptop', 'Dell', 54999),
            ('Smart TV', 'Sony', 49999),
            ('Digital Camera', 'Canon', 35999),
        ]
    elif category == 'Furniture':
        items = [
            ('Ergonomic Chair', 'Nilkamal', 7999),
            ('Modern Table', 'IKEA', 12999),
            ('Comfort Sofa', 'Urban Ladder', 28999),
        ]
    elif category == 'Home Decor':
        items = [
            ('Decorative Lamp', 'Home Centre', 3999),
            ('Elegant Wall Frame', 'Urban Ladder', 4999),
        ]
    elif category == 'Appliances':
        items = [
            ('Modern Refrigerator', 'Whirlpool', 34999),
            ('Smart Washing Machine', 'LG', 27999),
            ('Compact Microwave', 'Samsung', 12999),
        ]
    elif category == 'Sports':
        items = [
            ('Performance Sports Gear', 'Nivia', 2999),
            ('Training Kit', 'Adidas', 3999),
        ]
    elif category == 'Beauty':
        items = [
            ('Premium Shampoo', 'Dove', 799),
            ('Hydrating Cream', 'Nivea', 599),
            ('Luxury Perfume', 'Versace', 3499),
        ]
    elif category == 'Books':
        items = [
            ('Best Seller Book', 'Penguin', 799),
            ('Popular Novel', 'HarperCollins', 699),
        ]
    elif category == 'Groceries':
        items = [
            ('Fresh Juice', 'Tropicana', 199),
            ('Premium Milk', 'Amul', 99),
            ("Organic Food Pack", "Nature's Basket", 499),
        ]
    else:
        items = [(q.title(), 'Brand', 999)]

    result_list = []
    for idx, (name, brand, price) in enumerate(items):
        result_list.append({
            'product_id': 100000 + idx,
            'name': name,
            'category': category,
            'price': price,
            'stock': 100,
            'seller_id': 1,
            'display_name': name,
            'brand': brand,
        })
    return result_list


def _build_display_name(product, query=''):
    raw_name = (product.get('name') or '').strip()
    if raw_name and not raw_name.lower().startswith('product_'):
        return raw_name

    category = (product.get('category') or '').strip()
    q = (query or '').strip().lower()
    terms = [term for term in q.split() if term and term not in {'and', 'the', 'for', 'a', 'an'}]
    noun = None

    for term in terms:
        if term.lower() not in {'product', 'item', 'buy', 'shop', 'search', 'show'}:
            noun = term
            break

    if not noun and category:
        noun = category.lower()

    if category == 'Fashion':
        if noun in {'belt', 'belts'}:
            return 'Classic Leather Belt'
        if noun in {'wallet', 'wallets'}:
            return 'Premium Leather Wallet'
        if noun in {'shoe', 'shoes', 'sandal', 'sandals'}:
            return 'Stylish Casual Shoe'
        if noun in {'shirt', 'shirts'}:
            return 'Premium Cotton Shirt'
        if noun in {'dress', 'dresses'}:
            return 'Elegant Dress'
        if noun in {'bag', 'bags'}:
            return 'Trendy Handbag'
        return 'Premium Fashion Item'

    if category == 'Mobiles':
        if noun in {'phone', 'phones', 'mobile', 'mobiles'}:
            return 'Smart Mobile Phone'
        if noun in {'laptop', 'laptops'}:
            return 'Slim Laptop'
        return 'Modern Mobile Device'

    if category == 'Electronics':
        if noun in {'laptop', 'laptops'}:
            return 'Slim Laptop'
        if noun in {'tv', 'television'}:
            return 'Smart TV'
        if noun in {'camera'}:
            return 'Digital Camera'
        return 'Advanced Electronic Device'

    if category == 'Furniture':
        if noun in {'chair', 'chairs'}:
            return 'Ergonomic Chair'
        if noun in {'table', 'tables'}:
            return 'Modern Table'
        if noun in {'sofa', 'sofas'}:
            return 'Comfort Sofa'
        return 'Modern Furniture Piece'

    if category == 'Home Decor':
        if noun in {'lamp', 'lamps'}:
            return 'Decorative Lamp'
        return 'Elegant Home Decor Piece'

    if category == 'Appliances':
        if noun in {'fridge', 'refrigerator'}:
            return 'Modern Refrigerator'
        if noun in {'washing', 'washer'}:
            return 'Smart Washing Machine'
        if noun in {'microwave'}:
            return 'Compact Microwave'
        return 'Reliable Appliance'

    if category == 'Sports':
        if noun in {'football', 'cricket', 'bat', 'ball'}:
            return 'Performance Sports Gear'
        return 'Sporty Essentials'

    if category == 'Beauty':
        if noun in {'shampoo'}:
            return 'Premium Shampoo'
        if noun in {'cream'}:
            return 'Hydrating Cream'
        if noun in {'perfume'}:
            return 'Luxury Perfume'
        return 'Beauty Essentials'

    if category == 'Books':
        if noun in {'book', 'books', 'novel'}:
            return 'Best Seller Book'
        return 'Popular Book'

    if category == 'Groceries':
        if noun in {'juice'}:
            return 'Fresh Juice'
        if noun in {'milk'}:
            return 'Premium Milk'
        return 'Fresh Grocery Item'

    if noun:
        return f"Premium {noun.title()}"
    return f"Premium {category or 'Product'}"


def _enrich_products(rows, query=''):
    enriched = []
    for row in rows:
        product = dict(row)
        product['display_name'] = _build_display_name(product, query)
        enriched.append(product)
    return enriched


def _get_search_matches(cursor, query):
    q = (query or '').strip().lower()
    if not q:
        cursor.execute("SELECT * FROM products ORDER BY price DESC LIMIT 24")
        return [dict(row) for row in cursor.fetchall()]

    search_terms = [term for term in q.split() if term]
    variants = _build_variant_products(q)
    if variants:
        results = variants
    else:
        conditions = []
        params = []

        for term in search_terms:
            conditions.append("(lower(name) LIKE ? OR lower(category) LIKE ?)")
            like_term = f'%{term}%'
            params.extend([like_term, like_term])

        if conditions:
            cursor.execute(
                f"SELECT * FROM products WHERE {' OR '.join(conditions)} ORDER BY price DESC",
                params
            )
            results = [dict(row) for row in cursor.fetchall()]
        else:
            results = []

        if not results:
            hinted_category = None
            for term in search_terms:
                if term in SEARCH_CATEGORY_HINTS:
                    hinted_category = SEARCH_CATEGORY_HINTS[term]
                    break

            if hinted_category:
                cursor.execute(
                    "SELECT * FROM products WHERE lower(category) = ? ORDER BY price DESC",
                    (hinted_category.lower(),)
                )
                results = [dict(row) for row in cursor.fetchall()]

        if not results:
            cursor.execute("SELECT * FROM products ORDER BY price DESC LIMIT 12")
            results = [dict(row) for row in cursor.fetchall()]

    results = _enrich_products(results, query)

    enriched_results = []
    for product in results:
        name = (product.get('name') or '').lower()
        category = (product.get('category') or '').lower()
        match_label = 'Popular Picks'
        match_detail = 'Showing popular items for discovery'

        if q == name:
            match_label = 'Exact Match'
            match_detail = 'Perfect match in product name'
        elif q in name:
            match_label = 'Name Match'
            match_detail = 'Matched by product name'
        elif q in category:
            match_label = 'Category Match'
            match_detail = 'Matched by product category'
        elif any(term in category for term in search_terms):
            match_label = 'Related Match'
            match_detail = 'Related to your search term'
        elif any(term in name for term in search_terms):
            match_label = 'Related Match'
            match_detail = 'Related to your search term'

        product['match_label'] = match_label
        product['match_detail'] = match_detail
        enriched_results.append(product)

    return enriched_results

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login/buyer', methods=['GET'])
def login_buyer():
    return render_template('login_buyer.html')

@app.route('/login/seller', methods=['GET'])
def login_seller():
    return render_template('login_seller.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    role_choice = request.form.get('role', 'buyer')
    
    # Check Admin
    if role_choice == 'admin' or username == 'dhoni':
        if password == 'Nikile@63699':
            session['user_id'] = 0
            session['username'] = 'dhoni'
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        return render_template('login.html', error="Invalid Credentials")

    # Regular login
    user = db.get_user_by_username(username)
    if not user:
        db.add_user(username, 'none', role_choice)
        user = db.get_user_by_username(username)
        session['role'] = role_choice
    elif role_choice in ['buyer', 'seller'] and user['role'] != role_choice:
        # If user explicitly chooses a different role, update it in session (and could update in DB)
        # For now, we'll trust the choice for this session
        session['role'] = role_choice
    else:
        session['role'] = user['role']
    
    session['user_id'] = user['user_id']
    session['username'] = user['username']
    
    # Log the login behavior
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_behavior (user_id, product_id, action, timestamp) VALUES (?, NULL, 'login', ?)",
                       (user['user_id'], datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        print("Error logging login:", e)
    
    if session.get('role') == 'seller':
        return redirect(url_for('seller_dashboard'))
    return redirect(url_for('buyer_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard/buyer')
def buyer_dashboard():
    if 'user_id' not in session or session['role'] != 'buyer':
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    # Get recommendations
    recs = inference.get_recommendations(user_id)
    # Get user community
    community = inference.get_user_community(user_id)
    
    # Get product details for recommendations
    conn = db.get_connection()
    cursor = conn.cursor()
    recs_placeholders = ','.join(['?'] * len(recs))
    cursor.execute(f"SELECT * FROM products WHERE product_id IN ({recs_placeholders})", recs)
    recommended_products = cursor.fetchall()
    
    # Get all products for inventory (Increased limit for visibility)
    cursor.execute("SELECT * FROM products ORDER BY product_id DESC LIMIT 20")
    all_products = cursor.fetchall()
    
    return render_template('buyer_dashboard.html', 
                           user=session['username'], 
                           community=community,
                           recommendations=_enrich_products(recommended_products),
                           products=_enrich_products(all_products))

@app.route('/dashboard/seller')
def seller_dashboard():
    if 'user_id' not in session or session['role'] != 'seller':
        return redirect(url_for('index'))
        
    demand_data = inference.get_regional_demand()
    
    # Get seller products
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE seller_id = ?", (session['user_id'],))
    seller_products = cursor.fetchall()
    
    return render_template('seller_dashboard.html', 
                           user=session['username'], 
                           demand=demand_data,
                           products=seller_products)

@app.route('/dashboard/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
        
    # Get stats
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM transactions")
    trans_count = cursor.fetchone()['count']
    
    # Revenue data
    total_revenue = 0
    try:
        cursor.execute("SELECT SUM(p.price * t.quantity) as total_revenue FROM transactions t JOIN products p ON t.product_id = p.product_id")
        rev_row = cursor.fetchone()
        if rev_row and rev_row['total_revenue']:
            total_revenue = rev_row['total_revenue']
    except:
        pass

    # Recent Transactions
    recent_tx = []
    try:
        cursor.execute("""
            SELECT t.timestamp, u.username, p.name as product_name, p.price, t.quantity
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN products p ON t.product_id = p.product_id
            ORDER BY t.timestamp DESC LIMIT 7
        """)
        recent_tx = cursor.fetchall()
    except Exception as e:
        print("Error fetching recent tx:", e)
    
    # Community distribution
    communities = {}
    for i in range(inference.num_communities):
        communities[i] = int(np.sum(inference.user_communities == i))
        
    return render_template('admin_dashboard.html', 
                           user=session.get('username'),
                           user_count=user_count,
                           trans_count=trans_count,
                           total_revenue=total_revenue,
                           recent_tx=recent_tx,
                           communities=communities)

@app.route('/search')
def search():
    query = (request.args.get('q', '') or '').strip()
    conn = db.get_connection()
    cursor = conn.cursor()

    results = _get_search_matches(cursor, query)

    if query:
        recommended_products = []
    else:
        # Get high quality recommendations when browsing normally
        recs = inference.get_recommendations(session.get('user_id', 1), top_n=6)
        recs_placeholders = ','.join(['?'] * len(recs))
        cursor.execute(f"SELECT * FROM products WHERE product_id IN ({recs_placeholders})", recs)
        recommended_products = cursor.fetchall()

    return render_template('buyer_dashboard.html',
                           user=session.get('username'),
                           products=results,
                           recommendations=recommended_products,
                           community="All",
                           search_query=query,
                           no_results=False)

@app.route('/api/predict_demand', methods=['GET'])
def api_predict_demand():
    return jsonify(inference.get_regional_demand())

@app.route('/product/<int:product_id>')
def product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    prod = cursor.fetchone()
    
    if not prod:
        return redirect(url_for('buyer_dashboard'))
        
    # Log the view behavior for real-time intelligence
    try:
        cursor.execute("INSERT INTO user_behavior (user_id, product_id, action, timestamp) VALUES (?, ?, 'view', ?)",
                       (session['user_id'], product_id, datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        print("Error logging behavior:", e)
        
    # Getting related products for horizontal scroll section
    cursor.execute("SELECT * FROM products WHERE category = ? AND product_id != ? LIMIT 5", (prod['category'], product_id))
    related = cursor.fetchall()
    
    return render_template('product.html', product=prod, related=related)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session or session.get('role') != 'buyer':
        return redirect(url_for('index'))
    
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    
    return redirect(url_for('cart'))

@app.route('/buy_now/<int:product_id>')
def buy_now(product_id):
    if 'user_id' not in session or session.get('role') != 'buyer':
        return redirect(url_for('index'))
    
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    
    return redirect(url_for('checkout'))

@app.route('/cart')
def cart():
    if 'user_id' not in session or session.get('role') != 'buyer':
        return redirect(url_for('index'))
        
    cart_ids = session.get('cart', [])
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cart_items = []
    total = 0
    
    if cart_ids:
        placeholders = ','.join(['?'] * len(cart_ids))
        cursor.execute(f"SELECT * FROM products WHERE product_id IN ({placeholders})", cart_ids)
        products = cursor.fetchall()
        
        for p in products:
            qty = cart_ids.count(p['product_id'])
            subtotal = p['price'] * qty
            cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
            
    return render_template('cart.html', items=cart_items, total=total, user=session.get('username'))

@app.route('/checkout')
def checkout():
    if 'user_id' not in session or session.get('role') != 'buyer':
        return redirect(url_for('index'))
    
    # Process dummy checkout - clear the cart
    session['cart'] = []
    
    return render_template('checkout.html', user=session.get('username'))

@app.route('/admin/<section>')
def admin_section(section):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))
        
    template_name = f"admin_{section}.html"
    
    # Section specific data
    data = {}
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if section == 'users':
        cursor.execute("""
            SELECT u.*, 
                   (SELECT MAX(timestamp) FROM user_behavior WHERE user_id = u.user_id AND action = 'login') as last_login
            FROM users u
            ORDER BY last_login DESC, u.user_id DESC
        """)
        data['users_list'] = cursor.fetchall()
    elif section == 'inventory':
        cursor.execute("SELECT * FROM products")
        data['inventory_list'] = cursor.fetchall()
    elif section == 'ai_models':
        data['models'] = [
            {'name': 'Demand Predictor', 'status': 'Active', 'accuracy': '94%'},
            {'name': 'Customer Segmenter', 'status': 'Active', 'accuracy': '89%'},
            {'name': 'Price Optimizer', 'status': 'Training', 'accuracy': 'N/A'}
        ]
    elif section == 'analytics':
        data['metrics'] = {
            'daily_active': 150,
            'bounce_rate': '22%',
            'avg_session': '5m 12s'
        }

    try:
        return render_template(template_name, user=session.get('username'), **data)
    except Exception as e:
        print(f"Template {template_name} not found. Error: {e}")
        title = section.replace('_', ' ').title()
        return render_template('admin_placeholder.html', section_title=title, user=session.get('username'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('profile.html', user=session.get('username'))

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('settings.html', user=session.get('username'))

@app.route('/seller/post_ad', methods=['GET', 'POST'])
def seller_post_ad():
    if 'user_id' not in session or session.get('role') != 'seller':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock, seller_id) VALUES (?, ?, ?, ?, ?)",
                       (name, category, price, stock, session.get('user_id')))
        conn.commit()
        return redirect(url_for('seller_dashboard'))
    return render_template('seller_post_ad.html')

@app.route('/api/admin/live_stats')
def api_admin_live_stats():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    user_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM transactions")
    trans_count = cursor.fetchone()['count']
    
    total_revenue = 0
    try:
        cursor.execute("SELECT SUM(p.price * t.quantity) as total_revenue FROM transactions t JOIN products p ON t.product_id = p.product_id")
        rev_row = cursor.fetchone()
        if rev_row and rev_row['total_revenue']:
            total_revenue = rev_row['total_revenue']
    except:
        pass
        
    recent_activities = []
    
    # Get latest user behaviors (logins, views, etc)
    try:
        cursor.execute("""
            SELECT b.action, b.timestamp, u.username, p.name as product_name
            FROM user_behavior b
            JOIN users u ON b.user_id = u.user_id
            LEFT JOIN products p ON b.product_id = p.product_id
            ORDER BY b.behavior_id DESC LIMIT 4
        """)
        for b in cursor.fetchall():
            if b['action'] == 'login':
                recent_activities.append({
                    'title': 'User Access',
                    'desc': f"User '{b['username']}' initiated a session",
                    'time': 'Just now',
                    'icon': 'bi-box-arrow-in-right',
                    'color': 'info'
                })
            elif b['action'] == 'view':
                recent_activities.append({
                    'title': 'Intelligence Log',
                    'desc': f"User '{b['username']}' analyzed a product",
                    'time': 'Just now',
                    'icon': 'bi-eye-fill',
                    'color': 'primary'
                })
    except:
        pass
    
    # Try fetching latest transactions to prepend
    try:
        cursor.execute("""
            SELECT 'transaction' as type, t.timestamp, u.username, p.name as product_name
            FROM transactions t
            JOIN users u ON t.user_id = u.user_id
            JOIN products p ON t.product_id = p.product_id
            ORDER BY t.transaction_id DESC LIMIT 1
        """)
        for tx in cursor.fetchall():
            recent_activities.insert(0, {
                'title': 'Transaction Success',
                'desc': f"User '{tx['username']}' bought {tx['product_name'][:15]}...",
                'time': 'Just now',
                'icon': 'bi-check2-circle',
                'color': 'success'
            })
    except:
        pass

    communities = {}
    for i in range(inference.num_communities):
        communities[i] = int(np.sum(inference.user_communities == i))

    return jsonify({
        'user_count': user_count,
        'trans_count': trans_count,
        'total_revenue': total_revenue,
        'communities': len(communities),
        'activities': recent_activities
    })

@app.route('/api/admin/live_inventory_activity')
def api_admin_live_inventory_activity():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT b.action, b.timestamp, u.username, p.name as product_name, p.product_id
            FROM user_behavior b
            JOIN users u ON b.user_id = u.user_id
            JOIN products p ON b.product_id = p.product_id
            ORDER BY b.behavior_id DESC LIMIT 6
        """)
        activities = []
        for row in cursor.fetchall():
            activities.append({
                'action': row['action'],
                'username': row['username'],
                'product_name': row['product_name'],
                'product_id': row['product_id']
            })
        return jsonify({'activities': activities})
    except Exception as e:
        return jsonify({'activities': []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
