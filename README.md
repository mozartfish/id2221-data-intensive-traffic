# id2221-data-intensive-traffic
ID2221 Data Intensive Computing Project 

## Data Source 
[Trafiklab](https://www.trafiklab.se/) - scheduled, real-time data 

### Data API 
[SL API](https://www.trafiklab.se/api/our-apis/sl/)

## Technical Stack + Setup 
### Data Source 
- SL Transport API -> Real-Time 
- GTFS Regional -> Scheduled 

### Ingestion 
- Kafka -> Real-Time streaming 
- HDFS(upload) -> batch GTFS data 

### Processing 
- Spark -> Batch processing 
- Kafka/Spark Streams -> Real-time processing 

### Storage 
- HDFs -> raw data storage 
- HBase -> real-time lookup 
- mongodb/cassandra - eda 

## Data Pipeline 
### Real-Time Data Pipeline 
- SL API -> Kafka -> Spark Stream -> Cassandra/MongoDB 

### Batch Data Pipeline 
- GTFS File -> HDFS -> Spark Batch -> Cassandra/MongoDB 


## TBD 
### Visualization
- Apache Superset 
- Grafana 
- Jupyter Notebook - Altair/matplotlib 
### Machine Learning 
- Spark mllib 


