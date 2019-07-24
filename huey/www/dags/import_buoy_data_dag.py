"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta

import sys
sys.path.append("..")
from app.importer import import_buoy_realtime_wave_detail, \
    import_raw_spectral_wave_data

from pprint import pprint

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'huey_import_buoy_data', default_args=default_args, schedule_interval=timedelta(days=1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)


def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'

t2 = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

def run_import_buoy_realtime_wave_detail(ds, **kwargs):
    import_buoy_realtime_wave_detail()

t3 = PythonOperator(
    task_id='import_buoy_realtime_wave_detail',
    provide_context=True,
    python_callable=run_import_buoy_realtime_wave_detail,
    dag=dag,
)

def run_import_buoy_raw_spectral_wave_data(ds, **kwargs):
    import_raw_spectral_wave_data()

t3 = PythonOperator(
    task_id='import_buoy_raw_spectral_wave_data',
    provide_context=True,
    python_callable=run_import_buoy_raw_spectral_wave_data,
    dag=dag,
)
