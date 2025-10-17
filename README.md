# id2221-data-intensive-traffic

## Developers 
- Pranav Rajan, David Tanudin 

## Description 
This project was developed as the final part of the ID2221 course at KTH to gain practice with big data processing and data pipelines. The objective of this project was to understand the infrastructure and plumbing behind data applications and dealing with real world big data using tools including Spark, Kafka, and MongoDB. The project implements a real-time data processing pipeline that ingests transit data from Trafiklab's API, streams it through Kafka, processes it with Spark Streaming, and stores it in MongoDB for analysis.

## Data Source 
- [Trafiklab](https://www.trafiklab.se/) - Real-time Swedish transit data
- [SL API](https://www.trafiklab.se/api/our-apis/sl/) - Real-time transit departures

## Technical Stack
- **Data Source:** Trafiklab API
- **Ingestion:** Kafka
- **Processing:** Spark Streaming
- **Storage:** MongoDB
- **Visualization:** Flask Web Dashboard

## Data Pipeline Architecture
```
Trafiklab API → Producer → Kafka → Spark → MongoDB → Web Dashboard
```

---

## Prerequisites
- **Python 3.11+**
- **Docker Desktop**
- **Trafiklab API Key** - [Get one here](https://www.trafiklab.se/)

---

## Installation and Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd id2221-data-intensive-traffic
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API key
Create a `.env` file in the project root:
```bash
TRAFIKLAB_KEY=your_api_key_here
```

### 4. Start the pipeline
```bash
python main.py
```

This starts Docker containers, Kafka producer, and Spark streaming.

### 5. Start the web dashboard (in separate terminal)
```bash
python web_dashboard.py
```

### 6. Open the dashboard
Open http://localhost:5432 in your browser to:
- Search for transit stops
- View real-time departures
- Auto-start producers for monitored stops

**Note:** After searching and selecting a stop, wait approximately 60 seconds for the first API call to complete and data to appear. The producer fetches data every minute.

**Note:** Make sure the `.env` file with your Trafiklab API key is in the same directory as `main.py` and `web_dashboard.py`.

---

## Services & Ports
| Service   | Port  | URL                        |
|-----------|-------|----------------------------|
| Kafka     | 29092 | localhost:29092            |
| Kafdrop   | 9000  | http://localhost:9000      |
| MongoDB   | 27017 | mongodb://localhost:27017  |
| Dashboard | 5432  | http://localhost:5432      |

---

## Project Structure
```
id2221-data-intensive-traffic/
├── main.py                  # Pipeline orchestration
├── web_dashboard.py         # Flask web interface
├── producer.py              # Kafka producer
├── producer_manager.py      # Auto-start producers
├── spark_stream_simple.py   # Spark streaming consumer
├── mongo_query.py           # MongoDB query examples
├── docker-compose.yml       # Docker services
├── requirements.txt         # Python dependencies
├── .env                     # API key (create this)
└── templates/
    └── dashboard.html       # Web UI
```

---

## Query MongoDB

### Using Python (mongo_query.py)
```bash
python mongo_query.py
```

### Using MongoDB Shell
```bash
docker exec -it mongodb mongosh
```

```javascript
use trafiklab
db.departures.find().limit(5).pretty()
db.departures.countDocuments()
exit
```

---

## Troubleshooting

### Kafka import error
If you see `kafka.vendor.six.moves` module not found:
```bash
pip uninstall kafka-python -y
pip install kafka-python-ng
```

### Spark permission error
If Spark fails with Ivy cache permission denied:
```bash
docker exec -it --user root spark bash -c "mkdir -p /home/spark/.ivy2/cache && chmod -R 777 /home/spark/.ivy2"
```

### Docker not starting
If containers fail to start:
```bash
docker-compose down
docker-compose up -d
```

### No data appearing
If MongoDB is empty:
- Verify `.env` file contains valid `TRAFIKLAB_KEY`
- Check Kafka UI at http://localhost:9000
- Ensure producer is running