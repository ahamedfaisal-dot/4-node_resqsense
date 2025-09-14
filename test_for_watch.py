from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import json

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Define the database model for sensor data
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accelerometer_x = db.Column(db.Float)
    accelerometer_y = db.Column(db.Float)
    accelerometer_z = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)
    spo2 = db.Column(db.Integer)
    button = db.Column(db.Integer)
    buzzer = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'accelerometer': {
                'x': self.accelerometer_x,
                'y': self.accelerometer_y,
                'z': self.accelerometer_z
            },
            'heart_rate': self.heart_rate,
            'spo2': self.spo2,
            'button': self.button,
            'buzzer': self.buzzer
        }

# Create the database tables
with app.app_context():
    db.create_all()

# Serve the main HTML page
@app.route('/')
def index():
    """Serves the main HTML page for the dashboard."""
    return render_template('watch.html')

# Define a route that accepts POST requests for sensor data
@app.route('/watchdata', methods=['POST'])
def receive_data():
    """Receives and processes sensor data from the ESP8266."""
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    print("Received data:", data)

    # Store data in the database
    try:
        new_data = SensorData(
            accelerometer_x=data.get('accelerometer', {}).get('x'),
            accelerometer_y=data.get('accelerometer', {}).get('y'),
            accelerometer_z=data.get('accelerometer', {}).get('z'),
            heart_rate=data.get('heart_rate'),
            spo2=data.get('spo2'),
            button=data.get('button'),
            buzzer=data.get('buzzer')
        )
        db.session.add(new_data)
        db.session.commit()
    except Exception as e:
        print(f"Error saving to database: {e}")
        db.session.rollback()
        return jsonify({"status": "error", "message": "Failed to save data"}), 500

    # Emit the data to all connected WebSocket clients
    socketio.emit('sensor_update', data)
    
    return jsonify({"status": "success", "message": "Data received"}), 201

# WebSocket connection handler
@socketio.on('connect')
def handle_connect():
    """Handles a new WebSocket connection."""
    print('Client connected')
    # Send last 20 records on connect
    try:
        recent_data = SensorData.query.order_by(SensorData.id.desc()).limit(20).all()
        recent_data.reverse()
        emit('initial_data', [d.to_dict() for d in recent_data])
    except Exception as e:
        print(f"Error fetching initial data: {e}")


@socketio.on('disconnect')
def handle_disconnect():
    """Handles a WebSocket disconnection."""
    print('Client disconnected')

# Run the Flask app
if __name__ == '__main__':
    # Use host='0.0.0.0' to make the server accessible from any device on your network
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
