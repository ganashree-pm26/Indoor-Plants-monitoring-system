from flask import Flask, render_template, jsonify
import serial
import re
import threading
import time
from datetime import datetime
import json
import os

app = Flask(__name__)

# Load plant data from JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLANT_DATA_PATH = os.path.join(BASE_DIR, 'static', 'plant_data.json')
with open(PLANT_DATA_PATH, 'r') as f:
    PLANT_DATA = json.load(f)

# Global variable to store the latest sensor readings
latest_readings = {
    'temperature': 0.0,
    'humidity': 0.0,
    'soil_moisture': 0,
    'air_quality': 0,
    'light_intensity': 0,
    'nitrogen': 0,
    'phosphorous': 0,
    'potassium': 0,
    'timestamp': datetime.now().isoformat()
}

# Serial connection settings
SERIAL_PORT = 'COM3'  # Change this to match your ESP32 port
BAUD_RATE = 115200
serial_connection = None

def parse_sensor_data(data):
    """Parse sensor readings from serial data"""
    readings = {}
    
    # Temperature
    temp_match = re.search(r'🌡️ Temperature: ([\d.]+) °C', data)
    if temp_match:
        readings['temperature'] = float(temp_match.group(1))
    
    # Humidity
    humidity_match = re.search(r'💧 Humidity: ([\d.]+) %', data)
    if humidity_match:
        readings['humidity'] = float(humidity_match.group(1))
    
    # Soil Moisture
    soil_match = re.search(r'🌱 Soil Moisture \(raw\): (\d+)', data)
    if soil_match:
        readings['soil_moisture'] = int(soil_match.group(1))
    
    # Air Quality
    air_match = re.search(r'🌫️ Air Quality \(raw\): (\d+)', data)
    if air_match:
        readings['air_quality'] = int(air_match.group(1))
    
    # Light Intensity
    light_match = re.search(r'💡 Light Intensity \(raw\): (\d+)', data)
    if light_match:
        readings['light_intensity'] = int(light_match.group(1))
    
    # Nitrogen
    nitrogen_match = re.search(r'🌾 Nitrogen: (\d+)', data)
    if nitrogen_match:
        readings['nitrogen'] = int(nitrogen_match.group(1))
    
    # Phosphorous
    phosphorous_match = re.search(r'🌾 Phosphorous: (\d+)', data)
    if phosphorous_match:
        readings['phosphorous'] = int(phosphorous_match.group(1))
    
    # Potassium
    potassium_match = re.search(r'🌾 Potassium: (\d+)', data)
    if potassium_match:
        readings['potassium'] = int(potassium_match.group(1))
    
    return readings

def read_serial_data():
    """Background thread to continuously read serial data"""
    global latest_readings, serial_connection
    
    while True:
        try:
            if serial_connection and serial_connection.is_open:
                if serial_connection.in_waiting:
                    data = serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    
                    # Look for the sensor readings section
                    if 'Sensor Readings:' in data:
                        # Read the next few lines to get all sensor data
                        sensor_data = data + '\n'
                        for _ in range(8):  # Read next 8 lines
                            if serial_connection.in_waiting:
                                line = serial_connection.readline().decode('utf-8', errors='ignore').strip()
                                sensor_data += line + '\n'
                        
                        # Parse the sensor data
                        parsed_readings = parse_sensor_data(sensor_data)
                        if parsed_readings:
                            latest_readings.update(parsed_readings)
                            latest_readings['timestamp'] = datetime.now().isoformat()
                            print(f"Updated readings: {latest_readings}")
            
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            
        except Exception as e:
            print(f"Error reading serial data: {e}")
            time.sleep(1)

