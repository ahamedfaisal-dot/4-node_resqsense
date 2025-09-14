from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
DATABASE = 'sensor_data.db'

def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Check if the table exists and has the correct structure
    cursor.execute("PRAGMA table_info(sensor_data)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if not columns:
        # Create new table with correct structure
        cursor.execute('''
            CREATE TABLE sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL, 
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                mq4 REAL, mq5 REAL, mq135 REAL, mq7 REAL,
                temperature REAL, humidity REAL, sound REAL,
                fire INTEGER, vibration INTEGER, pressure REAL,
                acceleration_x REAL, acceleration_y REAL, acceleration_z REAL
            )
        ''')
        print("Created new sensor_data table with node_id support")
    elif 'node_id' not in columns:
        # Add node_id column to existing table
        cursor.execute('ALTER TABLE sensor_data ADD COLUMN node_id TEXT DEFAULT "node1"')
        print("Added node_id column to existing sensor_data table")
    
    conn.commit()
    conn.close()

def insert_sensor_data(data):
    """Insert sensor data into the database"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        acceleration = data.get('Acceleration', {})
        acc_x = acceleration.get('x', 0)
        acc_y = acceleration.get('y', 0)
        acc_z = acceleration.get('z', 0)
        
        # --- MODIFIED: Added node_id to the INSERT query ---
        cursor.execute('''
            INSERT INTO sensor_data (
                node_id, mq4, mq5, mq135, mq7, temperature, humidity, 
                sound, fire, vibration, pressure, 
                acceleration_x, acceleration_y, acceleration_z
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('node_id', 'unknown'), # Get the node_id from the JSON payload
            data.get('MQ4', 0), data.get('MQ5', 0), data.get('MQ135', 0),
            data.get('MQ7', 0), data.get('Temperature', 0), data.get('Humidity', 0),
            data.get('Sound', 0), data.get('Fire', 0), data.get('Vibration', 0),
            data.get('Pressure', 0), acc_x, acc_y, acc_z
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting data: {e}")
        return False

def broadcast_sensor_data(data):
    """Store data in database - WebSocket broadcasting removed for Windows compatibility"""
    # Data is stored in database, frontend will poll for updates
    pass

@app.route('/data', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Invalid data format: JSON required."}), 400
    
    data = request.get_json()
    # Log which node sent the data
    print(f"Received data from {data.get('node_id', 'Unknown Node')}:")
    print(data)
    
    if insert_sensor_data(data):
        print("Data stored successfully in database")
        broadcast_sensor_data(data)
        return jsonify({"status": "success", "message": "Data received and stored successfully!"}), 200
    else:
        print("Failed to store data in database")
        return jsonify({"status": "error", "message": "Data received but failed to store"}), 500

@app.route('/data', methods=['GET'])
def get_data():
    """Retrieve stored sensor data for a specific node with optional limit"""
    # --- MODIFIED: Filter data by node_id from a query parameter ---
    node_id = request.args.get('node')
    if not node_id:
        return jsonify({"status": "error", "message": "A 'node' query parameter is required (e.g., /data?node=node_1)"}), 400

    # Get limit parameter with default
    limit = request.args.get('limit', 50)
    try:
        limit = int(limit)
        limit = min(max(limit, 1), 100)  # Clamp between 1 and 100
    except ValueError:
        limit = 50

    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sensor_data 
            WHERE node_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (node_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Format data to match frontend expectations
        data = []
        for row in rows:
            data.append({
                'id': row['id'],
                'node_id': row['node_id'],
                'timestamp': row['timestamp'],
                'MQ4': row['mq4'],  # Match frontend expectations
                'MQ5': row['mq5'],
                'MQ135': row['mq135'],
                'MQ7': row['mq7'],
                'Temperature': row['temperature'],
                'Humidity': row['humidity'],
                'Sound': row['sound'],
                'Fire': row['fire'],
                'Vibration': row['vibration'],
                'Pressure': row['pressure'],
                'Acceleration': {
                    'x': row['acceleration_x'],
                    'y': row['acceleration_y'],
                    'z': row['acceleration_z']
                }
            })
        
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- NEW ENDPOINT: Get latest data for all nodes for the map view ---
@app.route('/api/latest_data_all_nodes', methods=['GET'])
def get_latest_data_all_nodes():
    """Get the single most recent data entry for each node."""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # This advanced SQL query gets the latest record for each node_id
        cursor.execute('''
            SELECT t1.*
            FROM sensor_data t1
            INNER JOIN (
                SELECT node_id, MAX(timestamp) as max_timestamp
                FROM sensor_data
                GROUP BY node_id
            ) t2 ON t1.node_id = t2.node_id AND t1.timestamp = t2.max_timestamp;
        ''')

        rows = cursor.fetchall()
        conn.close()

        # Create a dictionary where keys are node_ids
        data = {row['node_id']: dict(row) for row in rows}
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def dashboard():
    """Serve the dashboard HTML page"""
    return render_template('index.html')

@app.route('/stats')
def get_stats():
    """Get basic statistics about the stored data"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get total records
        cursor.execute('SELECT COUNT(*) as total FROM sensor_data')
        total_records = cursor.fetchone()['total']
        
        # Get average temperature and humidity
        cursor.execute('SELECT AVG(temperature) as avg_temp, AVG(humidity) as avg_humidity FROM sensor_data')
        avg_data = cursor.fetchone()
        avg_temperature = avg_data['avg_temp'] or 0
        avg_humidity = avg_data['avg_humidity'] or 0
        
        # Get latest timestamp
        cursor.execute('SELECT MAX(timestamp) as latest FROM sensor_data')
        latest_timestamp = cursor.fetchone()['latest']
        
        conn.close()
        
        stats = {
            'total_records': total_records,
            'average_temperature': round(avg_temperature, 1),
            'average_humidity': round(avg_humidity, 1),
            'latest_timestamp': latest_timestamp
        }
        
        return jsonify({"status": "success", "stats": stats}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# WebSocket handlers removed for Windows compatibility
# Frontend will use polling to get real-time updates

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    print("Database initialized successfully!")
    
    # Run the server with regular Flask (Windows compatible)
    try:
        print("🚀 Starting ResQSense Server...")
        print("📡 Server will be available at http://localhost:5000")
        print("📊 HTTP API endpoints are fully functional")
        print("🔄 Frontend will poll for real-time updates")
        
        # Use regular Flask for Windows compatibility
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try running with: python app.py")