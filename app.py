from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from modules.chatbot import get_chatbot_response, store_chat_message, get_chat_history
from modules.auth import register_user, login_user
from modules.products import list_product, get_products, place_order

app = Flask(__name__)
app.secret_key = "farmfair_secret_key_2025"

# Database initialization
def init_db():
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, farmer_id INTEGER, name TEXT, price REAL, quantity INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, buyer_id INTEGER, quantity INTEGER, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, sender TEXT, message TEXT, user_id INTEGER)''')
    conn.commit()
    conn.close()

# Mock news and price data
MOCK_NEWS = [
    {"title": "Tomato Prices Surge in Rayalaseema", "content": "Due to low supply, tomato prices hit ₹80/kg."},
    {"title": "New Subsidy for Farmers", "content": "Govt announces ₹5000/ha for organic farming."}
]
MOCK_PRICES = [
    {"product": "Tomato", "price": 80, "unit": "kg"},
    {"product": "Onion", "price": 50, "unit": "kg"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    role = session["role"]
    error = None
    
    # Chatbot handling
    if request.method == "POST" and "message" in request.form:
        user_input = request.form["message"]
        response = get_chatbot_response(user_input, user_id)
        store_chat_message("You", user_input, user_id)
        store_chat_message("Jarvis", response, user_id)
    
    # Product listing
    if request.method == "POST" and "product_name" in request.form:
        name = request.form["product_name"]
        price = float(request.form["product_price"])
        quantity = int(request.form["product_quantity"])
        list_product(user_id, name, price, quantity)
    
    # Order placement
    if request.method == "POST" and "order_product_id" in request.form:
        product_id = int(request.form["order_product_id"])
        quantity = int(request.form["order_quantity"])
        try:
            place_order(product_id, user_id, quantity)
        except ValueError as e:
            error = str(e)
    
    chat_history = get_chat_history(user_id)
    products = get_products()
    return render_template("index.html", chat_history=chat_history, products=products, 
                         news=MOCK_NEWS, prices=MOCK_PRICES, role=role, error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = login_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("index"))
        return render_template("index.html", login_error="Invalid credentials", show_login=True)
    return render_template("index.html", show_login=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        try:
            register_user(username, password, role)
            return redirect(url_for("login"))
        except ValueError as e:
            return render_template("index.html", register_error=str(e), show_register=True)
    return render_template("index.html", show_register=True)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("role", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)