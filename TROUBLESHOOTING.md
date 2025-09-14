# ResQSense Troubleshooting Guide

## 🚨 **Data Not Visualizing? Here's How to Fix It**

### **Problem**: Charts are empty, no real-time data updates

### **Root Cause**: Database schema mismatch and node_id format issues

---

## 🔧 **Step-by-Step Fix**

### **1. Reset the Database**
```bash
# Stop the server (Ctrl+C)
python reset_database.py
```

### **2. Restart the Server**
```bash
python app.py
```

**Expected Output:**
```
Database initialized successfully!
Created new sensor_data table with node_id support
```

### **3. Test Data Flow**
```bash
# In a new terminal
python test_multi_node_client.py
```

**Expected Output:**
```
✅ Main Shaft - Level 1 (node_1): Data sent successfully
✅ East Tunnel - Level 2 (node_2): Data sent successfully  
✅ West Tunnel - Level 3 (node_3): Data sent successfully
```

### **4. Check Browser Console**
- Open http://localhost:5000
- Press F12 → Console tab
- Look for these messages:
  ```
  Received real-time data: {node_id: "node_1", ...}
  Normalized nodeId: node1
  Current activeNode: node_1
  Updating charts for active node: node1
  ```

---

## 🔍 **Debugging Steps**

### **Check Server Logs**
Look for these messages in the terminal running `app.py`:
```
Received data from node_1: {...}
Data stored successfully in database
```

### **Check Database Structure**
```bash
# In a new terminal
sqlite3 sensor_data.db
.schema sensor_data
```

**Expected Output:**
```sql
CREATE TABLE sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    mq4 REAL, mq5 REAL, mq135 REAL, mq7 REAL,
    temperature REAL, humidity REAL, sound REAL,
    fire INTEGER, vibration INTEGER, pressure REAL,
    acceleration_x REAL, acceleration_y REAL, acceleration_z REAL
);
```

### **Check WebSocket Connection**
In browser console, look for:
```
WebSocket connected
```

---

## 🚫 **Common Issues & Solutions**

### **Issue 1: "table sensor_data has no column named node_id"**
**Solution**: Run `python reset_database.py` and restart server

### **Issue 2: "Failed to store data in database"**
**Solution**: Check database permissions and disk space

### **Issue 3: Charts not updating**
**Solution**: 
1. Check WebSocket connection status (top-right corner)
2. Verify data is being received in console
3. Check if active node matches incoming data

### **Issue 4: Node switching not working**
**Solution**: 
1. Click on node cards or mining map points
2. Check console for navigation messages
3. Verify node data buffers are populated

---

## 📊 **Data Flow Verification**

### **Expected Data Structure**
```json
{
    "node_id": "node_1",
    "MQ4": 250,
    "MQ5": 300,
    "MQ135": 400,
    "MQ7": 150,
    "Temperature": 28.5,
    "Humidity": 65,
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
```

### **Data Flow Path**
```
Test Client → Flask Server → SQLite DB → WebSocket → Frontend Charts
    ↓              ↓              ↓           ↓           ↓
  node_1      POST /data    Store     Broadcast   Update
  node_2      node_id       Data      sensor_data Charts
  node_3      Processing    Success   Event       Real-time
```

---

## 🎯 **Quick Test Commands**

### **Test API Endpoint**
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node_1", "Temperature": 25, "Humidity": 60}'
```

### **Check Database Content**
```bash
sqlite3 sensor_data.db "SELECT node_id, temperature, humidity FROM sensor_data LIMIT 5;"
```

### **Test WebSocket Connection**
```bash
# In browser console
socket.connected  // Should return true
```

---

## 📱 **Frontend Debugging**

### **Check Active Node**
```javascript
// In browser console
console.log('Active Node:', activeNode);
console.log('Node Data:', nodeData);
```

### **Force Chart Update**
```javascript
// In browser console
updateCharts({Temperature: 25, Humidity: 60, timestamp: Date.now()});
```

### **Check Chart Objects**
```javascript
// In browser console
console.log('Charts:', charts);
console.log('Temperature Chart:', charts.temperature);
```

---

## 🆘 **Still Not Working?**

### **1. Check All Services**
- Flask server running on port 5000
- Test client sending data
- Browser console showing WebSocket connection
- Database file exists and has correct schema

### **2. Verify Network**
- No firewall blocking port 5000
- Localhost accessible
- WebSocket connection established

### **3. Check Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Restart Everything**
```bash
# Terminal 1: Stop server (Ctrl+C)
# Terminal 2: Stop test client (Ctrl+C)

# Terminal 1: Start server
python app.py

# Terminal 2: Start test client  
python test_multi_node_client.py

# Browser: Refresh page
```

---

## 📞 **Need More Help?**

1. Check the console logs for error messages
2. Verify the database schema matches expected structure
3. Ensure WebSocket connection is established
4. Confirm data is being sent and received
5. Check if charts are properly initialized

**Remember**: The system needs to receive data to populate charts. Start the test client to see real-time updates!
