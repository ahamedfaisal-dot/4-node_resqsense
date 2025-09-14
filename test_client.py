import requests
import json
import time
import random

# Flask server URL
SERVER_URL = "http://localhost:5000"

def send_sensor_data():
    """Send sample sensor data to the Flask server"""
    
    # Sample sensor data with varying gas levels to demonstrate safety thresholds
    sensor_data = {
        'MQ4': random.randint(200, 1200),      # Methane: 200-1200 ppm (will show NORMAL/WARNING/DANGER)
        'MQ5': random.randint(300, 900),       # LPG: 300-900 ppm (will show NORMAL/WARNING/DANGER)
        'MQ135': random.randint(250, 800),     # Air Quality: 250-800 ppm (will show NORMAL/WARNING/DANGER)
        'MQ7': random.randint(150, 500),       # CO: 150-500 ppm (will show NORMAL/WARNING/DANGER)
        'Temperature': round(random.uniform(20, 40), 1),
        'Humidity': random.randint(40, 80),
        'Sound': random.randint(0, 100),
        'Fire': random.choice([0, 1]),
        'Vibration': random.choice([0, 1]),
        'Pressure': random.randint(98000, 102000),
        'Acceleration': {
            'x': round(random.uniform(0.5, 3.0), 6),
            'y': round(random.uniform(0.5, 3.0), 6),
            'z': round(random.uniform(0.5, 3.0), 6)
        }
    }
    
    try:
        # Send POST request to the server
        response = requests.post(
            f"{SERVER_URL}/data",
            json=sensor_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"✅ Data sent successfully: {response.json()}")
            print(f"   MQ4 (Methane): {sensor_data['MQ4']} ppm")
            print(f"   MQ5 (LPG): {sensor_data['MQ5']} ppm")
            print(f"   MQ135 (Air): {sensor_data['MQ135']} ppm")
            print(f"   MQ7 (CO): {sensor_data['MQ7']} ppm")
        else:
            print(f"❌ Error sending data: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function to continuously send sensor data"""
    print("🚀 Starting underground mining sensor data simulation...")
    print(f"📡 Sending data to: {SERVER_URL}")
    print("🌐 Open http://localhost:5000 in your browser to see real-time charts!")
    print("⚠️  Watch for NORMAL/WARNING/DANGER status indicators on gas sensors")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            send_sensor_data()
            time.sleep(2)  # Send data every 2 seconds to see status changes
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping sensor data simulation...")

if __name__ == "__main__":
    main()
