let currentLocData = null;
let currentCropName = null;

async function analyzeLocation() {
    const district = document.getElementById('districtInput').value;
    const village = document.getElementById('villageInput').value;
    const errorEl = document.getElementById('locationError');
    const resultEl = document.getElementById('locationResult');

    errorEl.textContent = '';
    resultEl.classList.add('hidden');

    if (!district && !village) {
        errorEl.textContent = "Please enter a District OR Village.";
        return;
    }

    try {
        const response = await fetch('/location-analysis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ district: district, village: village })
        });

        if (!response.ok) {
            throw new Error('Location not found in database (Try a demo village like "Araku Valley", "Uppal", "Kazipet")');
        }

        const data = await response.json();
        currentLocData = data;

        let locName = data.location.district;
        if (data.location.detected_village) {
            locName = `${data.location.detected_village}, ${data.location.district}`;
        }

        document.getElementById('detectedLoc').textContent = locName;
        document.getElementById('soilType').textContent = data.location.soil_type;
        document.getElementById('climateZone').textContent = data.location.climate_zone;

        // Live Weather Update
        if (data.current_weather) {
            document.getElementById('tempDisplay').textContent = `${data.current_weather.temp_c}°C`;
            document.getElementById('weatherCondition').textContent = data.current_weather.condition;
            document.getElementById('humidityDisplay').textContent = data.current_weather.humidity_percent;
            document.getElementById('windDisplay').textContent = data.current_weather.wind_speed_kmh;
        }

        resultEl.classList.remove('hidden');
        document.getElementById('step2').classList.remove('hidden');
    } catch (e) {
        errorEl.textContent = e.message;
    }
}

async function recommendCrops() {
    if (!currentLocData) return;

    const season = document.getElementById('seasonInput').value;
    const resultGrid = document.getElementById('cropResult');
    resultGrid.innerHTML = 'Loading...';
    resultGrid.classList.remove('hidden');

    try {
        const response = await fetch('/recommend-crops', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                soil_type: currentLocData.location.soil_type,
                climate_zone: currentLocData.location.climate_zone,
                season: season
            })
        });

        const data = await response.json();
        resultGrid.innerHTML = '';

        if (data.recommendations.length === 0) {
            resultGrid.innerHTML = '<p>No specific recommendations for this criteria.</p>';
            return;
        }

        data.recommendations.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'crop-card';
            card.innerHTML = `
                <div class="crop-header">
                    <strong>${rec.crop.name}</strong>
                    <span class="crop-score">${rec.score}%</span>
                </div>
                <small>${rec.reasons[0]}</small>
                <button class="btn-secondary" style="margin-top:0.5rem; font-size:0.8rem; padding:0.3rem 0.8rem; width:100%;">Select</button>
            `;
            card.onclick = () => selectCrop(rec.crop.name, card);
            resultGrid.appendChild(card);
        });

    } catch (e) {
        resultGrid.innerHTML = 'Error fetching crops.';
    }
}

async function selectCrop(cropName, cardElement) {
    currentCropName = cropName;

    // UI selection
    document.querySelectorAll('.crop-card').forEach(el => el.classList.remove('selected'));
    cardElement.classList.add('selected');

    document.getElementById('selectedCropName').textContent = cropName;

    // Update Yield Section
    document.getElementById('yieldCropName').textContent = cropName;
    document.getElementById('step3a').classList.remove('hidden');
    document.getElementById('yieldResult').classList.add('hidden');

    // Update Market Section
    document.getElementById('priceCropName').textContent = cropName;
    document.getElementById('marketSection').classList.remove('hidden');
    fetchMarketPrice(cropName);

    const step3 = document.getElementById('step3');
    step3.classList.remove('hidden');
    document.getElementById('calcResult').classList.add('hidden');

    // Smooth scroll to next step so user sees the 'Get Resources' button
    step3.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function fetchMarketPrice(cropName) {
    document.getElementById('priceValue').textContent = "Loading...";
    try {
        const response = await fetch('/get-market-price', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop_name: cropName,
                state: currentLocData.location.state
            })
        });
        const data = await response.json();

        document.getElementById('priceValue').textContent = `₹ ${data.price_per_quintal}/q`;
        document.getElementById('marketLoc').textContent = `at ${data.market_location}`;

        const trendEl = document.getElementById('priceTrend');
        trendEl.textContent = `${data.trend} (${Math.abs(data.fluctuation_percent)}%)`;
        trendEl.style.color = data.trend.includes('UP') ? '#27ae60' : '#e74c3c';

    } catch (e) {
        console.error("Market data failed");
    }
}

