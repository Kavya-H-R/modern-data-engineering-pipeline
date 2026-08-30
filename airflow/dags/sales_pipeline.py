from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="sales_pipeline",
    description="Tiny sales data engineering pipeline",
    start_date=datetime(2026, 8, 29),
    schedule=None,
    catchup=False,
    tags=["sales", "learning"],
) as dag:

    validate_file = BashOperator(
        task_id="validate_file",
        bash_command="cd /opt/airflow/project && python src/validate.py",
    )

    spark_transform = BashOperator(
        task_id="spark_transform",
        bash_command="cd /opt/airflow/project && python src/transform.py",
    )

    load_database = BashOperator(
        task_id="load_database",
        bash_command="cd /opt/airflow/project && python src/load_postgres.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        dbt run \
        --project-dir /opt/airflow/project/dbt_project \
        --profiles-dir /opt/airflow/project/dbt_project
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        dbt test \
        --project-dir /opt/airflow/project/dbt_project \
        --profiles-dir /opt/airflow/project/dbt_project
        """,
    )

    validate_file >> spark_transform >> load_database >> dbt_run >> dbt_test