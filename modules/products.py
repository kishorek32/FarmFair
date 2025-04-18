import sqlite3

def list_product(farmer_id, name, price, quantity):
    if price <= 0 or quantity <= 0:
        raise ValueError("Price and quantity must be positive")
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (farmer_id, name, price, quantity) VALUES (?, ?, ?, ?)", 
              (farmer_id, name, price, quantity))
    conn.commit()
    conn.close()

def get_products():
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute("SELECT id, name, price, quantity FROM products WHERE quantity > 0")
    products = [{"id": row[0], "name": row[1], "price": row[2], "quantity": row[3]} for row in c.fetchall()]
    conn.close()
    return products

def place_order(product_id, buyer_id, quantity):
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    result = c.fetchone()
    if not result:
        conn.close()
        raise ValueError("Product not found")
    available = result[0]
    if quantity <= 0 or quantity > available:
        conn.close()
        raise ValueError("Invalid quantity")
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
    c.execute("INSERT INTO orders (product_id, buyer_id, quantity, status) VALUES (?, ?, ?, ?)", 
              (product_id, buyer_id, quantity, "Pending"))
    conn.commit()
    conn.close()