async function calculateYield() {
    if (!currentCropName || !currentLocData) return;
    const area = document.getElementById('yieldArea').value;

    const response = await fetch('/calculate-yield', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            crop_name: currentCropName,
            area: area,
            soil_type: currentLocData.location.soil_type,
            climate_zone: currentLocData.location.climate_zone
        })
    });

    const data = await response.json();
    const el = document.getElementById('yieldResult');
    document.getElementById('yieldValue').textContent = `${data.total_yield} ${data.unit} (${data.prediction_confidence})`;
    el.classList.remove('hidden');
}

async function calculateResources() {
    if (!currentCropName || !currentLocData) return;

    const area = document.getElementById('areaInput').value;
    const resultBox = document.getElementById('calcResult');

    // Fetch Resources + Schedule
    try {
        // Default area to 1 if empty or invalid
        let areaVal = parseFloat(area);
        if (isNaN(areaVal) || areaVal <= 0) {
            areaVal = 1;
            document.getElementById('areaInput').value = 1;
        }

        const response = await fetch('/calculate-resources', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop_name: currentCropName,
                area: areaVal,
                soil_type: currentLocData.location.soil_type,
                location_details: currentLocData.location // Sending full details for AI Engine
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server returned an error');
        }

        // Render Resources
        const res = data.resources;
        if (!res) throw new Error("Invalid response data");

        const plan = res.fertilizer_plan_kg || {};

        document.getElementById('resourceOutput').innerHTML = `
            <ul>
                <li><strong>Seeds:</strong> ${res.seeds_kg} kg</li>
                <li><strong>Urea (N):</strong> ${plan.Urea || 0} kg</li>
                <li><strong>SSP (P):</strong> ${plan.SSP || 0} kg</li>
                <li><strong>MOP (K):</strong> ${plan.MOP || 0} kg</li>
                <li><strong>Water:</strong> ${res.water_liters_seasonal} Liters/season</li>
            </ul>
        `;

        // Render Schedule
        const schedDiv = document.getElementById('scheduleOutput');
        schedDiv.innerHTML = data.schedule.map(s => `
            <div class="timeline-item">
                <strong>${s.stage}</strong><br>
                ${s.detail}<br>
                <em style="font-size:0.9rem; color:#666;">Method: ${s.method}</em>
            </div>
        `).join('');

        // Render AI Explanation with basic Markdown parsing
        let explanation = data.explanation;
        if (explanation) {
            // Convert **bold** to <b>bold</b>
            explanation = explanation.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            // Convert newline to <br>
            explanation = explanation.replace(/\n/g, '<br>');
        } else {
            explanation = "AI analysis is currently unavailable for this specific crop configuration.";
        }

        document.getElementById('aiExplanation').innerHTML = explanation;

        // Check Disease Risk
        checkDiseaseRisk(currentCropName);

        resultBox.classList.remove('hidden');
    } catch (e) {
        console.error(e);
        alert("Error: " + e.message);
    }
}

async function checkDiseaseRisk(cropName) {
    const diseaseBox = document.getElementById('diseaseBox');
    diseaseBox.classList.add('hidden');

    // Simple logic: if weather is cloudy/humid, show risk
    try {
        const response = await fetch('/get-disease-risk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop_name: cropName,
                weather_condition: document.getElementById('weatherCondition').textContent
            })
        });

        const data = await response.json();
        if (data.risk_level !== "None") {
            document.getElementById('diseaseName').textContent = data.disease_name;
            document.getElementById('diseaseRisk').textContent = data.risk_level;
            document.getElementById('diseaseRemedy').textContent = data.remedy;
            diseaseBox.classList.remove('hidden');
        }
    } catch (e) {
        console.error("Disease check failed");
    }
}

