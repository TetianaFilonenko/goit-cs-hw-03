import psycopg2
from tabulate import tabulate

# Database connection parameters
dbname = "user_tasks_db"
user = "postgres"
host = "localhost"
port = "5432"


def execute_queries():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
        cur = conn.cursor()

        # 1. Get all tasks for a specific user
        user_id = 1
        cur.execute("SELECT * FROM tasks WHERE user_id = %s;", (user_id,))
        result = cur.fetchall()
        print(f"All tasks for user_id {user_id}")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 2. Select tasks with a specific status
        status = "new"
        cur.execute(
            "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s);",
            (status,),
        )
        result = cur.fetchall()
        print(f"\nTasks with status {status}")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 3. Update the status of a specific task
        task_id = 1
        new_status = "in progress"
        cur.execute(
            "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s;",
            (new_status, task_id),
        )
        conn.commit()
        print(f"\nUpdated task_id {task_id} to status {new_status}")

        # 4. Get list of users with no tasks
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
        result = cur.fetchall()
        print("\nUsers with no tasks")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 5. Add a new task for a specific user
        new_task = ("New Task Title", "Task description", "new", 1)
        cur.execute(
            """
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
            """,
            new_task,
        )
        conn.commit()
        print(f"\nAdded a new task for user_id {new_task[3]}")

        # 6. Get all tasks that are not completed
        cur.execute(
            "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');"
        )
        result = cur.fetchall()
        print("\nTasks that are not completed")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 7. Delete a specific task
        delete_task_id = 2
        cur.execute("DELETE FROM tasks WHERE id = %s;", (delete_task_id,))
        conn.commit()
        print(f"\nDeleted task_id {delete_task_id}")

        # 8. Find users with a specific email
        email_pattern = "%@example.com"
        cur.execute("SELECT * FROM users WHERE email LIKE %s;", (email_pattern,))
        result = cur.fetchall()
        print(f"\nUsers with email pattern {email_pattern}")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 9. Update a user's name
        update_user_id = 1
        new_fullname = "Updated User Name"
        cur.execute(
            "UPDATE users SET fullname = %s WHERE id = %s;",
            (new_fullname, update_user_id),
        )
        conn.commit()
        print(f"\nUpdated fullname for user_id {update_user_id} to {new_fullname}")

        # 10. Get the number of tasks for each status
        cur.execute(
            "SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name;"
        )
        result = cur.fetchall()
        print("\nNumber of tasks for each status")
        print(tabulate(result, headers=["Status", "Task Count"], tablefmt="pretty"))

        # 11. Get tasks assigned to users with a specific email domain
        cur.execute(
            """
            SELECT tasks.* FROM tasks
            JOIN users ON tasks.user_id = users.id
            WHERE users.email LIKE %s;
            """,
            (email_pattern,),
        )
        result = cur.fetchall()
        print(f"\nTasks assigned to users with email pattern {email_pattern}")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 12. Get tasks without a description
        cur.execute("SELECT * FROM tasks WHERE description IS NULL;")
        result = cur.fetchall()
        print("\nTasks without a description")
        print(
            tabulate(
                result, headers=[desc[0] for desc in cur.description], tablefmt="pretty"
            )
        )

        # 13. Select users and their tasks that are 'in progress'
        cur.execute(
            """
            SELECT users.fullname, tasks.title FROM tasks
            JOIN users ON tasks.user_id = users.id
            WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
            """
        )
        result = cur.fetchall()
        print("\nUsers and their tasks that are 'in progress'")
        print(tabulate(result, headers=["User", "Task Title"], tablefmt="pretty"))

        # 14. Get users and the count of their tasks
        cur.execute(
            """
            SELECT users.fullname, COUNT(tasks.id) FROM users
            LEFT JOIN tasks ON users.id = tasks.user_id
            GROUP BY users.fullname;
            """
        )
        result = cur.fetchall()
        print("\nUsers and the count of their tasks")
        print(tabulate(result, headers=["User", "Task Count"], tablefmt="pretty"))

        # Close the cursor and connection
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    execute_queries()
