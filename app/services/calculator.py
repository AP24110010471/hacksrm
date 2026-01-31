class CalculatorService:
    def __init__(self, data_loader):
        self.fertilizers = data_loader.get_fertilizers()

    def calculate_requirements(self, crop_details, land_area_acres, soil_profile):
        """
        Calculates seeds, water, and fertilizer requirements.
        """
        if not crop_details:
            return None

        # 1. Seed Calculation
        seed_needed = crop_details['seed_rate_kg_per_acre'] * land_area_acres

        # 2. Water Calculation (Total seasonal requirement)
        # 1 mm rainfall on 1 acre = ~4046 liters.
        # This is a rough estimation of total volume needed.
        water_liters = crop_details['water_req_mm'] * 4046.86 * land_area_acres

        # 3. Fertilizer Calculation (Simply NPK matching)
        # Target NPK in kg
        target_n = crop_details['npk_kg_per_acre']['N'] * land_area_acres
        target_p = crop_details['npk_kg_per_acre']['P'] * land_area_acres
        target_k = crop_details['npk_kg_per_acre']['K'] * land_area_acres

        # Suggest fertilizer mix (Simplistic optimization)
        # We will try to fulfill N using Urea, P using DAP/SSP, K using MOP.
        
        # Urea is 46% N. To get 1kg N, we need 1/0.46 = 2.17 kg Urea.
        urea_needed = target_n / 0.46 if target_n > 0 else 0
        
        # SSP is 16% P. To get 1kg P, we need 1/0.16 = 6.25 kg SSP.
        ssp_needed = target_p / 0.16 if target_p > 0 else 0
        
        # MOP is 60% K. To get 1kg K, we need 1/0.60 = 1.66 kg MOP.
        mop_needed = target_k / 0.60 if target_k > 0 else 0

        fertilizer_plan = {
            "Urea": round(urea_needed, 2),
            "SSP": round(ssp_needed, 2),
            "MOP": round(mop_needed, 2)
        }

        return {
            "seeds_kg": round(seed_needed, 2),
            "water_liters_seasonal": round(water_liters, 2),
            "fertilizer_plan_kg": fertilizer_plan,
            "target_npk_kg": {"N": target_n, "P": target_p, "K": target_k}
        }

    def get_application_schedule(self, crop_name):
        """
        Returns detailed timing and dosage instructions.
        """
        return [
            {"stage": "Basal Dose (At Sowing)", "detail": "Apply 50% N, 100% P, 100% K.", "method": "Soil Application below seed."},
            {"stage": "Vegetative Stage (30 Days)", "detail": "Apply 25% N.", "method": "Top dressing near root zone."},
            {"stage": "Flowering Stage (50 Days)", "detail": "Apply remaining 25% N.", "method": "Top dressing when soil is moist."}
        ]
