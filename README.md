# id2221-data-intensive-traffic

## Developers 
- Pranav Rajan, David Tanudin 

## Description 
This project was developed as the final part of the ID2221 course at KTH to gain practice with big data processing and data pipelines. The objective of this project was to understand the infrastructure and plumbing behind data applications and dealing with real world big data using tools including Spark, Kafka, and MongoDB. The project implements a real-time data processing pipeline that ingests transit data from Trafiklab's API, streams it through Kafka, processes it with Spark Streaming, and stores it in MongoDB for analysis.

## Data Source 
- [Trafiklab](https://www.trafiklab.se/) - scheduled, real-time data 
- [SL API](https://www.trafiklab.se/api/our-apis/sl/) - Real-time transit departures

## Technical Stack
### Data Source 
- SL Transport API → Real-Time transit data

### Ingestion 
- Kafka → Real-time streaming message broker

### Processing 
- Spark Streaming → Real-time data processing 

### Storage 
- MongoDB → NoSQL database for stream data

## Data Pipeline Architecture
### Real-Time Data Pipeline 
```
Trafiklab API → Kafka Producer → Kafka Broker → Spark Consumer → MongoDB
```

---

## Prerequisites
- **Python 3.11+** (tested with Python 3.12)
- **Docker Desktop** (with Docker Compose)
- **Trafiklab API Key** - Get one from [Trafiklab](https://www.trafiklab.se/)

---

## Installation and Setup

### Option 1: Using pip (Recommended for Windows)

#### 1. Clone the repository
```bash
git clone <repository-url>
cd id2221-data-intensive-traffic
```

#### 2. Set up Python environment
```bash
# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Configure environment variables
Create a `.env` file in the project root:
```bash
TRAFIKLAB_KEY=your_api_key_here
```

#### 4. Start Docker containers
```bash
docker-compose up -d
```

Verify all containers are running:
```bash
docker ps
```

You should see: `zookeeper`, `kafka`, `kafdrop`, `mongodb`, and `spark` containers.

#### 5. Fix Spark Ivy cache permissions
**Important:** Run this command to prevent Spark permission errors:
```bash
docker exec -it --user root spark bash -c "mkdir -p /home/spark/.ivy2/cache && chmod -R 777 /home/spark/.ivy2"
```

#### 6. Run the data pipeline
```bash
python main.py
```

This will:
- Start the Kafka producer (fetching data from Trafiklab)
- Start the Spark consumer (processing and storing to MongoDB)
- Display sample records from MongoDB

---

### Option 2: Using uv (Alternative)

#### 1. Install [uv](https://docs.astral.sh/uv/)
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Sync dependencies
```bash
uv sync
```

#### 3. Follow steps 3-6 from Option 1 above
Use `uv run` prefix for Python commands:
```bash
uv run python main.py
uv run jupyter lab
```

---

## Project Structure
```
id2221-data-intensive-traffic/
├── main.py                 # Main orchestration script
├── producer.py             # Kafka producer (Trafiklab → Kafka)
├── spark_stream_simple.py  # Spark streaming consumer (Kafka → MongoDB)
├── docker-compose.yml      # Docker services configuration
├── requirements.txt        # Python dependencies
├── pyproject.toml          # UV/Python project config
├── .env                    # Environment variables (create this)
└── README.md
```

---

## Services & Ports
| Service   | Port  | Purpose                          | URL                        |
|-----------|-------|----------------------------------|----------------------------|
| Kafka     | 9092  | Internal broker                  | kafka:9092                 |
| Kafka     | 29092 | External (localhost) broker      | localhost:29092            |
| Kafdrop   | 9000  | Kafka web UI                     | http://localhost:9000      |
| MongoDB   | 27017 | NoSQL database                   | mongodb://localhost:27017  |
| Zookeeper | 2181  | Kafka coordination               | -                          |

---

## Usage

### Running the full pipeline
```bash
python main.py
```

### Running components individually

#### Start Kafka producer only:
```bash
python producer.py
```

#### View Kafka messages in Kafdrop:
Open http://localhost:9000 in your browser

#### Run Spark streaming consumer:
```bash
docker exec spark bash -c "/opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.2 \
  /app/spark_stream_simple.py"
```

#### Query MongoDB data (Python):
```python
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client["trafiklab"]
docs = list(db.departures.find().limit(10))
df = pd.DataFrame(docs)
print(df)
```

#### Query MongoDB data (MongoDB Shell):
Access the MongoDB shell directly:
```bash
docker exec -it mongodb mongosh
```

Then use these commands inside the MongoDB shell:
```javascript
// Switch to the trafiklab database
use trafiklab

// Show all collections
show collections

// Count total documents
db.departures.countDocuments()

// View first 5 documents (prettified)
db.departures.find().limit(5).pretty()

// View specific fields only
db.departures.find({}, {operator: 1, line: 1, destination: 1, delay_seconds: 1, _id: 0}).limit(5)

// Find delayed departures
db.departures.find({delay_seconds: {$gt: 60}}).pretty()

// Exit MongoDB shell
exit
```

---

## Troubleshooting

### Issue: `kafka.vendor.six.moves` module not found
**Solution:** Uninstall `kafka-python` and install `kafka-python-ng`:
```bash
pip uninstall kafka-python -y
pip install kafka-python-ng
```

### Issue: Spark Ivy cache permission denied
**Solution:** Run the following command:
```bash
docker exec -it --user root spark bash -c "mkdir -p /home/spark/.ivy2/cache && chmod -R 777 /home/spark/.ivy2"
```

### Issue: Docker containers not starting
**Solution:** 
```bash
# Stop all containers
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up -d
```

### Issue: No data in MongoDB
**Solution:** 
- Check if producer is running: `docker logs kafka`
- Check if Kafka topic exists: Visit http://localhost:9000
- Verify `.env` file has valid `TRAFIKLAB_KEY`

---

## License
MIT License



