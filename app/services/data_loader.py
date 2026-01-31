import json
import os
import pandas as pd

class DataLoader:
    def __init__(self, data_dir='app/data'):
        self.data_dir = data_dir
        self.geo_data = []
        self.soil_profiles = {}
        self.crops = []
        self.fertilizers = {}
        self._load_data()

    def _load_data(self):
        # Load Geo Data
        with open(os.path.join(self.data_dir, 'geo_data.json'), 'r') as f:
            self.geo_data = json.load(f)
        
        # Load Soil Profiles
        with open(os.path.join(self.data_dir, 'soil_profiles.json'), 'r') as f:
            self.soil_profiles = json.load(f)

        # Load Crops
        with open(os.path.join(self.data_dir, 'crops.json'), 'r') as f:
            self.crops = json.load(f)

        # Load Fertilizers
        with open(os.path.join(self.data_dir, 'fertilizers.json'), 'r') as f:
            self.fertilizers = json.load(f)

        # Load Villages (Handle missing file gracefully)
        try:
            with open(os.path.join(self.data_dir, 'villages.json'), 'r') as f:
                self.villages = json.load(f)
        except Exception:
            self.villages = {}

    def get_geo_data(self):
        return self.geo_data

    def get_soil_profiles(self):
        return self.soil_profiles

    def get_crops(self):
        return self.crops

    def get_fertilizers(self):
        return self.fertilizers
        
    def get_villages(self):
        return self.villages
