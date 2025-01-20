import os
import sys
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.transform_load_data import transform_load_data
#from utils.constants import API_KEY


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Instantiate the DAG
dag = DAG(
    'weather_dag',  # DAG ID
    default_args=default_args,  # Default arguments
    description='A simple ETL to extract weather information',  # DAG description
    schedule_interval='@daily',  # DAG schedule interval
    catchup=False  # Do not backfill missing runs
)

is_weather_api_ready = HttpSensor(
        task_id ='is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=c4e3eb072cf6f836d8bc055299416684',
        dag=dag
        )


extract_weather_data = HttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=c4e3eb072cf6f836d8bc055299416684',
        method = 'GET',
        response_filter= lambda r: json.loads(r.text),
        log_response=True,
        dag=dag
        )

transform_load_weather_data = PythonOperator(
        task_id= 'transform_load_weather_data',
        python_callable=transform_load_data,dag=dag
        )




is_weather_api_ready >> extract_weather_data >> transform_load_weather_data

