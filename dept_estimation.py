import sqlite3
from flask import Flask, request, jsonify, render_template, g

# --- App and Database Setup ---
app = Flask(__name__)
DATABASE = 'sensor_data.db'

def setup_database():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            front INTEGER NOT NULL,
            right INTEGER NOT NULL,
            back INTEGER NOT NULL,
            left INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database is ready. ✅")

# Helper function to get the database connection for a request
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Return rows as dictionaries
    return db

# Close the database connection automatically after each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- API Routes ---

# Route to receive POST data from your sensor
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    print(f"Received: {data}")

    db = get_db()
    db.execute(
        'INSERT INTO readings (front, right, back, left) VALUES (?, ?, ?, ?)',
        (data.get('front'), data.get('right'), data.get('back'), data.get('left'))
    )
    db.commit()
    return jsonify({"status": "ok"}), 200

# Route to provide the last 20 readings to the frontend
@app.route('/get_data', methods=['GET'])
def get_data():
    cursor = get_db().execute('SELECT * FROM readings ORDER BY id DESC LIMIT 20')
    readings = cursor.fetchall()
    return jsonify([dict(row) for row in readings])

# --- Frontend Route ---

# Route to serve the main dashboard page
@app.route('/')
def index():
    return render_template('map.html')

# --- Main Execution ---
if __name__ == '__main__':
    setup_database() # Ensure the database is set up before running
    app.run(host='0.0.0.0', port=5000, debug=True)