from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('test_db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/vulnerable-query', methods=['POST'])
def vulnerable_query():
    user_input = request.json['input']  # external input from user
    conn = get_db_connection()
    
    # Vulnerable query - SQL Injection (due to direct user input in the query)
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    result = conn.execute(query).fetchall()
    conn.close()

    return jsonify([dict(row) for row in result])

@app.route('/safe-query-int', methods=['GET'])
def safe_query_int():
    user_id = int(request.args.get('id'))  # input is a number
    conn = get_db_connection()
    
    # Safe query - the external input is an integer
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = conn.execute(query).fetchall()
    conn.close()

    return jsonify([dict(row) for row in result])

@app.route('/safe-query-constant', methods=['GET'])
def safe_query_constant():
    fixed_username = 'admin'  # constant value
    conn = get_db_connection()
    
    # Safe query - the value is constant
    query = f"SELECT * FROM users WHERE username = '{fixed_username}'"
    result = conn.execute(query).fetchall()
    conn.close()

    return jsonify([dict(row) for row in result])

if __name__ == '__main__':
    app.run(port=3000)