def connect_serial():
    """Connect to the ESP32 via serial"""
    global serial_connection
    
    try:
        serial_connection = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to ESP32 on {SERIAL_PORT}")
        return True
    except Exception as e:
        print(f"Failed to connect to ESP32: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/readings')
def get_readings():
    """API endpoint to get latest sensor readings"""
    return jsonify(latest_readings)

@app.route('/api/status')
def get_status():
    """API endpoint to check connection status"""
    status = {
        'connected': serial_connection is not None and serial_connection.is_open,
        'port': SERIAL_PORT,
        'baud_rate': BAUD_RATE
    }
    return jsonify(status)

@app.route('/recommend')
def recommend():
    """Recommends plants based on current sensor data."""
    readings = {
        'light': latest_readings.get('light_intensity', 0),
        'moisture': latest_readings.get('soil_moisture', 0),
        'humidity': latest_readings.get('humidity', 0),
        'temp': latest_readings.get('temperature', 0),
        'air_quality': latest_readings.get('air_quality', 0),
        'n': latest_readings.get('nitrogen', 0),
        'p': latest_readings.get('phosphorous', 0),
        'k': latest_readings.get('potassium', 0),
    }

    def map_value(value, fromLow, fromHigh, toLow, toHigh):
        return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

    recommendations = []
    for plant in PLANT_DATA:
        score = 0
        details = {}

        param_checks = {
            'light': ('light', readings['light']),
            'moisture': ('moisture', readings['moisture']),
            'humidity': ('humidity', readings['humidity']),
            'temp': ('temp', readings['temp']),
            'n': ('n', readings['n']),
            'p': ('p', readings['p']),
            'k': ('k', readings['k']),
        }

        for param, (key, value) in param_checks.items():
            in_range = plant[key][0] <= value <= plant[key][1]
            if in_range:
                score += 1
            
            detail_obj = {'value': value, 'in_range': in_range}
            if param == 'light':
                light_percent = map_value(value, 4095, 0, 0, 100)
                detail_obj['percent'] = round(max(0, min(100, light_percent)))
            details[param] = detail_obj

        air_quality_val = readings['air_quality']
        air_in_range = air_quality_val <= plant['air_quality'][1]
        if air_in_range:
            score += 1
        
        air_ppm = (air_quality_val / 4095.0) * 1000
        details['air_quality'] = {
            'value': air_quality_val, 
            'in_range': air_in_range,
            'ppm': round(air_ppm, 2)
        }
        
        match_percentage = (score / 8) * 100
        
        recommendations.append({
            'plant': plant,
            'match_percentage': match_percentage,
            'details': details
        })

    sorted_recommendations = sorted(recommendations, key=lambda x: x['match_percentage'], reverse=True)
    top_recommendations = sorted_recommendations[:3]

    return render_template('recommend.html', recommendations=top_recommendations, readings=readings)

@app.route('/suggest')
def suggest():
    """Renders the suggestions page with all plant data."""
    return render_template('suggest.html', plants=PLANT_DATA)


@app.route('/library')
def library():
    """Renders the plant library page."""
    return render_template('library.html', plants=PLANT_DATA)


@app.route('/plant/<plant_name>')
def plant_profile(plant_name):
    """Renders the detailed profile page for a specific plant."""
    plant = next((p for p in PLANT_DATA if p['name'] == plant_name), None)
    if plant:
        # The detailed data isn't here yet, but we can render the page
        return render_template('plant_profile.html', plant=plant)
    return "Plant not found", 404


def interpret_readings(readings):
    """Adds human-readable interpretations to the raw sensor data."""
    interpreted = readings.copy()

    # 1. Soil Moisture to Percentage
    # Updated calibration to match UI: 500 (wet) to 3000 (dry)
    SOIL_WET_RAW = 500  # Raw value when fully submerged in water
    SOIL_DRY_RAW = 3000   # Raw value when in completely dry air
    
    raw_soil = readings.get('soil_moisture', SOIL_DRY_RAW)
    raw_soil_clamped = max(SOIL_WET_RAW, min(SOIL_DRY_RAW, raw_soil))
    soil_percent = 100 * (SOIL_DRY_RAW - raw_soil_clamped) / (SOIL_DRY_RAW - SOIL_WET_RAW)
    interpreted['soil_moisture_percent'] = round(soil_percent)

    # 2. Air Quality to Qualitative Level
    # NOTE: Based on common MQ-135 sensor behavior (higher value = worse air).
    raw_air = readings.get('air_quality', 0)
    if raw_air < 1400:
        air_level = "Good"
    elif raw_air < 1800:
        air_level = "Moderate"
    else:
        air_level = "Poor"
    interpreted['air_quality_level'] = air_level

    # 3. Light Intensity to Qualitative Level
    # NOTE: Based on a 12-bit ADC (0-4095). Higher value = more light.
    raw_light = readings.get('light_intensity', 0)
    if raw_light > 3000:
        light_level = "Very Bright"
    elif raw_light > 1500:
        light_level = "Bright"
    elif raw_light > 500:
        light_level = "Moderate"
    else:
        light_level = "Low"
    interpreted['light_intensity_level'] = light_level

    return interpreted

if __name__ == '__main__':
    # Start serial connection
    if connect_serial():
        # Start background thread for reading serial data
        serial_thread = threading.Thread(target=read_serial_data, daemon=True)
        serial_thread.start()
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False) 