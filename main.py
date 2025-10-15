import subprocess
import time
import os
from pymongo import MongoClient
import pandas as pd

def start_docker():
    print("Starting Docker containers (Kafka, Spark, MongoDB)...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("Containers are up.")
    time.sleep(10)  # give Kafka & Mongo some time to initialize

def start_producer():
    print("Starting Trafiklab → Kafka producer...")
    # Run producer in background so Spark can start too
    subprocess.Popen(["python", "producer.py"])
    time.sleep(5)
    print("Producer running in background.")

def start_spark():
    print("Starting Spark Streaming consumer...")
    subprocess.run([
        "docker", "exec", "spark", "bash", "-c",
        "/opt/spark/bin/spark-submit "
        "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2 "
        "/app/spark_stream_simple.py"
    ])

def visualize_mongodb_head():
    print("Fetching a few records from MongoDB...")
    client = MongoClient("mongodb://localhost:27017/")
    db = client["trafiklab"]
    docs = list(db.departures.find().limit(5))
    if not docs:
        print("No records found yet. Wait for the stream to populate MongoDB.")
    else:
        df = pd.DataFrame(docs)
        print(df[["operator", "line", "destination", "scheduled", "realtime", "delay_seconds"]].head())

if __name__ == "__main__":
    start_docker()
    start_producer()
    start_spark()
    visualize_mongodb_head()
