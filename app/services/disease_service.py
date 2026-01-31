import random

class DiseaseService:
    def __init__(self):
        self.diseases = {
            "Cotton": [
                {"name": "Pink Bollworm", "symptoms": "Holes in bolls, stained lint.", "remedy": "Use Pheromone traps."},
                {"name": "Leaf Curl Virus", "symptoms": "Upward curling of leaves.", "remedy": "Control whitefly vectors."}
            ],
            "Rice": [
                {"name": "Blast Disease", "symptoms": "Spindle-shaped lesions on leaves.", "remedy": "Spray Tricyclazole."},
                {"name": "Brown Spot", "symptoms": "Brown circular spots on leaves.", "remedy": "Balanced nutrition (add Zinc)."}
            ],
            "Wheat": [
                {"name": "Yellow Rust", "symptoms": "Yellow stripes on leaves.", "remedy": "Resistant varieties, Propiconazole."},
                {"name": "Loose Smut", "symptoms": "Black powdery mass in earheads.", "remedy": "Seed treatment with Carboxin."}
            ]
        }
        
    def get_potential_risk(self, crop_name, weather_condition):
        """
        Returns a random potential disease risk based on crop and weather.
        """
        crop_key = crop_name.split('(')[0].strip()
        possible_diseases = self.diseases.get(crop_key, [])
        
        if not possible_diseases:
            return {
                "disease_name": "None",
                "risk_level": "None",
                "symptoms": "N/A",
                "remedy": "N/A"
            }
            
        # Simulate Random Infection
        infection = random.choice(possible_diseases)
        
        risk_level = "Low"
        if "Rain" in weather_condition or "Cloudy" in weather_condition:
            risk_level = "High"
            
        return {
            "disease_name": infection['name'],
            "risk_level": risk_level,
            "symptoms": infection['symptoms'],
            "remedy": infection['remedy']
        }
