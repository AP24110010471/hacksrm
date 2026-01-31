import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def main():
    print_section("1. System Check")
    try:
        resp = requests.get(BASE_URL + "/")
        print("Server Status:", resp.json())
    except Exception as e:
        print("Error connecting to server. Make sure app.py is running!")
        return

    # Scenario: Farmer in Pune (Black Soil) in Kharif season with 2 acres
    print_section("2. Scenario: Farmer in Pune (2 acres)")
    
    # Step 1: Location Analysis
    print(">>> Detecting Location Details for 'Pune'...")
    loc_payload = {"district": "Pune"}
    loc_resp = requests.post(f"{BASE_URL}/location-analysis", json=loc_payload)
    
    if loc_resp.status_code != 200:
        print("Location API failed:", loc_resp.text)
        return

    loc_data = loc_resp.json()
    print("Location Data Detected:")
    print(json.dumps(loc_data['location'], indent=2))
    print("Soil Analysis:")
    print(json.dumps(loc_data['soil_analysis'], indent=2))
    
    detected_soil = loc_data['location']['soil_type']
    detected_climate = loc_data['location']['climate_zone']
    
    # Step 2: Crop Recommendation
    print_section("3. Asking AI for Crop Recommendations (Kharif Season)")
    rec_payload = {
        "soil_type": detected_soil,
        "climate_zone": detected_climate,
        "season": "Kharif"
    }
    rec_resp = requests.post(f"{BASE_URL}/recommend-crops", json=rec_payload)
    recommendations = rec_resp.json()['recommendations']
    
    print(f"Server returned {len(recommendations)} recommendations.")
    for idx, rec in enumerate(recommendations, 1):
        print(f"{idx}. {rec['crop']['name']} (Score: {rec['score']})")
        print(f"   Reasons: {'; '.join(rec['reasons'])}")

    if not recommendations:
        print("No crops found.")
        return

    best_crop = recommendations[0]['crop']['name']
    
    # Step 3: Calculator & Explanation
    print_section(f"4. Calculating Resources for {best_crop} (2 Acres)")
    calc_payload = {
        "crop_name": best_crop,
        "land_area_acres": 2,
        "soil_type": detected_soil
    }
    calc_resp = requests.post(f"{BASE_URL}/calculate-resources", json=calc_payload)
    final_data = calc_resp.json()
    
    print("Resource Requirements:")
    print(json.dumps(final_data['quantities'], indent=2))
    
    print_section("5. Explainable AI (XAI) Justification")
    print(final_data['ai_explanation']['crop_suitability'])
    print("-" * 20)
    print("Fertilizer Logic:")
    print(final_data['ai_explanation']['fertilizer_logic'])

if __name__ == "__main__":
    main()
