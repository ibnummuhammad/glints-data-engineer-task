from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def _extract_data():
    sql_stmt = "SELECT * FROM sales"
    pg_hook = PostgresHook(postgres_conn_id="postgres_src", schema="airflow")
    pg_conn = pg_hook.get_conn()
    cursor = pg_conn.cursor()
    cursor.execute(sql_stmt)
    data_raw = cursor.fetchall()
    data = []
    for row in data_raw:
        data.append(tuple((row[0], row[1], row[2], row[3].strftime("%Y-%m-%d"))))
    data = str(data)
    data = data[1:-1]
    return data


with DAG(
    "data-pipeline",
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
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
        do_xcom_push=True,
    )
    load_data = PostgresOperator(
        task_id="load_data",
        postgres_conn_id="postgres_dst",
        sql="""INSERT INTO sales VALUES {{ ti.xcom_pull(task_ids='extract_data', key='return_value') }};""",
    )
    end_task = DummyOperator(task_id="end")

start_task >> extract_data >> load_data >> end_task
