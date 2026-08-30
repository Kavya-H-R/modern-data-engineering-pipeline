# Sales Data Engineering Pipeline

An end-to-end data engineering project that demonstrates ingestion, validation, distributed transformation, database loading, analytical modeling, data-quality testing, orchestration, and containerization.

## Architecture

```text
sales.csv
    |
    v
Python Validation
    |
    v
PySpark Transformation
    |
    v
PostgreSQL
    |
    v
dbt Transformation
    |
    v
dbt Data Quality Tests
```

Apache Airflow orchestrates the complete workflow, while Docker Compose provides the local runtime environment for Airflow and PostgreSQL.

## Tech Stack

- Python
- PySpark
- PostgreSQL
- dbt
- Apache Airflow
- Docker & Docker Compose
- Git & GitHub

## Pipeline Flow

### 1. Source Data

The pipeline starts with a CSV sales dataset containing:

- order ID
- customer ID
- product
- quantity
- price
- order date

### 2. Data Validation

`src/validate.py` validates the incoming file before downstream processing begins.

Current validations include:

- expected column structure
- non-empty dataset

If validation fails, downstream Airflow tasks are not executed.

### 3. PySpark Transformation

`src/transform.py` reads the source CSV using PySpark and calculates:

```text
total_amount = quantity * price
```

The transformed dataset is written to a generated output directory for the loading stage.

### 4. PostgreSQL Load

`src/load_postgres.py` loads the Spark-transformed data into PostgreSQL.

The load is designed to be repeatable for this batch pipeline by clearing the target table before reloading the current dataset.

Database configuration is supplied through environment variables rather than hardcoded credentials.

### 5. dbt Transformation

dbt treats the PostgreSQL `sales` table as a source and builds an analytical model:

```text
customer_sales_summary
```

The model calculates total spending for each customer.

Example:

```text
customer_id | total_spent
------------|------------
101         | 50800
102         | 1600
103         | 1500
```

### 6. Data Quality Testing

dbt tests validate the analytical output.

Current tests include:

- `customer_id` is not null
- `customer_id` is unique
- `total_spent` is not null

This ensures that successful task execution alone is not treated as proof of correct data.

### 7. Airflow Orchestration

Apache Airflow manages task dependencies:

```text
validate_file
      |
      v
spark_transform
      |
      v
load_database
      |
      v
dbt_run
      |
      v
dbt_test
```

A downstream task executes only after its required upstream task succeeds.

## Project Structure

```text
sales-data-engineering-pipeline/
|
|-- airflow/
|   `-- dags/
|       `-- sales_pipeline.py
|
|-- data/
|   `-- sales.csv
|
|-- dbt_project/
|   |-- models/
|   |   |-- customer_sales_summary.sql
|   |   |-- schema.yml
|   |   `-- sources.yml
|   |-- dbt_project.yml
|   `-- profiles.yml
|
|-- src/
|   |-- validate.py
|   |-- transform.py
|   `-- load_postgres.py
|
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yaml
|-- requirements.txt
`-- README.md
```

Generated Spark outputs, dbt artifacts, Python cache files, local databases, virtual environments, and environment-variable files are excluded from Git.

## Running the Pipeline

### Prerequisites

Install:

- Git
- Docker Desktop

### 1. Clone the repository

```bash
git clone <repository-url>
cd sales-data-engineering-pipeline
```

### 2. Create `.env`

Create a `.env` file in the project root:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=sales_db
POSTGRES_USER=sales_user
POSTGRES_PASSWORD=<your-local-password>
```

The `.env` file is excluded from Git.

### 3. Build and start the services

```bash
docker compose up -d --build
```

### 4. Open Airflow

Open:

```text
http://localhost:8080
```

Trigger the `sales_pipeline` DAG from the Airflow UI.

### 5. Verify PostgreSQL Output

The pipeline creates the transformed sales data in PostgreSQL and dbt creates the customer-level analytical summary.

## Engineering Concepts Demonstrated

This project demonstrates several foundational data-engineering concepts:

- ETL/ELT pipeline design
- data validation
- distributed data processing with Spark
- relational database loading
- analytical SQL transformations
- data-quality testing
- workflow orchestration
- task dependency management
- fail-fast pipeline behavior
- basic batch idempotency
- environment-based configuration
- containerization
- Docker service networking
- reproducible local environments
- separation of source code and generated artifacts

## Current Scope

This project intentionally uses a small local dataset so that the focus remains on understanding the interaction between the major components of a modern data pipeline.

PySpark and Airflow are intentionally used even though the dataset itself does not require distributed processing or workflow orchestration at this scale.

## Future Improvements

Potential production-oriented extensions include:

- incremental ingestion
- object/cloud storage
- schema evolution handling
- stronger data contracts
- Airflow retries and alerting
- improved idempotent loading strategies
- partitioned processing
- CI/CD with GitHub Actions
- automated unit/integration tests
- observability and monitoring
- secrets management
- larger-scale datasets
