#!/usr/bin/env python3
"""
Node Navigation Test Script for ResQSense
This script tests the multi-node functionality by sending data to different nodes
"""

import requests
import json
import time

def send_node_data(node_id, data):
    """Send data to a specific node"""
    try:
        response = requests.post(
            "http://localhost:5000/data",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ Node {node_id}: Data sent successfully")
            return True
        else:
            print(f"❌ Node {node_id}: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Node {node_id}: Error - {e}")
        return False

def test_node_navigation():
    """Test sending data to different nodes"""
    
    print("🧪 ResQSense Node Navigation Test")
    print("=" * 50)
    
    # Test data for Node 1
    node1_data = {
        "node_id": "node_1",
        "Temperature": 25.0,
        "Humidity": 60.0,
        "MQ4": 200,
        "MQ5": 300,
        "MQ135": 400,
        "MQ7": 150,
        "Sound": 45,
        "Fire": 0,
        "Vibration": 0,
        "Pressure": 101325,
        "Acceleration": {"x": 1.2, "y": -0.8, "z": 9.8}
    }
    
    # Test data for Node 2
    node2_data = {
        "node_id": "node_2",
        "Temperature": 28.0,
        "Humidity": 70.0,
        "MQ4": 500,
        "MQ5": 600,
        "MQ135": 300,
        "MQ7": 250,
        "Sound": 55,
        "Fire": 0,
        "Vibration": 1,
        "Pressure": 101400,
        "Acceleration": {"x": -0.5, "y": 1.8, "z": 9.9}
    }
    
    # Test data for Node 3
    node3_data = {
        "node_id": "node_3",
        "Temperature": 30.0,
        "Humidity": 65.0,
        "MQ4": 800,
        "MQ5": 400,
        "MQ135": 600,
        "MQ7": 350,
        "Sound": 65,
        "Fire": 1,
        "Vibration": 0,
        "Pressure": 101500,
        "Acceleration": {"x": 2.1, "y": -1.2, "z": 9.7}
    }
    
    print("📡 Sending data to Node 1...")
    send_node_data("node_1", node1_data)
    time.sleep(2)
    
    print("📡 Sending data to Node 2...")
    send_node_data("node_2", node2_data)
    time.sleep(2)
    
    print("📡 Sending data to Node 3...")
    send_node_data("node_3", node3_data)
    time.sleep(2)
    
    print("\n🎯 Testing Instructions:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Click on 'Node 1' - you should see Temperature: 25°C, Humidity: 60%")
    print("3. Click on 'Node 2' - you should see Temperature: 28°C, Humidity: 70%")
    print("4. Click on 'Node 3' - you should see Temperature: 30°C, Humidity: 65%")
    print("5. Check browser console (F12) for debug messages")
    
    print("\n📊 Expected Results:")
    print("• Each node should show different data")
    print("• Charts should update when switching nodes")
    print("• Node status indicators should show 'Online'")
    print("• Mining map should highlight the active node")

if __name__ == "__main__":
    test_node_navigation()
