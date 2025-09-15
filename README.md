# ResQSense - Underground Mining Safety Monitor

##  **Multi-Node Real-Time Sensor Monitoring System**

ResQSense is an advanced underground mining safety monitoring system that provides real-time visualization of sensor data from multiple mining nodes using WebSocket streaming and interactive 3D visualizations.

##  **Key Features**

###  **Multi-Node Support**
- **3 Active Mining Nodes**: Monitor multiple locations simultaneously
- **Node 1**: Main Shaft - Level 1 (Central access point)
- **Node 2**: East Tunnel - Level 2 (Eastern expansion)
- **Node 3**: West Tunnel - Level 3 (Western expansion)
- **Real-time Node Switching**: Click any node to view its specific data
- **Individual Data Storage**: Each node maintains separate data history

###  **Interactive Underground Mining Map**
- **3D Mining Layout**: Visual representation of underground structure
- **Surface Level**: Brown surface layer with main shaft access
- **Main Shaft**: Central vertical access tunnel
- **East & West Tunnels**: Horizontal expansion tunnels
- **Clickable Node Points**: Interactive nodes that navigate to specific data views
- **Real-time Status**: Visual indicators for each node's operational status

###  **Advanced Sensor Visualization**
- **Individual Gas Sensor Charts**: Separate monitoring for MQ4, MQ5, MQ135, MQ7
- **Temperature & Humidity**: Dedicated environmental monitoring
- **Fire & Vibration Detection**: Binary safety sensors with visual alerts
- **3D Acceleration Model**: Interactive 3D vector visualization
- **Sound & Pressure**: Combined environmental monitoring
- **Safety Thresholds**: Underground mining compliance standards

###  **Real-Time Communication**
- **WebSocket Streaming**: Instant data updates across all nodes
- **Multi-Node Data Handling**: Simultaneous data processing
- **Automatic Node Detection**: Smart data routing based on node_id
- **Connection Status Monitoring**: Real-time connection health indicators

##  **Technical Architecture**

### **Backend (Flask + SQLite)**
- **Multi-Node Database**: Separate data storage per node
- **RESTful API**: `/data` endpoint for data submission and retrieval
- **WebSocket Server**: Flask-SocketIO for real-time communication
- **Node-Aware Processing**: Automatic data routing and storage

### **Frontend (HTML5 + JavaScript)**
- **Responsive Design**: Mobile-friendly interface
- **Chart.js Integration**: Real-time chart updates
- **Three.js 3D Engine**: Interactive acceleration visualization
- **WebSocket Client**: Real-time data streaming
- **Node Navigation**: Seamless switching between mining nodes

### **Data Flow**
```
Sensor Nodes → Flask Backend → SQLite Database → WebSocket → Frontend Dashboard
     ↓              ↓              ↓              ↓           ↓
  Real-time    Data Storage   Historical    Broadcasting   Visualization
   Data        & Processing     Data         to Clients     & Alerts
```

##  **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Start the Server**
```bash
python app.py
```
Server will start at: `http://localhost:5000`

### **3. Run Multi-Node Simulator**
```bash
python test_multi_node_client.py
```

### **4. Access Dashboard**
Open your browser and navigate to: `http://localhost:5000`

##  **Dashboard Features**

### **Node Overview Section**
- **Interactive Node Cards**: Click to switch between nodes
- **Real-time Status**: Online/Offline indicators
- **Location Information**: Mining level and access details
- **Visual Feedback**: Hover effects and active state highlighting

### **Underground Mining Map**
- **Interactive Layout**: Click nodes to navigate to data views
- **Visual Hierarchy**: Surface, shaft, and tunnel representation
- **Node Positioning**: Accurate spatial representation
- **Legend System**: Color-coded node identification

### **Sensor Data Visualization**
- **Real-time Charts**: Live updates from active node
- **Safety Indicators**: Color-coded status (Normal/Warning/Danger)
- **Historical Data**: Rolling window of recent readings
- **Interactive Elements**: Hover tooltips and zoom capabilities

##  **Configuration**

### **Node Setup**
Each node should send data with the following structure:
```json
{
    "node_id": "node1",
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

### **Safety Thresholds**
- **MQ4 (Methane)**: Normal: 0-300 ppm, Warning: 300-1000 ppm, Danger: >1000 ppm
- **MQ5 (LPG/Propane)**: Normal: 0-400 ppm, Warning: 400-800 ppm, Danger: >800 ppm
- **MQ135 (Air Quality)**: Normal: 0-350 ppm, Warning: 350-700 ppm, Danger: >700 ppm
- **MQ7 (Carbon Monoxide)**: Normal: 0-200 ppm, Warning: 200-400 ppm, Danger: >400 ppm

##  **API Endpoints**

### **POST /data**
Submit sensor data from any node
```bash
curl -X POST http://localhost:5000/data \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node1", "Temperature": 28.5, ...}'
```

### **GET /data?node=node1**
Retrieve historical data for a specific node
```bash
curl "http://localhost:5000/data?node=node1"
```

### **GET /api/latest_data_all_nodes**
Get latest data from all nodes for overview
```bash
curl "http://localhost:5000/api/latest_data_all_nodes"
```

##  **Use Cases**

### **Underground Mining Safety**
- **Real-time Gas Monitoring**: Continuous air quality assessment
- **Environmental Control**: Temperature and humidity monitoring
- **Safety Alerts**: Fire and vibration detection
- **Multi-Location Monitoring**: Comprehensive site coverage

### **Industrial Applications**
- **Multi-Unit Monitoring**: Factory floor sensor networks
- **Environmental Compliance**: Air quality and safety standards
- **Predictive Maintenance**: Vibration and pressure analysis
- **Emergency Response**: Real-time alert systems

##  **Security Features**

- **CORS Enabled**: Cross-origin resource sharing for development
- **Input Validation**: JSON payload verification
- **Error Handling**: Graceful failure management
- **Connection Monitoring**: Real-time status tracking

##  **Mobile Responsiveness**

- **Responsive Grid**: Adapts to different screen sizes
- **Touch-Friendly**: Mobile-optimized interactions
- **Optimized Charts**: Mobile-optimized visualizations
- **Adaptive Layout**: Automatic column adjustment

##  **Future Enhancements**

- **Additional Sensor Types**: Expand sensor support
- **Advanced Analytics**: Machine learning integration
- **Alert System**: Email/SMS notifications
- **Data Export**: CSV/JSON export functionality
- **User Authentication**: Role-based access control
- **Mobile App**: Native mobile applications

##  **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

##  **License**

This project is licensed under the MIT License - see the LICENSE file for details.

##  **Support**

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code examples

---

**ResQSense** - Protecting miners through advanced technology and real-time monitoring. ⛏️🔒
