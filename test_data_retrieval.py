#!/usr/bin/env python3
"""
Test Data Retrieval Script for ResQSense
This script tests if data can be retrieved from the database
"""

import requests
import json

def test_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing ResQSense API Endpoints")
    print("=" * 50)
    
    # Test 1: Stats endpoint
    print("\n📊 Testing /stats endpoint...")
    try:
        response = requests.get(f"{base_url}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats endpoint working: {data}")
        else:
            print(f"❌ Stats endpoint failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")
    
    # Test 2: Data endpoint for each node
    nodes = ["node_1", "node_2", "node_3"]
    for node in nodes:
        print(f"\n📡 Testing /data endpoint for {node}...")
        try:
            response = requests.get(f"{base_url}/data?node={node}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success' and data['data']:
                    print(f"✅ {node}: Found {len(data['data'])} data points")
                    if data['data']:
                        latest = data['data'][0]
                        print(f"   Latest: Temp={latest.get('temperature', 'N/A')}°C, "
                              f"Humidity={latest.get('humidity', 'N/A')}%")
                else:
                    print(f"⚠️ {node}: No data found")
            else:
                print(f"❌ {node}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {node}: Error - {e}")
    
    # Test 3: Latest data for all nodes
    print(f"\n🌐 Testing /api/latest_data_all_nodes endpoint...")
    try:
        response = requests.get(f"{base_url}/api/latest_data_all_nodes", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success' and data['data']:
                print(f"✅ Found latest data for {len(data['data'])} nodes:")
                for node_id, node_data in data['data'].items():
                    print(f"   {node_id}: Temp={node_data.get('temperature', 'N/A')}°C, "
                          f"Humidity={node_data.get('humidity', 'N/A')}%")
            else:
                print("⚠️ No latest data found")
        else:
            print(f"❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_endpoints()
