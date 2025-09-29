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

### Ingestion 
- Kafka -> Real-Time streaming

### Processing 
- Kafka/Spark Streams -> Real-time processing 

### Storage 
- cassandra -> for the big stream data 

## Data Pipeline 
### Real-Time Data Pipeline 
- SL API -> Kafka -> Spark Stream -> Cassandra/MongoDB 


## Installation and Setup 
1. install [uv](https://docs.astral.sh/uv/)
- inside project run **uv sync**

2. run **docker-compose up -d**
- after docker is running - run **docker ps** to ensure all the containers and services are running properly

3. inside the notebook directory run the following commands 
- **uv run jupyter lab** 

4. run all cassandra_init notebook to set up the cassandra database 

5. run the kafka notebook to process and store the stream data



