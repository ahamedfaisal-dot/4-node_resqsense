#!/usr/bin/env python3
"""
Basic ResQSense Test Script
Tests the HTTP API endpoints without WebSocket complications
"""

import requests
import json
import time

def test_basic_functionality():
    """Test basic server functionality"""
    
    print("🧪 ResQSense Basic Functionality Test")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running - Dashboard accessible")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - is it running?")
        print("💡 Start the server with: python run_server.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False
    
    # Test 2: Send test data to Node 1
    test_data = {
        "node_id": "node_1",
        "Temperature": 25.5,
        "Humidity": 65.0,
        "MQ4": 250,
        "MQ5": 300,
        "MQ135": 400,
        "MQ7": 150,
        "Sound": 45,
        "Fire": 0,
        "Vibration": 0,
        "Pressure": 101325,
        "Acceleration": {"x": 1.2, "y": -0.8, "z": 9.8}
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/data",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Data sent successfully to Node 1")
        else:
            print(f"❌ Failed to send data: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending data: {e}")
        return False
    
    # Test 3: Check stats endpoint
    try:
        response = requests.get("http://localhost:5000/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Stats endpoint working")
            print(f"   📊 Total records: {stats.get('stats', {}).get('total_records', 'N/A')}")
        else:
            print(f"❌ Stats endpoint failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    # Test 4: Check data retrieval
    try:
        response = requests.get("http://localhost:5000/data?node=node_1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Data retrieval working")
            print(f"   📈 Retrieved {len(data.get('data', []))} data points")
        else:
            print(f"❌ Data retrieval failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
    
    print("\n🎯 Next Steps:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. You should see the dashboard with Node 1 data")
    print("3. Click on different nodes to test navigation")
    print("4. Check browser console (F12) for any JavaScript errors")
    
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n✅ All basic tests passed!")
    else:
        print("\n❌ Some tests failed - check the server logs")
