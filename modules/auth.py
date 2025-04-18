import sqlite3

def register_user(username, password, role):
    if role not in ["farmer", "retailer", "consumer"]:
        raise ValueError("Invalid role")
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                  (username, password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("Username already exists")
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", 
              (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "role": user[1]}
    return None