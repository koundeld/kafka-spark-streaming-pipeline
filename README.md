# Streaming Pipeline with Kafka + Spark Structured Streaming + BigQuery

## Overview:
This project demonstrates a real-time **taxi ride streaming pipeline**.  
- **Producer**: Simulates taxi ride events and publishes them to Kafka.  
- **Spark Structured Streaming**: Consumes and processes events, adds windowed aggregations, and writes results to **BigQuery** for analytics.  

---

## Architecture Diagram
<img width="951" height="144" alt="streaming_architecture" src="https://github.com/user-attachments/assets/962c1fc9-43e9-4885-a0f6-5da8b9a147ac" />

---

## Tech Stack
- **Kafka** (event streaming backbone)  
- **Spark Structured Streaming** (real-time data processing)  
- **Python** (event simulation + Spark jobs)  
- **BigQuery** (cloud data warehouse)  
- **Docker** (Kafka/Zookeeper containerized setup) 

---

## Event Simulation
- A Python script generates **fake taxi ride events** every 10 seconds.  
- Each event contains attributes such as:  
  - `driver_id` (used as Kafka message key)  
  - `pickup/drop boroughs`  
  - `trip_distance` (1–20 km)  
  - `passenger_count` (1–4)  
  - `fare_amount` (randomized within range)  
  - `payment_type` (Cash/Card)  
- Events are serialized as JSON and published to a Kafka topic.

---

## Pipeline FLow
1. **Producer** → Publishes simulated events to a Kafka topic.  
2. **Spark Structured Streaming** →  
   - Consumes messages from Kafka.  
   - Parses JSON values using a defined schema.  
   - Adds an hourly window column (`event_time`).  
   - Writes streaming data into a **BigQuery table**.

---

## Setup Instructions
1. **Start Kafka locally (via Docker Compose):**  
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).  
   - Use the provided [`docker-compose.yml`](./docker-compose.yml) in this repo.
   - Run `docker-compose up -d` to start **Kafka + Zookeeper**.  
2. **Create a Kafka topic:**  
   ``` 
   bash kafka-topics --create --topic taxi_rides --bootstrap-server localhost:9092
   ```
3. **Run the event Producer***
    ``` 
    bash python producer/cab_data_producer.py
    ```
4.	**Run the streaming job (with Kafka connector):**
    ```
    bash spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 jobs/streaming_app.py
    ```
5.  **BigQuery integration:**
    - Create a service account with BigQuery read/write access.
    - Download the key JSON and set GOOGLE_APPLICATION_CREDENTIALS.
    - Ensure dataset/table exist before running.

---

# Repository Structure
```
.
├── producer/        # Python event generator
├── jobs/            # Spark structured streaming jobs
├── docker-compose.yml
├── README.md
└── requirements.txt
```
---

# Disclaimer
This project is for learning and demonstration purposes only.
