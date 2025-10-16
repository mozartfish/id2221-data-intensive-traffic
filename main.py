import subprocess
import time
import os
from pymongo import MongoClient
import pandas as pd

def ensure_spark_cache():
    """Create and fix permissions for Spark's Ivy cache."""
    print("Ensuring Spark Ivy cache exists and has correct permissions...")
    try:
        subprocess.run([
            "docker", "exec", "-it", "spark", "bash", "-c",
            "mkdir -p /home/spark/.ivy2/cache && chmod -R 777 /home/spark/.ivy2"
        ], check=True)
        print("Spark Ivy cache ready.")
    except subprocess.CalledProcessError:
        print("Warning: could not set Ivy permissions (Spark may still run).")

def start_docker():
    print("Starting Docker containers (Kafka, Spark, MongoDB)...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("Containers are up.")
    time.sleep(10)  

def start_producer():
    print("Starting Trafiklab → Kafka producer...")
    subprocess.Popen(["python", "producer.py"])
    time.sleep(5)
    print("Producer running in background.")

def start_spark():
    print("Starting Spark Streaming consumer in background...")
    subprocess.Popen([
        "docker", "exec", "spark", "bash", "-c",
        "/opt/spark/bin/spark-submit "
        "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
        "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2 "
        "/app/spark_stream_simple.py"
    ])
    print("Spark consumer started. Waiting for data to flow through pipeline...")
    time.sleep(20)  # Wait for Spark to initialize and process first batch

def visualize_mongodb_head():
    print("\n" + "="*60)
    print("Fetching records from MongoDB...")
    print("="*60)
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["trafiklab"]
        
        # Check if collection exists and has data
        count = db.departures.count_documents({})
        print(f"Total documents in MongoDB: {count}")
        
        if count == 0:
            print("\n⚠️  No records found yet.")
            print("The pipeline is running. Data should appear soon.")
            print("You can check MongoDB later with:")
            print("  python -c \"from pymongo import MongoClient; print(list(MongoClient('mongodb://localhost:27017/')['trafiklab']['departures'].find().limit(5)))\"")
        else:
            docs = list(db.departures.find().limit(5))
            df = pd.DataFrame(docs)
            print("\n✅ Sample records from MongoDB:\n")
            # Display available columns, handle if expected columns don't exist
            available_cols = [col for col in ["operator", "line", "destination", "scheduled", "realtime", "delay_seconds"] 
                            if col in df.columns]
            if available_cols:
                print(df[available_cols].to_string(index=False))
            else:
                print(df.to_string(index=False))
        
        client.close()
    except Exception as e:
        print(f"\n❌ Error connecting to MongoDB: {e}")
        print("Make sure MongoDB container is running: docker ps")

if __name__ == "__main__":
    start_docker()
    ensure_spark_cache()
    start_producer()
    start_spark()
    visualize_mongodb_head()
    
    print("\n" + "="*60)
    print("Pipeline is running!")
    print("="*60)
    print("• Producer: Streaming data from Trafiklab to Kafka")
    print("• Spark: Processing Kafka messages and writing to MongoDB")
    print("• MongoDB: Storing processed data")
    print("\nUseful commands:")
    print("  - View Kafka topics: http://localhost:9000")
    print("  - Check MongoDB: docker exec -it mongodb mongosh")
    print("  - Stop all: docker-compose down")
    print("="*60)
