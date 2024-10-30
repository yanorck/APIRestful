import psycopg2
import os
import time

# Remove +psycopg2 se for usar psycopg2.connect
DATABASE_URL = os.getenv("DATABASE_URL").replace("+psycopg2", "")

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            break
        except psycopg2.OperationalError:
            print("Database not ready, retrying...")
            time.sleep(1)

wait_for_db()
