import sqlite3
from datetime import datetime
import ollama

def get_chatbot_response(user_input, user_id):
    try:
        response = ollama.chat(
            model="deepseek-r1:7b",
            messages=[
                {"role": "system", "content": "You’re Jarvis, a friendly AI assistant for FarmFair. Help farmers, retailers, and consumers with queries about farming, products, or prices. Respond concisely with a warm tone."},
                {"role": "user", "content": user_input}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Oops, something went wrong: {str(e)}"

def store_chat_message(sender, message, user_id):
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO chat_history (timestamp, sender, message, user_id) VALUES (?, ?, ?, ?)", 
              (timestamp, sender, message, user_id))
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect("database/chatbot.db")
    c = conn.cursor()
    c.execute("SELECT sender, message FROM chat_history WHERE user_id = ? ORDER BY id DESC LIMIT ?", 
              (user_id, limit))
    history = c.fetchall()
    conn.close()
    return history[::-1]