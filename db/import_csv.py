import csv
import os
import psycopg2
from psycopg2 import sql

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
path_csv = os.environ.get('CSV_PATH')

with open(path_csv, newline='') as csvfile:
    reader = csv.reader(csvfile)

    # NOTE: Skip header
    next(reader)

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database=db_name,
        user=user,
        password=password,
    )
    cursor = conn.cursor()
    for row in reader:
        for i, col in enumerate(row):
            if col == '':
                row[i] = None

        cursor.execute(sql.SQL(
            "INSERT INTO conflict (country, admin1, population, events, score)  VALUES (%s, %s, %s, %s, %s)"), row)
    conn.commit()
    cursor.close()
    conn.close()
