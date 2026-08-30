FROM apache/airflow:3.3.1-python3.12

USER root

RUN apt-get update \
    && apt-get install -y openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir \
    pyspark==4.2.0 \
    psycopg2-binary \
    dbt-postgres