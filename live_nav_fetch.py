import time
import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

def fetch_with_retry(url, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries:
                raise e
            print(f"  [Attempt {attempt} failed: {e}. Retrying in {delay}s...]")
            time.sleep(delay)

# Step 4: Fetch live NAV for one fund (125497 - SBI Small Cap Fund)
print("--- Step 4: Fetching single fund NAV (Scheme 125497) ---")
url = "https://api.mfapi.in/mf/125497"
result = fetch_with_retry(url)

print("Meta:", result.get("meta"))
df = pd.DataFrame(result["data"])
df["scheme_code"] = 125497
df.to_csv("data/raw/live_nav_125497.csv", index=False)
print("Saved live_nav_125497.csv with shape:", df.shape)
print(df.head())

# Step 5: Fetch NAV for the 5 key schemes
print("\n--- Step 5: Fetching 5 key schemes NAV ---")
schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

for name, code in schemes.items():
    try:
        data_json = fetch_with_retry(f"https://api.mfapi.in/mf/{code}")
        d = pd.DataFrame(data_json["data"])
        d["scheme_code"] = code
        out_path = f"data/raw/nav_{name}.csv"
        d.to_csv(out_path, index=False)
        print(f"Successfully fetched and saved {name} (code: {code}) -> {out_path} Shape: {d.shape}")
    except Exception as e:
        print(f"Error fetching {name} ({code}): {e}")
    time.sleep(1)  # be polite to the API

print("\nLive NAV fetching complete!")
