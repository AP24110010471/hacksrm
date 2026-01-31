import urllib.request
import os

url = "https://4kwallpapers.com/images/wallpapers/agriculture-farm-land-countryside-aerial-view-green-3840x2160-3985.jpg"
output_path = "app/static/custom_natural.jpg"

print(f"Downloading from {url}...")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
        out_file.write(response.read())
    print(f"Successfully saved to {output_path}")
except Exception as e:
    print(f"Error downloading: {e}")
