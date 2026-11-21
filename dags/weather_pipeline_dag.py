from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

PROJECT_DIR = '/opt/airflow/project'

with DAG(
    dag_id='winnipeg_weather_pipeline',
    default_args=default_args,
    description='A DAG to fetch and save Winnipeg weather data, load to s3 and transform with dbt',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['weather', 'winnipeg', 'portfolio'],
) as dag:
    
    extract_weather = BashOperator(
        task_id='extract_weather',
        bash_command=f"cd {PROJECT_DIR} && python3 extract_weather.py"
    )

    load_to_s3 = BashOperator(
        task_id='load_to_s3',
        bash_command=f"cd {PROJECT_DIR} && python3 load_to_s3.py",
    )

    transform_with_dbt = BashOperator(
        task_id='transform_with_dbt',
        bash_command='echo "In production, trigger dbt job via API"',
    )

    #dependency chain
    extract_weather >> load_to_s3 >> transform_with_dbt