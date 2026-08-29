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

    load_database = BashOperator(
        task_id="load_database",
        bash_command="cd /opt/airflow/project && python src/load_sqlite.py",
    )

    run_sql = BashOperator(
        task_id="run_sql",
        bash_command="cd /opt/airflow/project && python src/run_sql.py",
    )

    validate_file >> load_database >> run_sql