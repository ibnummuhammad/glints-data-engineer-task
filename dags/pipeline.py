from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    "pipeline",
    default_args={
        "depends_on_past": False,
        "retries": 1,
    },
    description="A simple tutorial DAG",
    start_date=datetime(2022, 8, 5),
    catchup=False,
) as dag:
    start_task = DummyOperator(task_id="start")
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_src",
        sql="""
            CREATE TABLE IF NOT EXISTS sales(
                id SERIAL,
                quantity INT,
                price INT,
                date DATE,
                PRIMARY KEY (id)
            );
        """,
    )
    end_task = DummyOperator(task_id="end")

start_task >> create_table >> end_task
