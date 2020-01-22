# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_dag.buoy_data.ipynb (unless otherwise specified).

__all__ = ['default_args', 'dag', 'run_import_buoy_realtime_wave_detail', 't1']

# Cell
from ..imports import *
from .airflow_imports import *

# Cell
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

# Cell
# @hourly
dag = DAG(
    'huey_import_buoy_data', \
    default_args=default_args, \
    schedule_interval="0 * * * *", \
    catchup=False
)

# Cell
from ..data.importer.buoy_data import import_buoy_realtime_wave_detail

# Cell
def run_import_buoy_realtime_wave_detail():
    station_id = "46025"
    import_buoy_realtime_wave_detail(station_id)

# Cell
t1 = PythonOperator(
    task_id='import_buoy_realtime_wave_detail',
    python_callable=run_import_buoy_realtime_wave_detail,
    dag=dag)