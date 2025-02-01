from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import json
import psycopg2
from kafka import KafkaConsumer

def transform_data(message_value):
    """
    Apply simple transformations to the data.
    This function can be extended as needed.
    """
    # For example, ensure numeric fields are rounded and add a processing timestamp.
    station = message_value.get("station", "unknown")

    if station == "battery":
        # Round the voltage value to an integer
        if "voltage" in message_value:
            message_value["voltage"] = round(message_value["voltage"])
    elif station == "chassis":
        # Round the torque to one decimal place
        if "torque" in message_value:
            message_value["torque"] = round(message_value["torque"], 1)
    elif station == "paint":
        # Round the booth_humidity to an integer
        if "booth_humidity" in message_value:
            message_value["booth_humidity"] = round(message_value["booth_humidity"])
    # Add a new field to indicate when processing occurred.
    message_value["processed_at"] = datetime.now().isoformat()
    return message_value

def etl_task():
    # Create a Kafka consumer subscribing to multiple topics.
    consumer = KafkaConsumer(
        'chassis_topic', 'battery_topic', 'paint_topic', 'quality_topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='airflow_etl_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    # Connect to Postgres (using the Docker service name "postgres").
    conn = psycopg2.connect(
        host="postgres",
        database="factory_db",
        user="factory_user",
        password="factory_pass"
    )
    cur = conn.cursor()

    # Create a table if it doesn't exist.
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id SERIAL PRIMARY KEY,
        station VARCHAR(50),
        data JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    cur.execute(create_table_query)
    conn.commit()

    messages_processed = 0
    # Process messages for demonstration.
    for message in consumer:
        data = message.value
        # Apply transformations.
        transformed_data = transform_data(data)
        # Insert the transformed data into Postgres.
        insert_query = "INSERT INTO sensor_data (station, data) VALUES (%s, %s);"
        cur.execute(insert_query, (transformed_data.get('station'), json.dumps(transformed_data)))
        conn.commit()
        messages_processed += 1
        if messages_processed >= 5:
            break

    cur.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('factory_etl',
          default_args=default_args,
          schedule_interval=timedelta(minutes=5),
          catchup=False)

etl_operator = PythonOperator(
    task_id='run_etl_task',
    python_callable=etl_task,
    dag=dag
)
