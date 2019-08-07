"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.slack_operator import SlackAPIPostOperator
from airflow.hooks.base_hook import BaseHook

from sqlalchemy.orm.session import sessionmaker


from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

import os
APP_PATH = os.getenv("APP_PATH")

import sys
sys.path.append(APP_PATH)

from huey.importer import import_buoy_realtime_wave_detail, \
    import_buoy_raw_spectral_wave_data

from huey.utils import get_db_session

from pprint import pprint

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 24),
    'email': ['heyhueyapp@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

def send_slack_alert():
    slack_token = BaseHook.get_connection('slack').password
    alert = SlackAPIPostOperator(
        task_id='huey_import_buoy_data_success',
        token=slack_token,
        text='Buoy Data Import Success.',
        channel='#huey_data_import',
        username='heyhueyapp'
    )
    return alert.execute(context=None)

# @hourly
dag = DAG(
    'huey_import_buoy_data', \
    default_args=default_args, \
    schedule_interval="0 * * * *", \
    catchup=False,
    on_success_callback=send_slack_alert
)

def run_import_buoy_realtime_wave_detail(**kwargs):
    db_session = get_db_session()
    import_buoy_realtime_wave_detail(db_session)

t3 = PythonOperator(
    task_id='import_buoy_realtime_wave_detail',
    python_callable=run_import_buoy_realtime_wave_detail,
    dag=dag,
)

def run_import_buoy_raw_spectral_wave_data(**kwargs):
    db_session = get_db_session()
    import_buoy_raw_spectral_wave_data(db_session)

t4 = PythonOperator(
    task_id='import_buoy_raw_spectral_wave_data',
    python_callable=run_import_buoy_raw_spectral_wave_data,
    dag=dag,
)
