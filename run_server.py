#!/usr/bin/env python3
"""
Windows-Compatible ResQSense Server
This script runs the Flask server without WebSocket issues on Windows
"""

import os
import sys
from app import app, init_db

def main():
    """Main server function"""
    try:
        # Initialize database
        print("🗄️ Initializing database...")
        init_db()
        print("✅ Database initialized successfully!")
        
        print("\n🚀 Starting ResQSense Server...")
        print("📡 Server will be available at http://localhost:5000")
        print("⚠️ Note: WebSocket features are temporarily disabled for Windows compatibility")
        print("📊 HTTP API endpoints are fully functional")
        print("\n🔄 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run Flask app directly (without SocketIO for now)
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Make sure no other process is using port 5000")
        print("💡 Try: netstat -ano | findstr :5000")

if __name__ == "__main__":
    main()
