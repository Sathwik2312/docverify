import psycopg2

db_host = "dpg-d8el10l7vvec73dpnfjg-a"
db_user = "docverify_user"
db_password = "u4fR0KOrvJA4FITyAbzrUBOs7HeP9SVD"
db_port = "5432"
db_name = "docverify_tskd"

def db_connection():
    try:
        connection = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            dbname=db_name,
            port=db_port
        )
        return connection

    except Exception as e:
        print("Database connection failed:", e)
        return None