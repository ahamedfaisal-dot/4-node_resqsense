#!/usr/bin/env python3
"""
Simple test script to verify ResQSense data flow
"""

import requests
import json
import time

def send_test_data():
    """Send test data to verify the system"""
    
    # Test data
    test_data = {
        "node_id": "node_1",
        "Temperature": 25.5,
        "Humidity": 65.0,
        "MQ4": 250,
        "MQ5": 350,
        "MQ135": 450,
        "MQ7": 180,
        "Sound": 45,
        "Fire": 0,
        "Vibration": 0,
        "Pressure": 101325,
        "Acceleration": {
            "x": 1.2,
            "y": -0.8,
            "z": 9.8
        }
    }
    
    try:
        # Send data
        response = requests.post(
            "http://localhost:5000/data",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Test data sent successfully!")
            print(f"   Temperature: {test_data['Temperature']}°C")
            print(f"   Humidity: {test_data['Humidity']}%")
            print(f"   MQ4: {test_data['MQ4']} ppm")
            return True
        else:
            print(f"❌ Failed to send data: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending data: {e}")
        return False

def main():
    print("🧪 ResQSense Simple Test")
    print("=" * 30)
    
    # Send test data
    if send_test_data():
        print("\n📊 Check your browser at http://localhost:5000")
        print("   Look for the test data in the charts!")
        print("   Check browser console (F12) for debug messages")
    else:
        print("\n❌ Test failed. Check if the server is running.")

if __name__ == "__main__":
    main()

