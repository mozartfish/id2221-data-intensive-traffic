import subprocess
import time
from pymongo import MongoClient
import pandas as pd

def ensure_spark_cache():
    try:
        subprocess.run([
            "docker", "exec", "--user", "root", "spark", "bash", "-c",
            "mkdir -p /home/spark/.ivy2/cache && chmod -R 777 /home/spark/.ivy2"
        ], check=True)
    except subprocess.CalledProcessError:
        pass

def start_docker():
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    time.sleep(15)

def start_producer():
    subprocess.Popen(["python", "producer.py"])
    time.sleep(5)

def start_spark():
    subprocess.run([
        "docker", "exec", "spark", "bash", "-c",
        "/opt/spark/bin/spark-submit "
        "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2 "
        "/app/spark_stream_simple.py"
    ])

def visualize_mongodb_head():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["trafiklab"]
    docs = list(db.departures.find().limit(5))
    if docs:
        df = pd.DataFrame(docs)
        print(df[["operator", "line", "destination", "scheduled", "realtime", "delay_seconds"]].head())

if __name__ == "__main__":
    start_docker()
    ensure_spark_cache()
    start_producer()
    start_spark()
    visualize_mongodb_head()
