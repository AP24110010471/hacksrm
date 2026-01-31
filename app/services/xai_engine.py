class XAIEngine:
    def explain_recommendation(self, soil_details, crop_details, location_details):
        """
        Generates a text explanation for why a crop was recommended.
        """
        soil_type = location_details.get('soil_type', 'Unknown')
        crop_name = crop_details.get('name', 'Crop')
        
        explanation = [
            f"**Why {crop_name}?**",
            f"1. **Soil Match**: This location has *{soil_type}* soil, which provides the necessary drainage and texture for {crop_name}.",
            f"2. **Climate Fit**: Detailed analysis shows that the temperature range ({location_details.get('avg_tmin')}-{location_details.get('avg_tmax')}°C) matches the ideal growth phase for this crop.",
            f"3. **Sustainability**: {crop_name} is compatible with the current organic carbon levels ({soil_details.get('organic_carbon', 'Unknown')}) in the soil.",
            "",
            "**Long-term Impact**:",
            "Continuous cultivation without rotation may deplete specific nutrients. Consider rotating with pulses to restore Nitrogen."
        ]
        return "\n".join(explanation)

    def explain_fertilizer(self, calculation_result):
        """
        Explains the fertilizer dosage.
        """
        plan = calculation_result['fertilizer_plan_kg']
        return (f"To meet the nutrient goal of N:{calculation_result['target_npk_kg']['N']}kg, "
                f"P:{calculation_result['target_npk_kg']['P']}kg, K:{calculation_result['target_npk_kg']['K']}kg:\n"
                f"- **Urea** ({plan['Urea']}kg) is chosen as the primary Nitrogen source (cheap and effective).\n"
                f"- **SSP** ({plan['SSP']}kg) provides Phosphorus and essential Sulphur.\n"
                f"- **MOP** ({plan['MOP']}kg) supplies Potassium which aids in root strengthening.")
