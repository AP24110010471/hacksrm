# Geo-Intelligent Crop, Soil & Fertilizer Advisory Platform

## Overview
This is a purely software-based, offline decision intelligence system for agriculture. It runs on a local Flask server and uses pre-loaded datasets to provide recommendations.

## Live Demo
🚀 **[Try it Live on Render](https://hacksrm.onrender.com)**

## Features
- **Location Intelligence**: Maps districts/coordinates to soil and climate zones.
- **Crop Recommendation**: Suggests crops based on soil, season, and climate.
- **Resource Calculator**: Computes seeds, water, and fertilizer dosage (N-P-K).
- **Explainable AI (XAI)**: Provides human-readable reasons for every recommendation.
- **Offline Capable**: No internet required after setup.

## Folder Structure
```
hacksrm/
├── app/
│   ├── app.py                 # Main Flask Application
│   ├── data/                  # Mock Datasets (JSON/CSV)
│   └── services/              # Business Logic Modules
├── requirements.txt           # Python Dependencies
├── demo_scenario.py           # Verification Script
└── README.md                  # This file
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher.
- `pip` (Python package manager).

### 2. Installation
Open a terminal in this folder and run:
```bash
# Install dependencies
pip install -r requirements.txt
```

*Note: If `pip` is missing, run `python -m ensurepip --default-pip` first.*

### 3. Running with One-Click Scripts (Windows)
- Double-click **`start_server.bat`**. 
  - Checks for Python/Pip -> Installs requirements -> Starts Server.
  - If it fails, please read **`SETUP_GUIDE.md`**.
- Double-click **`run_demo.bat`** to run the simulation.

### 4. Manual Execution
See **`SETUP_GUIDE.md`** for detailed manual instructions.

You should see: `Running on http://0.0.0.0:5000`

### 4. Running the Demo
Open a new terminal window (keep the server running) and execute:
```bash
python demo_scenario.py
```
This script simulates a farmer in **Pune** (Black Soil) looking for **Kharif** crops, performs calculations, and prints the AI explanation.

## API Endpoints
- **POST** `/location-analysis`: `{ "district": "Pune" }`
- **POST** `/recommend-crops`: `{ "soil_type": "Black", "season": "Kharif", "climate_zone": "Semi-Arid" }`
- **POST** `/calculate-resources`: `{ "crop_name": "Cotton", "land_area_acres": 2, "soil_type": "Black" }`
