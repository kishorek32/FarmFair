FarmFair
FarmFair is a mobile-optimized web application that connects farmers directly with retailers and consumers, eliminating middlemen to ensure fair pricing, enable fast transportation, provide a platform to sell farming products, and deliver daily farming news and price updates.
Features

Chatbot: Powered by DeepSeek-R1:7b (local AI model) to assist users with queries.
Authentication: Secure login/signup for farmers, retailers, and consumers.
Product Listing: Farmers can list products; retailers/consumers can browse and order.
Fair Pricing: Direct sales ensure farmers get better prices.
Fast Transportation: Mock logistics feature for estimated delivery times.
News and Updates: Daily farming news and price updates (mock data).

Setup

Prerequisites:
Python 3.10
Ollama with deepseek-r1:7b model
VS Code


Install Dependencies:cd E:\JARWIS\JARWIS
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt


Start Ollama:ollama serve
ollama pull deepseek-r1:7b


Run the App:python app.py

Open http://127.0.0.1:5000 in a mobile browser.
Test:
Register as a farmer, retailer, or consumer.
List a product (farmer), order a product (retailer/consumer), or chat with Jarvis.



Project Structure

app.py: Main Flask app.
static/: CSS and background image.
templates/: HTML templates.
modules/: Chatbot, auth, and product logic.
database/: SQLite database.
docs/: Constraints and screenshots.

Constraints
See docs/constraints.md for development constraints.
Screenshots

docs/screenshots/home.png: Homepage.
docs/screenshots/chatbot.png: Chatbot interface.

