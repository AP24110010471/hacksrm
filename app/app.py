import sys
import os
import json

# Robust Path Handling
# Add the current directory (app/) to sys.path to ensure 'services' can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from services.data_loader import DataLoader
from services.geo_service import GeoService
from services.recommendation_engine import CropRecommendationService
from services.calculator import CalculatorService
from services.xai_engine import XAIEngine
from services.disease_service import DiseaseService
from services.yield_service import YieldService
from services.market_service import MarketService
from services.weather_service import WeatherService

app = Flask(__name__)


# ... (Previous services initialized)
# ... (Previous services initialized)
# Use absolute path for data directory to avoid CWD issues
DATA_DIR = os.path.join(current_dir, 'data')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

disease_service = DiseaseService()

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_history(data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/calculate-resources', methods=['POST'])
def calculate():
    data = request.json
    crop_name = data.get('crop_name')
    try:
        area = float(data.get('area', 1))
    except (ValueError, TypeError):
        area = 1.0
    soil_type = data.get('soil_type', 'Loamy') # Default if not provided
    
    # Need to fetch details for calculation
    crop_details = img_service.get_crop_details(crop_name)
    soil_profile = data_loader.get_soil_profiles().get(soil_type, {})
    
    if not crop_details:
         return jsonify({"error": "Crop not found"}), 404

    # 1. Basic Calculation using existing service method
    resources = calc_service.calculate_requirements(crop_details, area, soil_profile)
    
    # 2. Add detailed schedule (Adding this method to service next)
    schedule = calc_service.get_application_schedule(crop_name)
    
    # 3. Add explanation
    # Construct comprehensive AI Insight
    location_details = data.get('location_details', {})
    
    # Get explanations
    why_crop = xai_service.explain_recommendation(soil_profile, crop_details, location_details)
    why_fert = xai_service.explain_fertilizer(resources)
    
    # Combine with a visual separator
    full_explanation = f"{why_crop}\n\n**Nutrient Plan**:\n{why_fert}"
    
    return jsonify({
        "resources": resources,
        "schedule": schedule,
        "explanation": full_explanation
    })

@app.route('/get-disease-risk', methods=['POST'])
def get_disease():
    data = request.json
    crop = data.get('crop_name')
    weather = data.get('weather_condition', 'Clear')
    
    risk_info = disease_service.get_potential_risk(crop, weather)
    return jsonify(risk_info)

@app.route('/history', methods=['GET', 'POST'])
def handle_history():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user'] # Using user handle as key
    history_db = load_history()
    
    if request.method == 'GET':
        return jsonify(history_db.get(user_id, []))
        
    if request.method == 'POST':
        record = request.json
        if user_id not in history_db:
            history_db[user_id] = []
        
        # Add basic timestamp/id simulation
        record['year'] = record.get('year', '2025')
        history_db[user_id].append(record)
        save_history(history_db)
        return jsonify({"msg": "Record Saved"})
app.secret_key = 'super_secret_offline_key' # Required for sessions

# Services Initialized below


# Initialize Services
data_loader = DataLoader(DATA_DIR)
geo_service = GeoService(data_loader)
img_service = CropRecommendationService(data_loader)
calc_service = CalculatorService(data_loader)
yield_service = YieldService(data_loader)
market_service = MarketService(data_loader)
weather_service = WeatherService()
xai_service = XAIEngine()

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/', methods=['GET'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        if username in users and users[username]['password'] == password:
            session['user'] = users[username]['fullname']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid Credentials")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        users = load_users()
        
        if username in users:
            return render_template('register.html', error="User already exists!")
            
        users[username] = {"password": password, "fullname": fullname}
        save_users(users)
        
        session['user'] = fullname
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/location-analysis', methods=['POST'])
def analyze_location():
    data = request.json
    location_details = None
    
    district_input = data.get('district', '')
    village_input = data.get('village', '')
    
    # Prioritize Village if provided, otherwise District
    search_term = village_input if village_input else district_input
    
    location_details = geo_service.get_details_by_district(search_term)
    
    if not location_details:
        return jsonify({"error": "Location not found in database. Try a supported Village/District."}), 404

    # Enhance with soil profile details
    soil_type = location_details['soil_type']
    soil_profile = data_loader.get_soil_profiles().get(soil_type, {})
    
    # Get Live Weather
    current_weather = weather_service.get_current_weather(location_details)
    
    response = {
        "location": location_details,
        "soil_analysis": soil_profile,
        "current_weather": current_weather,
        "status_msg": "Location Mapped Successfully"
    }
    return jsonify(response)

@app.route('/get-market-price', methods=['POST'])
def get_price():
    data = request.json
    crop_name = data.get('crop_name')
    state = data.get('state', 'India')
    
    price_info = market_service.get_live_price(crop_name, state)
    return jsonify(price_info)

@app.route('/calculate-yield', methods=['POST'])
def calc_yield():
    data = request.json
    crop = data.get('crop_name')
    area = float(data.get('area', 1))
    soil = data.get('soil_type', 'Unknown')
    climate = data.get('climate_zone', 'Unknown')
    
    result = yield_service.calculate_yield(crop, area, soil, climate)
    return jsonify(result)

@app.route('/recommend-crops', methods=['POST'])
def recommend():
    data = request.json
    # Expecting: { "soil_type": "Black", "climate_zone": "Semi-Arid", "season": "Kharif" }
    
    soil_type = data.get('soil_type')
    climate = data.get('climate_zone')
    season = data.get('season')

    recommendations = img_service.recommend_crops(soil_type, climate, season)
    return jsonify({"recommendations": recommendations})

# Duplicate removed


if __name__ == '__main__':
    print("Starting purely local offline server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
