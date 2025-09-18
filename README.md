# id2221-data-intensive-traffic

## Developers 
- Pranav Rajan, David Tanudin 

## Description 
This project ws developed as the final part of the ID2221 course at KTH to gain practice with big data procesing and data pipelines. The objective of this project was to understand the infrastructure and plumbing behind data applications and dealing with real world big data(streaming, batch) using tools including HDFs, Spark, Kafka, Cassandra/MongoDB and designing a data processing pipeline architecture to process the data and store it into a NoSQL database and either perform visualization or machine learning on the data. We chose the Trafiklab Data specifically for their real-time and scheduled data apis which offered opportunities to explore real time data processing and batch data processing and how to engineer pipelines for these different types of data.

## Data Source 
- [Trafiklab](https://www.trafiklab.se/) - scheduled, real-time data 

### Data API 
- [SL API](https://www.trafiklab.se/api/our-apis/sl/)

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

## Installation and Setup 

