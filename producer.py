import os
import requests
import json
import time
from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv()
API_KEY = os.getenv("TRAFIKLAB_KEY")

STOP_ID = "740000002"  # Göteborg Central
URL = f"https://realtime-api.trafiklab.se/v1/departures/{STOP_ID}?key={API_KEY}&limit=100&time_window=60"

KAFKA_TOPIC = "sl_stream"
KAFKA_BROKER = "localhost:29092"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v, indent=2, ensure_ascii=False).encode("utf-8"),
    request_timeout_ms=30000,
    metadata_max_age_ms=30000,
    retries=3
)

print("Starting Trafiklab → Kafka producer...")

while True:
    try:
        resp = requests.get(URL, timeout=10)
        print("Status:", resp.status_code)

        if resp.ok:
            data = resp.json()
            departures = data.get("departures", [])
            print(f"📊 Received {len(departures)} departures from API")

            for d in departures:
                line = d["route"].get("designation")
                operator = d["agency"]["name"]
                dest = d["route"].get("direction")
                sched = d.get("scheduled")
                rt = d.get("realtime")
                delay = d.get("delay")

                message = {
                    "operator": operator,
                    "line": line,
                    "destination": dest,
                    "scheduled": sched,
                    "realtime": rt,
                    "delay_seconds": delay,
                }

                producer.send(KAFKA_TOPIC, message)
                print("Sent to Kafka:", message)

            producer.flush()
        else:
            print("Error fetching data:", resp.text)

    except Exception as e:
        print("Exception:", e)

    time.sleep(60)
