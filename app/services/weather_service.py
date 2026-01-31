import random
from datetime import datetime

class WeatherService:
    def __init__(self):
        pass

    def get_current_weather(self, location_details):
        """
        Generates a 'current' weather report based on the climate zone bounds.
        """
        # Extract bounds
        t_min = location_details.get('avg_tmin', 20)
        t_max = location_details.get('avg_tmax', 35)
        
        # Simulate current temp (somewhere between min and max)
        current_temp = random.uniform(t_min, t_max)
        
        # Simulate conditions based on temp/zone
        conditions = ["Clear Sky", "Partly Cloudy", "Haze", "Sunny"]
        if "Tropical" in location_details.get('climate_zone', ''):
            conditions.extend(["Humid", "Light Rain"])
            humidity = random.randint(60, 90)
        else:
            humidity = random.randint(30, 60)
            
        return {
            "temp_c": round(current_temp, 1),
            "condition": random.choice(conditions),
            "humidity_percent": humidity,
            "wind_speed_kmh": random.randint(5, 20),
            "last_updated": datetime.now().strftime("%H:%M")
        }
