class CropRecommendationService:
    def __init__(self, data_loader):
        self.crops = data_loader.get_crops()
        self.soil_profiles = data_loader.get_soil_profiles()

    def recommend_crops(self, soil_type, climate_zone, season):
        """
        Recommend crops based on Soil Type compatability and Season.
        Climate zone is used for validation (simple matching).
        """
        recommendations = []
        explanations = []

        # Normalize inputs
        soil_type = soil_type.capitalize() # e.g., "Black"
        season = season.capitalize() # e.g., "Kharif"

        for crop in self.crops:
            score = 0
            reasons = []

            # 1. Soil Match
            if soil_type in crop['suitable_soils']:
                score += 50
                reasons.append(f"Well suited for {soil_type} soil.")
            else:
                reasons.append(f"Not typically grown in {soil_type} soil.")
            
            # 2. Season Match (Strict)
            if crop['season'].lower() == "annual" or crop['season'].lower() == season.lower():
                score += 30
                reasons.append(f"Matches the current {season} season.")
            else:
                score -= 100 # Invalid season
                reasons.append(f"Wrong season (Requires {crop['season']}).")

            if score > 50:
                recommendations.append({
                    "crop": crop,
                    "score": score,
                    "reasons": reasons
                })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations

    def get_crop_details(self, crop_name):
        for crop in self.crops:
            if crop['name'].lower() == crop_name.lower():
                return crop
        return None
