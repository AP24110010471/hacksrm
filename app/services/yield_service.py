class YieldService:
    def __init__(self, data_loader):
        self.crops = data_loader.get_crops()

    def calculate_yield(self, crop_name, area_acres, soil_type, climate_zone):
        """
        Calculates potential yield based on crop type and environmental factors.
        """
        # Base yields in Quintals per Acre (Mock Data)
        base_yields = {
            "Cotton": 12,
            "Wheat": 18,
            "Rice": 25,
            "Bajra": 10,
            "Sugarcane": 300,
            "Maize": 22,
            "Soybean": 15
        }
        
        crop_base = base_yields.get(crop_name.split('(')[0].strip(), 15) # Default 15
        
        # Modifiers based on environment
        modifier = 1.0
        
        # Soil Synergy
        # Ideally this should check 'suitable_soils' from crop db, but simplifying for robustness
        msg = "Standard Conditions"
        if "Black" in soil_type and crop_name in ["Cotton", "Sugarcane"]:
            modifier += 0.2
            msg = "High Yield (Excellent Soil Match)"
        elif "Alluvial" in soil_type and crop_name in ["Wheat", "Rice"]:
            modifier += 0.2
            msg = "High Yield (Excellent Soil Match)"
        elif "Red" in soil_type and crop_name in ["Bajra", "Maize"]:
             modifier += 0.1
        
        final_yield_per_acre = crop_base * modifier
        total_yield = final_yield_per_acre * area_acres
        
        return {
            "yield_per_acre": round(final_yield_per_acre, 1),
            "total_yield": round(total_yield, 1),
            "unit": "Quintals",
            "prediction_confidence": msg
        }
