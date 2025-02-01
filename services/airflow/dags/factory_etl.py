from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import json
import psycopg2
from kafka import KafkaConsumer

def etl_task():
    # Create a Kafka consumer that listens to all our topics
    consumer = KafkaConsumer(
        'chassis_topic', 'battery_topic', 'paint_topic', 'quality_topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='airflow_etl_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    # Connect to Postgres (using the Docker service name "postgres")
    conn = psycopg2.connect(
        host="postgres",
        database="factory_db",
        user="factory_user",
        password="factory_pass"
    )
    cur = conn.cursor()

    # Create a table if it doesn't exist
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

    # Process a few messages for demonstration
    messages_processed = 0
    for message in consumer:
        data = message.value
        insert_query = "INSERT INTO sensor_data (station, data) VALUES (%s, %s);"
        cur.execute(insert_query, (data.get('station'), json.dumps(data)))
        conn.commit()
        messages_processed += 1
        if messages_processed >= 5:
            break

    cur.close()
    conn.close()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('factory_etl', default_args=default_args, schedule_interval=timedelta(minutes=5))

etl = PythonOperator(
    task_id='run_etl',
    python_callable=etl_task,
    dag=dag
)
