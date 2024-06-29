import psycopg2
from psycopg2 import sql


def create_db():
    # Database connection parameters
    dbname = "user_tasks_db"
    user = "postgres"
    host = "localhost"
    port = "5432"

    # Connect to the PostgreSQL server
    conn = psycopg2.connect(dbname="postgres", user=user, host=host, port=port)
    conn.autocommit = True
    cur = conn.cursor()
    # Drop the existing database if it exists
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(dbname)))

    # Create the database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))

    # Close the initial connection
    cur.close()
    conn.close()

    # Reconnect to the new database
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()

    # Read the SQL script for creating the database tables
    with open('create_tables.sql', 'r') as f:
        sql_script = f.read()

    # Execute the script to create tables in the database
    cur.execute(sql_script)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    print("Database and tables created successfully.")


if __name__ == "__main__":
    create_db()
