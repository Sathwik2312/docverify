import psycopg2

def db_connection():
    return psycopg2.connect(
        host="localhost",
        database="dvs",
        user="postgres",
        password="1234"
    )

def return_db_connection(conn):
    if conn:
        conn.close()