from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

# Database connection setup (Replace with Supabase connection details)
DB_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DB_URL)

@app.route("/api/deposit", methods=["POST"])
def deposit():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    if not user_id or not amount:
        return jsonify({"error": "Missing parameters"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET sol_balance = sol_balance + %s WHERE id = %s", (amount, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Deposit successful", "amount": amount}), 200

@app.route("/api/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT sol_balance FROM users WHERE id = %s", (user_id,))
    balance = cur.fetchone()[0]

    if balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    cur.execute("UPDATE users SET sol_balance = sol_balance - %s WHERE id = %s", (amount, user_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Withdrawal successful", "amount": amount}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
