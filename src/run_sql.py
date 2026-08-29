import sqlite3


DATABASE_FILE = "data/sales.db"
SQL_FILE = "sql/analysis.sql"


connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()


with open(SQL_FILE, "r") as file:
    query = file.read()


cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)


connection.close()