from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY, 
                       item TEXT, 
                       amount REAL, 
                       month TEXT,
                       date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       descrption TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS income
                      (id INTEGER PRIMARY KEY, 
                       source TEXT, 
                       amount REAL, 
                       month TEXT,
                       date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       descrption TEXT)''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()

    if request.method == "POST":
        item = request.form["item"]
        amount = request.form["amount"]
        month = request.form["month"]
        cursor.execute("INSERT INTO expenses (item, amount, month) VALUES (?, ?, ?)", (item, amount, month))
        conn.commit()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    total_spent = sum(float(exp[2]) for exp in expenses)

    return render_template("index.html", expenses=expenses, total_spent=total_spent)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
