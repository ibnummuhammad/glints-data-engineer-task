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
    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data,
        do_xcom_push=True,
    )
    load_data = PostgresOperator(
        task_id="load_data",
        postgres_conn_id="postgres_dst",
        sql="""INSERT INTO sales VALUES
                ({{ ti.xcom_pull(task_ids='extract_data', key='return_value') }});""",
    )
    end_task = DummyOperator(task_id="end")

(
    start_task
    >> create_table_source
    >> import_table_source
    >> extract_data
    >> load_data
    >> end_task
)
