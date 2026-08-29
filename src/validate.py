import csv

FILE_PATH = "data/sales.csv"

REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "product",
    "quantity",
    "price",
    "order_date"
]


def validate_file():

    with open(FILE_PATH, "r") as file:
        reader = csv.DictReader(file)

        # Check required columns
        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError("Invalid columns in sales.csv")

        # Read rows
        rows = list(reader)

        # Check file is not empty
        if len(rows) == 0:
            raise ValueError("sales.csv contains no data")

        print(f"Validation successful: {len(rows)} records found.")


if __name__ == "__main__":
    validate_file()
