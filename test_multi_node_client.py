#!/usr/bin/env python3
"""
Multi-Node Sensor Data Simulator for ResQSense
Simulates real-time sensor data from 3 underground mining nodes
"""

import requests
import json
import time
import random
from datetime import datetime

# Server configuration
SERVER_URL = "http://localhost:5000/data"

# Node configurations
NODES = [
    {
        "id": "node_1",
        "name": "Main Shaft - Level 1",
        "location": "Central mining shaft, primary access point",
        "base_temp": 28,
        "base_humidity": 65
    },
    {
        "id": "node_2", 
        "name": "East Tunnel - Level 2",
        "location": "Eastern expansion tunnel, secondary access",
        "base_temp": 26,
        "base_humidity": 70
    },
    {
        "id": "node_3",
        "name": "West Tunnel - Level 3", 
        "location": "Western expansion tunnel, tertiary access",
        "base_temp": 30,
        "base_humidity": 60
    }
]

def generate_sensor_data(node_config):
    """Generate realistic sensor data for a specific node"""
    
    # Base values with realistic variations
    base_temp = node_config["base_temp"]
    base_humidity = node_config["base_humidity"]
    
    # Gas sensor readings (realistic for underground mining)
    mq4 = random.randint(150, 800)      # Methane: 150-800 ppm
    mq5 = random.randint(200, 600)      # LPG/Propane: 200-600 ppm  
    mq135 = random.randint(180, 500)    # Air Quality: 180-500 ppm
    mq7 = random.randint(80, 350)       # Carbon Monoxide: 80-350 ppm
    
    # Environmental sensors
    temperature = base_temp + random.uniform(-3, 3)
    humidity = base_humidity + random.uniform(-10, 10)
    
    # Safety sensors
    sound = random.randint(0, 80)       # Sound level: 0-80 dB
    fire = 1 if random.random() > 0.95 else 0  # 5% chance of fire detection
    vibration = 1 if random.random() > 0.90 else 0  # 10% chance of vibration
    
    # Pressure and acceleration
    pressure = random.randint(95000, 105000)  # Atmospheric pressure variation
    acceleration = {
        "x": random.uniform(-2, 2),
        "y": random.uniform(-2, 2), 
        "z": random.uniform(9.5, 10.5)  # Z-axis includes gravity
    }
    
    return {
        "node_id": node_config["id"],
        "MQ4": mq4,
        "MQ5": mq5, 
        "MQ135": mq135,
        "MQ7": mq7,
        "Temperature": round(temperature, 1),
        "Humidity": round(humidity, 1),
        "Sound": sound,
        "Fire": fire,
        "Vibration": vibration,
        "Pressure": pressure,
        "Acceleration": acceleration
    }

def send_node_data(node_config):
    """Send sensor data for a specific node to the server"""
    try:
        data = generate_sensor_data(node_config)
        
        # Send POST request to server
        response = requests.post(
            SERVER_URL,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ {node_config['name']} ({node_config['id']}): Data sent successfully")
            print(f"   📊 Gas: MQ4={data['MQ4']}, MQ5={data['MQ5']}, MQ135={data['MQ135']}, MQ7={data['MQ7']}")
            print(f"   🌡️ Environment: Temp={data['Temperature']}°C, Humidity={data['Humidity']}%")
            print(f"   ⚠️ Safety: Fire={data['Fire']}, Vibration={data['Vibration']}")
            print(f"   📍 Location: {node_config['location']}")
        else:
            print(f"❌ {node_config['name']}: Failed to send data - Status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {node_config['name']}: Network error - {e}")
    except Exception as e:
        print(f"❌ {node_config['name']}: Error - {e}")

def main():
    """Main function to run the multi-node sensor simulator"""
    print("🚀 ResQSense Multi-Node Sensor Data Simulator")
    print("=" * 60)
    print("Simulating 3 underground mining nodes with real-time data")
    print("Press Ctrl+C to stop the simulation")
    print("=" * 60)
    
    try:
        while True:
            print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)
            
            # Send data for all nodes
            for node in NODES:
                send_node_data(node)
                time.sleep(0.5)  # Small delay between nodes
            
            print(f"\n⏳ Waiting 3 seconds before next data transmission...")
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Simulation stopped by user")
        print("📊 Check the ResQSense dashboard to see the multi-node data visualization!")
        print("🌐 Dashboard URL: http://localhost:5000")

if __name__ == "__main__":
    main()
