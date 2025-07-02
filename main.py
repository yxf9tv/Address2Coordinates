import pandas as pd
import requests
import time

# Replace this with your actual API key
API_KEY = 'blocked out for privacy'

# Load the CSV
df = pd.read_csv("geocoded_addresses.csv")

# Clean Zip and combine address fields
df["Zip"] = df["Zip"].astype(str).str.replace(".0", "", regex=False).str.zfill(5)
df["Full_Address"] = df["Street"] + ", " + df["City"] + ", " + df["State"] + " " + df["Zip"]

# Initialize output columns
df["Latitude"] = None
df["Longitude"] = None


# Define geocoding function
def get_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        print(f"❌ {address} | Status: {data['status']}")
        return None, None


# Loop through and geocode
for idx, row in df.iterrows():
    address = row["Full_Address"]
    lat, lng = get_coordinates(address)
    df.at[idx, "Latitude"] = lat
    df.at[idx, "Longitude"] = lng
    time.sleep(0.1)  # avoid API rate limit

# Save to CSV
df.to_csv("geocoded_output.csv", index=False)
print("✅ Geocoding complete. File saved as geocoded_output.csv")
