import psycopg2
from faker import Faker


def seed_db():
    # Database connection parameters
    dbname = "user_tasks_db"
    user = "postgres"
    host = "localhost"
    port = "5432"

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
        cur = conn.cursor()

        # Instantiate Faker
        fake = Faker()

        # Seed the status table
        statuses = ["new", "in progress", "completed"]
        for status in statuses:
            cur.execute(
                "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
                (status,),
            )

        # Seed the users table
        for _ in range(10):
            fullname = fake.name()
            email = fake.unique.email()
            cur.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s);",
                (fullname, email),
            )

        # Seed the tasks table
        cur.execute("SELECT id FROM users;")
        user_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT id FROM status;")
        status_ids = [row[0] for row in cur.fetchall()]

        for _ in range(30):
            title = fake.sentence(nb_words=6)
            description = fake.text()
            status_id = fake.random_element(elements=status_ids)
            user_id = fake.random_element(elements=user_ids)
            cur.execute(
                "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
                (title, description, status_id, user_id),
            )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

        print("Database seeded successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    seed_db()
