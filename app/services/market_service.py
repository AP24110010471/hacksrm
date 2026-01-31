import random

class MarketService:
    def __init__(self, data_loader):
        self.crops = data_loader.get_crops()
        # Base market prices (INR per Quintal)
        self.base_prices = {
            "Cotton": 6000,
            "Wheat": 2125,
            "Rice": 2200,
            "Bajra": 2350,
            "Sugarcane": 315, # Per quintal
            "Maize": 2090,
            "Soybean": 4600
        }

    def get_live_price(self, crop_name, location_state):
        """
        Simulates fetching a live market price.
        Adds volatility based on simplistic random factors to mimic 'live' nature.
        """
        crop_key = crop_name.split('(')[0].strip()
        base = self.base_prices.get(crop_key, 2000)
        
        # Simulate market fluctuation (+/- 5%)
        fluctuation = random.uniform(-0.05, 0.05)
        current_price = base * (1 + fluctuation)
        
        # Trend indicator
        trend = "▲ UP" if fluctuation > 0 else "▼ DOWN"
        
        return {
            "crop": crop_name,
            "price_per_quintal": round(current_price, 2),
            "currency": "INR",
            "market_location": f"{location_state} APMC",
            "trend": trend,
            "fluctuation_percent": round(fluctuation * 100, 2)
        }
