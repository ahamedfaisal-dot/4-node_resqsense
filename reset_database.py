#!/usr/bin/env python3
"""
Database Reset Script for ResQSense
This script deletes the old database and allows the application to recreate it with the correct schema
"""

import os
import sqlite3

DATABASE = 'sensor_data.db'

def reset_database():
    """Delete the existing database file"""
    try:
        if os.path.exists(DATABASE):
            os.remove(DATABASE)
            print(f"✅ Deleted existing database: {DATABASE}")
        else:
            print(f"ℹ️ Database file {DATABASE} does not exist")
        
        print("🔄 Database will be recreated with correct schema when you restart the application")
        print("📝 Run 'python app.py' to restart the server")
        
    except Exception as e:
        print(f"❌ Error deleting database: {e}")

if __name__ == "__main__":
    print("🗑️ ResQSense Database Reset Tool")
    print("=" * 40)
    reset_database()
    print("=" * 40)
    print("💡 Next steps:")
    print("1. Run 'python app.py' to restart the server")
    print("2. Run 'python test_multi_node_client.py' to test data flow")
    print("3. Open http://localhost:5000 in your browser")