async function addToHistory() {
    if (!currentLocData || !currentCropName) return;

    const record = {
        date: new Date().toISOString().split('T')[0],
        crop: currentCropName,
        district: currentLocData.location.district,
        yield_est: document.getElementById('yieldValue').textContent
    };

    try {
        const response = await fetch('/history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(record)
        });
        const res = await response.json();
        alert("Saved to History!");
        loadHistory(); // Refresh table if exists
    } catch (e) {
        alert("Failed to save history");
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/history');
        if (!response.ok) return; // User might not be logged in or other error

        const historyData = await response.json();
        const tbody = document.querySelector('#historyTable tbody');
        tbody.innerHTML = '';

        if (historyData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4">No records found. Save a plan to see it here!</td></tr>';
            return;
        }

        historyData.reverse().forEach(record => {
            const row = `<tr>
                <td>${record.date || record.year}</td>
                <td>${record.crop}</td>
                <td>${record.district}</td>
                <td>${record.yield_est}</td>
            </tr>`;
            tbody.innerHTML += row;
        });
    } catch (e) {
        console.error("History load failed", e);
    }
}

async function runDiseaseDiagnosis() {
    if (!currentCropName) {
        alert("Please select a crop first (Step 2).");
        return;
    }

    // Update the display name in the diagnosis card
    document.getElementById('diagnosisCropName').textContent = currentCropName;

    // Reuse the existing disease service logic but present it vividly
    const visualizer = document.getElementById('diseaseVisualizer');
    visualizer.classList.remove('hidden');
    visualizer.innerHTML = '<p>Analyzing crop health parameters...</p>';

    try {
        const response = await fetch('/get-disease-risk', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                crop_name: currentCropName,
                weather_condition: document.getElementById('weatherCondition').textContent || 'Clear'
            })
        });

        const data = await response.json();

        // Dynamic Icon based on risk
        let icon = "🌿"; // Healthy
        let color = "#27ae60";
        if (data.risk_level === "Moderate") { icon = "⚠️"; color = "#f39c12"; }
        if (data.risk_level === "High") { icon = "🦠"; color = "#c0392b"; }

        visualizer.innerHTML = `
            <div class="visualizer-screen" style="background: rgba(255,255,255,0.5); padding: 20px; border-radius: 10px; border: 2px solid ${color};">
                <div style="font-size:3rem;">${icon}</div>
                <h3 id="diagName" style="color:${color}">${data.disease_name === "None" ? "Healthy Crop" : data.disease_name}</h3>
                <p><strong>Risk Level:</strong> <span style="font-weight:bold; color:${color}">${data.risk_level}</span></p>
                ${data.remedy ? `<p><strong>Recommended Action:</strong> ${data.remedy}</p>` : '<p>Conditions are favorable for healthy growth.</p>'}
            </div>
        `;

    } catch (e) {
        visualizer.innerHTML = '<p style="color:red">Diagnosis failed. Server error.</p>';
    }
}

// --- Settings & UI Logic ---

function toggleSettings() {
    const modal = document.getElementById('settingsModal');
    modal.classList.toggle('active');
}

function closeSettings(e) {
    if (e.target.id === 'settingsModal') {
        document.getElementById('settingsModal').classList.remove('active');
    }
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');

    // Update button text
    const btn = document.getElementById('themeBtn');
    if (isDark) {
        btn.innerHTML = '<ion-icon name="sunny-outline"></ion-icon> <span data-i18n="light_mode">Light Mode</span>';
    } else {
        btn.innerHTML = '<ion-icon name="moon-outline"></ion-icon> <span data-i18n="dark_mode">Dark Mode</span>';
    }
    // Re-apply language to new button text
    const currentLang = localStorage.getItem('language') || 'en';
    changeLanguage(currentLang);
}

function changeLanguage(lang) {
    localStorage.setItem('language', lang);
    document.getElementById('languageSelect').value = lang;

    const dict = translations[lang] || translations['en'];

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Translate dynamic elements if needed
    // Example: Placeholders could be handled here if added to dictionary
}

// --- 3D Tilt Effect ---
function initTiltEffect() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * -10; // Max 10deg rotation
            const rotateY = ((x - centerX) / centerX) * 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
        });
    });
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    initTiltEffect();

    // Load Saved Settings
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        toggleTheme(); // This will switch to dark
    }

    const savedLang = localStorage.getItem('language') || 'en';
    changeLanguage(savedLang);
});
