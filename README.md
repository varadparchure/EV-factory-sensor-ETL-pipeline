# End-to-End Data Pipeline for EV Factory Sensor ETL Pipeline

## Overview

This project demonstrates a complete end-to-end data pipeline for a smart EV factory. It simulates sensor data from various factory stations, streams the data via Apache Kafka (managed by Zookeeper), processes it with an Apache Airflow-managed ETL pipeline, stores the transformed data in a PostgreSQL database, and exposes the data via a FastAPI service. Visualization can be achieved through tools like Tableau.

For more detailed information on the architecture, design decisions, and implementation, please refer to the accompanying PDF documentation files.

![image](https://github.com/user-attachments/assets/1035e383-a6e6-4969-9c60-f39271dd8a76)

## Features

- **Synthetic Data Generation:**  
  A simulator continuously generates synthetic sensor data (e.g., chassis, battery, paint, quality) and publishes it to Kafka topics.

- **Data Streaming:**  
  Apache Kafka (coordinated by Zookeeper) acts as the message broker to decouple data production from consumption.

- **ETL Processing with Airflow:**  
  An Airflow DAG extracts data from multiple Kafka topics, applies transformations (such as rounding values and adding timestamps), and loads the processed data into PostgreSQL.

- **Data Access & Visualization:**  
  A FastAPI service provides a JSON API to query the sensor data. Visualization can be performed using Tableau or a custom dashboard.

## Usage Instructions

### 1. Build and Start All Containers

In your project directory, run the following command to build and start all the Docker containers (for Kafka, Zookeeper, PostgreSQL, Airflow, the Simulator, and the FastAPI service):

```bash
docker-compose up -d
```

### 2. Access the Airflow UI

After starting the containers, open your web browser and navigate to:
```bash
http://localhost:8080
```

Use the provided credentials (or create/update the admin user if needed) to log in and monitor/trigger the ETL jobs.

## 3. Trigger the ETL Pipeline

Within the Airflow UI, locate the ETL DAG (named `factory_etl`) and trigger it manually, or wait for its scheduled run. This job will extract data from Kafka, transform it, and load it into the PostgreSQL database.

## 4. View the Sensor Data API

To view the sensor data in JSON format, open your browser or use a command-line tool (e.g., `curl`) and navigate to:

```bash
http://localhost:8000/sensor-data
```


This endpoint returns the latest sensor data as JSON.

## 5. Connect Tableau (Optional)

For visualization, you can connect Tableau directly to the PostgreSQL database using the following connection details:

- **Server:** `localhost`
- **Port:** `5432`
- **Database:** `factory_db`
- **Username:** `factory_user`
- **Password:** `factory_pass`

## Additional Information

For more detailed technical information and insights on the project architecture and design, please refer to the attached PDF documentation files.





