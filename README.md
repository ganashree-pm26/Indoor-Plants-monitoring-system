# 🌱 Indoor Plant Monitoring & Recommendation System

A comprehensive Flask web application that monitors indoor plant conditions using ESP32 sensors and provides intelligent plant recommendations based on real-time environmental data.

## 🌟 Features

### 📊 Real-time Monitoring
- **Live Sensor Data**: Real-time readings updated every 2 seconds
- **Serial Communication**: Direct connection to ESP32 via USB
- **Connection Status**: Visual indicator showing ESP32 connection status with animated pulse effect
- **All Sensors**: Displays temperature, humidity, soil moisture, air quality, light intensity, and NPK values
- **Data Interpretation**: Automatic conversion of raw sensor values to human-readable formats
- **Timestamp Tracking**: Last update timestamps for all sensor readings

### 🌿 Plant Intelligence
- **AI-Powered Recommendations**: Advanced algorithm that scores plants based on 8 environmental parameters
- **Smart Matching**: Percentage-based compatibility scoring (0-100%) for each plant
- **Multi-Parameter Analysis**: Evaluates light, moisture, humidity, temperature, air quality, and NPK levels
- **Top 3 Recommendations**: Automatically sorts and displays the best plant matches
- **Detailed Parameter Breakdown**: Shows which conditions each plant prefers and current status
- **Plant Library**: Comprehensive database of 30+ indoor plants with detailed care information
- **Care Tips**: Specific care instructions for each plant
- **Toxicity Information**: Pet and human safety information
- **Fun Facts**: Interesting trivia about each plant species

### 🎨 Modern Interface
- **Responsive Design**: Beautiful, mobile-friendly web interface with CSS Grid
- **Interactive Dashboard**: Real-time data visualization with animated cards
- **Plant Profiles**: Detailed individual plant pages with high-quality images
- **Smart Matching**: Percentage-based compatibility scoring with visual indicators
- **Navigation System**: Clean navigation between Dashboard, Recommendations, Plant Suggester, and Library
- **Hover Effects**: Interactive elements with smooth transitions and animations
- **Status Indicators**: Visual connection status with color-coded indicators

### 📱 Web Interface Pages

#### 🏠 Dashboard (`/`)
- Real-time sensor data display with animated cards
- Connection status indicator with pulse animation
- Live data updates every 2 seconds
- Individual sensor cards for each parameter
- NPK values displayed in a special 3-column layout
- Last update timestamps

#### 🌿 Plant Recommendations (`/recommend`)
- AI-powered plant suggestions based on current conditions
- Top 3 recommendations with percentage match scores
- Expandable detailed parameter analysis
- Visual indicators for in-range vs out-of-range conditions
- Plant images with overlay information
- Interactive "Know More" buttons

#### 📚 Plant Library (`/library`)
- Browse all 30+ available plants
- Filter and search functionality
- Quick access to plant information
- Grid layout with plant cards

#### 💡 Plant Suggester (`/suggest`)
- Personalized care recommendations
- Environmental condition analysis
- Actionable advice for optimal plant health
- Comprehensive plant database access

#### 🌱 Individual Plant Profiles (`/plant/<plant_name>`)
- Detailed care information
- Toxicity warnings
- Fun facts and trivia
- High-quality plant images

### 🔧 Data Processing & Interpretation

#### Sensor Value Conversions
- **Soil Moisture**: Raw values converted to percentage (wet/dry scale)
- **Air Quality**: Raw values converted to PPM and qualitative levels (Good/Moderate/Poor)
- **Light Intensity**: Raw values converted to percentage and qualitative levels (Low/Moderate/Bright/Very Bright)
- **NPK Values**: Direct display of Nitrogen, Phosphorous, and Potassium levels

#### Recommendation Algorithm
- **8-Parameter Scoring**: Evaluates light, moisture, humidity, temperature, air quality, N, P, K
- **Range Checking**: Each parameter checked against plant's preferred ranges
- **Percentage Calculation**: Match percentage based on parameters in optimal range
- **Smart Sorting**: Plants ranked by compatibility score
- **Detailed Analysis**: Shows current values vs. plant preferences

## 📡 Sensor Data Displayed

- 🌡️ **Temperature**: Ambient temperature in °C
- 💧 **Humidity**: Relative humidity percentage
- 🌱 **Soil Moisture**: Raw sensor value (0-4095) with percentage conversion
- 🌫️ **Air Quality**: Raw air quality sensor value with PPM conversion and qualitative levels
- 💡 **Light Intensity**: Raw light sensor value with percentage conversion and brightness levels
- 🌾 **NPK Values**: Nitrogen, Phosphorous, and Potassium levels

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Serial Port

Edit `app.py` and change the `SERIAL_PORT` variable to match your ESP32:

```python
SERIAL_PORT = 'COM3'  # Windows
# SERIAL_PORT = '/dev/ttyUSB0'  # Linux
# SERIAL_PORT = '/dev/tty.usbserial'  # Mac
```

