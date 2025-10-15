import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TRAFIKLAB_KEY")

STOP_ID = "740000002"  # Göteborg Central
URL = f"https://realtime-api.trafiklab.se/v1/departures/{STOP_ID}?key={API_KEY}"

print("Fetching data from Trafiklab Realtime API...")
resp = requests.get(URL, timeout=10)
print("Status:", resp.status_code)

if resp.ok:
    data = resp.json()
    for d in data["departures"]:
        line = d["route"].get("designation")
        operator = d["agency"]["name"]
        dest = d["route"].get("direction")
        sched = d.get("scheduled")
        rt = d.get("realtime")
        delay = d.get("delay")
        print(f"{operator} line {line} → {dest} | scheduled: {sched}, realtime: {rt}, delay: {delay}s")

else:
    print("Error:", resp.text)

URL = f"https://realtime-api.trafiklab.se/v1/stops/list?key={API_KEY}"

print("\nFetching list of stops from Trafiklab Realtime API...")
resp = requests.get(URL, timeout=10)
print("Status:", resp.status_code)
if resp.ok:
    data = resp.json()
    with open("stops.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    
