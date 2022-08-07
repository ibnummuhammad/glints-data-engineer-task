import csv
from datetime import datetime, timedelta
import json

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


def _extract_table_source():
    sql_stmt = "SELECT * FROM sales"
    pg_hook = PostgresHook(postgres_conn_id="postgres_src", schema="airflow")
    pg_conn = pg_hook.get_conn()
    cursor = pg_conn.cursor()
    cursor.execute(sql_stmt)
    data_raw = cursor.fetchall()
    data = []
    for row in data_raw:
        data.append(
            {
                "id": row[0],
                "quantity": row[1],
                "price": row[2],
                "date": row[3].strftime("%Y-%m-%d"),
            }
        )
    data = json.dumps(data)
    return data


with DAG(
    "pipeline",
    default_args={
        "depends_on_past": False,
        "retries": 0,
    },
    description="A simple tutorial DAG",
    dagrun_timeout=timedelta(minutes=60),
    start_date=datetime(2022, 8, 5),
    catchup=False,
) as dag:
    start_task = DummyOperator(task_id="start")
    create_table_source = PostgresOperator(
        task_id="create_table_source",
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
    import_table_source = PostgresOperator(
        task_id="import_table_source",
        postgres_conn_id="postgres_src",
        sql="""
            COPY sales(id, quantity, price, date)
            FROM '/opt/data/sales_september_2019.csv' DELIMITER ',' CSV HEADER;
        """,
    )
    extract_table_source = PythonOperator(
        task_id="extract_table_source",
        python_callable=_extract_table_source,
        do_xcom_push=True,
    )
    end_task = DummyOperator(task_id="end")

(
    start_task
    >> create_table_source
    >> import_table_source
    >> extract_table_source
    >> end_task
)
