import sqlite3
import csv


CSV_FILE = "data/sales.csv"
DATABASE_FILE = "data/sales.db"


# Connect to SQLite database
connection = sqlite3.connect(DATABASE_FILE)

cursor = connection.cursor()


# Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    order_id INTEGER,
    customer_id INTEGER,
    product TEXT,
    quantity INTEGER,
    price INTEGER,
    order_date TEXT,
    total_amount INTEGER
)
""")
# Clear existing rows to prevent duplicates on pipeline reruns
cursor.execute("DELETE FROM sales")

# Read sales.csv
with open(CSV_FILE, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:

        total_amount = int(row["quantity"]) * int(row["price"])

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
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row["order_id"]),
            int(row["customer_id"]),
            row["product"],
            int(row["quantity"]),
            int(row["price"]),
            row["order_date"],
            total_amount
        ))


connection.commit()
connection.close()

print("Sales data loaded successfully.")