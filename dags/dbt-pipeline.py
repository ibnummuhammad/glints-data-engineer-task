from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator


with DAG(
    "dbt-pipeline",
    default_args={
        "depends_on_past": False,
        "retries": 0,
    },
    description="A simple data pipelining DAG",
    dagrun_timeout=timedelta(minutes=3),
    start_date=datetime(2022, 8, 5),
    catchup=False,
) as dag:
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

start_task >> end_task
