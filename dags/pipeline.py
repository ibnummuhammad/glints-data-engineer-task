from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator


with DAG(
    "data_pipeline",
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    start_date=datetime(2022, 8, 5),
    catchup=False,
) as dag:
    start_task = DummyOperator(task_id="start")
    print_hello_world = BashOperator(
        task_id="print_hello_world", bash_command='echo "HelloWorld!"'
    )
    end_task = DummyOperator(task_id="end")

start_task >> print_hello_world
print_hello_world >> end_task
