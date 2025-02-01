from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def etl_task():
    # Placeholder for the ETL logic.
    # Here is where you would connect to Kafka, read messages, and insert them into Postgres.
    print("ETL task running: This is where data would be processed.")

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