**To find your ESP32 port:**
- **Windows**: Check Device Manager under "Ports (COM & LPT)"
- **Linux**: Usually `/dev/ttyUSB0` or `/dev/ttyACM0`
- **Mac**: Usually `/dev/tty.usbserial-*`

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Web Interface

Open your browser and go to: `http://localhost:5000`

## 🔧 ESP32 Data Format

The application expects your ESP32 to send data in this format:

```
📦 Sensor Readings:
🌡️ Temperature: 28.20 °C
💧 Humidity: 62.20 %
🌱 Soil Moisture (raw): 368
🌫️ Air Quality (raw): 1302
💡 Light Intensity (raw): 4095
🌾 Nitrogen: 7
🌾 Phosphorous: 9
🌾 Potassium: 24
```

## 📁 File Structure

```
indoor_plant/
├── app.py                    # Main Flask application with recommendation algorithm
├── requirements.txt          # Python dependencies
├── static/
│   ├── images/              # Plant images (30+ species)
│   └── plant_data.json      # Plant database with care data and fun facts
├── templates/
│   ├── index.html           # Main dashboard with real-time monitoring
│   ├── recommend.html       # Plant recommendations with AI scoring
│   ├── library.html         # Plant library with search/filter
│   └── suggest.html         # Care suggestions and plant database
└── README.md               # This file
```

## 🔌 API Endpoints

- `GET /` - Main dashboard with live sensor data
- `GET /recommend` - AI-powered plant recommendations page
- `GET /library` - Plant library with search functionality
- `GET /suggest` - Care suggestions and plant database
- `GET /plant/<plant_name>` - Individual plant profile pages
- `GET /api/readings` - Returns latest sensor data (JSON)
- `GET /api/status` - Returns connection status (JSON)

## 🌱 Plant Database

The system includes 30+ indoor plants with comprehensive information:

- **Care Requirements**: Light, moisture, humidity, temperature ranges
- **NPK Preferences**: Nitrogen, Phosphorous, Potassium needs
- **Air Quality Tolerance**: Maximum air quality sensor values
- **Care Tips**: Specific watering and maintenance instructions
- **Toxicity Information**: Pet and human safety warnings
- **Fun Facts**: Interesting trivia about each species
- **High-Quality Images**: Professional plant photographs

### Featured Plants Include:
- Snake Plant, Peace Lily, Areca Palm, ZZ Plant, Pothos
- Spider Plant, Aloe Vera, Fiddle Leaf Fig, Monstera Deliciosa
- Rubber Plant, Calathea, Boston Fern, Cast Iron Plant
- Anthurium, Chinese Evergreen, Dracaena, Croton
- Parlor Palm, Dumb Cane, English Ivy, Prayer Plant
- Umbrella Plant, Aglaonema, Jade Plant, Money Plant
- Kentia Palm, Syngonium, Dwarf Banana Plant, Bird of Paradise
- Oxalis, Peperomia, and many more...

## 🛠️ Troubleshooting

### Connection Issues
1. **Wrong Port**: Make sure the `SERIAL_PORT` in `app.py` matches your ESP32
2. **Permission Denied**: On Linux/Mac, you might need to add your user to the `dialout` group
3. **Port in Use**: Close any other applications using the serial port (Arduino IDE, etc.)

### No Data Displayed
1. **Check ESP32**: Ensure your ESP32 is sending data in the correct format
2. **Baud Rate**: Verify the baud rate matches your ESP32 (default: 115200)
3. **Console Output**: Check the Python console for error messages

### Web Interface Issues
1. **Browser Cache**: Try refreshing the page or clearing browser cache
2. **JavaScript**: Ensure JavaScript is enabled in your browser
3. **Network**: Make sure you're accessing `http://localhost:5000`

## ⚙️ Customization

### Change Update Frequency
Edit the JavaScript in `templates/index.html`:
```javascript
// Update data every 2 seconds (change 2000 to desired milliseconds)
setInterval(fetchSensorData, 2000);
```

### Add New Plants
Edit `static/plant_data.json` to add new plants with their care requirements, fun facts, and toxicity information.

### Modify Sensor Parsing
Edit the `parse_sensor_data()` function in `app.py` to match your ESP32's output format.

### Adjust Data Interpretation
Modify the `interpret_readings()` function to customize:
- Soil moisture conversion ranges
- Air quality thresholds
- Light intensity levels

### Styling
The web interface uses modern CSS Grid and responsive design. Customize styles in the `<style>` sections of the HTML templates.

## 📋 Requirements

- Python 3.7+
- Flask 2.3.3
- pyserial 3.5
- ESP32 with sensors connected
- Web browser with JavaScript enabled

## 🤝 Contributing

This project is open source! Feel free to:
- Add new plants to the database with care information and fun facts
- Improve the recommendation algorithm and scoring system
- Enhance the UI/UX with new features
- Add new sensor support and data interpretation
- Report bugs or suggest features
- Improve the plant database with more detailed information

## 📄 License

This project is open source and available under the MIT License. 