class GeoService:
    def __init__(self, data_loader):
        self.geo_data = data_loader.get_geo_data()
        self.villages = data_loader.get_villages()

    def get_details_by_district(self, district_name):
        """
        Finds geo-location details by district or village name (case-insensitive).
        """
        input_name = district_name.lower().strip()
        print(f"[DEBUG] Searching for input: '{input_name}'")
        
        # 1. Check if it's a known village
        if input_name in self.villages:
            mapped_district = self.villages[input_name]
            print(f"[DEBUG] Village '{input_name}' is in district '{mapped_district}'")
            # Recursive call with the mapped district
            result = self.get_details_by_district(mapped_district)
            if result:
                # Add context only if it's a fresh dict (avoid mutating original cache)
                result = result.copy()
                result['detected_village'] = district_name.title()
            return result
            
        print(f"[DEBUG] Not a village, checking districts...")
        
        for location in self.geo_data:
            db_name = location.get('district', '').lower()
            if db_name == input_name:
                print(f"[DEBUG] Match found for district!")
                return location
        
        print("[DEBUG] No match found.")
        return None

    def get_details_by_lat_long(self, lat, long):
        """
        Finds details by checking if the coordinate falls within a known range.
        Simple bounding box check for this prototype.
        """
        for location in self.geo_data:
            if (location['latitude_range'][0] <= lat <= location['latitude_range'][1] and
                location['longitude_range'][0] <= long <= location['longitude_range'][1]):
                return location
        return None
