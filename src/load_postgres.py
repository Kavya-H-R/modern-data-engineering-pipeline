import csv
import glob
import os

import psycopg2


TRANSFORMED_FOLDER = "data/transformed_sales"

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")


# Find the transformed CSV created by Spark
csv_files = glob.glob(f"{TRANSFORMED_FOLDER}/part-*.csv")

if not csv_files:
    raise FileNotFoundError("No transformed Spark output found.")

CSV_FILE = csv_files[0]


# Connect to PostgreSQL
connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()


# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER,
    customer_id INTEGER,
    product VARCHAR(100),
    quantity INTEGER,
    price INTEGER,
    order_date DATE,
    total_amount INTEGER
)
""")


# Keep this tiny batch pipeline idempotent
cursor.execute("DELETE FROM sales")


# Load Spark-transformed data
with open(CSV_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO sales (
                order_id,
                customer_id,
                product,
                quantity,
                price,
                order_date,
                total_amount
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row["order_id"]),
            int(row["customer_id"]),
            row["product"],
            int(row["quantity"]),
            int(row["price"]),
            row["order_date"],
            int(row["total_amount"])
        ))


connection.commit()

cursor.close()
connection.close()

print("Transformed Spark data loaded into PostgreSQL successfully.")