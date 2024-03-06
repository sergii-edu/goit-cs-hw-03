from db import db_connection


@db_connection
def get_tasks_by_user(cur, user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    return cur.fetchall()


@db_connection
def get_tasks_by_status(cur, status_name):
    cur.execute(
        """
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = %s)
    """,
        (status_name,),
    )
    return cur.fetchall()


@db_connection
def update_task_status(cur, task_id, new_status):
    cur.execute(
        """
    UPDATE tasks 
    SET status_id = (SELECT id FROM status WHERE name = %s) 
    WHERE id = %s
    """,
        (new_status, task_id),
    )


@db_connection
def get_users_with_no_tasks(cur):
    cur.execute(
        """
    SELECT * FROM users 
    WHERE id NOT IN (SELECT user_id FROM tasks)
    """
    )
    return cur.fetchall()


@db_connection
def add_task_for_user(cur, user_id, title, description, status_id):
    cur.execute(
        """
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (%s, %s, %s, %s)
    """,
        (title, description, status_id, user_id),
    )


@db_connection
def get_uncompleted_tasks(cur):
    cur.execute(
        """
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """
    )
    return cur.fetchall()


@db_connection
def delete_task(cur, task_id):
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))


@db_connection
def find_users_by_email(cur, email_pattern):
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    return cur.fetchall()


@db_connection
def update_user_name(cur, user_id, new_name):
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))


@db_connection
def get_task_count_by_status(cur):
    cur.execute(
        """
    SELECT status.name, COUNT(tasks.id) 
    FROM status 
    LEFT JOIN tasks ON status.id = tasks.status_id 
    GROUP BY status.name
    """
    )
    return cur.fetchall()


@db_connection
def get_tasks_for_email_domain(cur, domain):
    cur.execute(
        """
    SELECT tasks.* FROM tasks 
    JOIN users ON tasks.user_id = users.id 
    WHERE users.email LIKE %s
    """,
        ("%" + domain,),
    )
    return cur.fetchall()


@db_connection
def get_tasks_without_description(cur):
    cur.execute(
        "SELECT id, title FROM tasks WHERE description IS NULL OR description = ''"
    )
    return cur.fetchall()


@db_connection
def get_in_progress_tasks_and_users(cur):
    cur.execute(
        """
    SELECT users.fullname, tasks.title, tasks.description FROM users 
    INNER JOIN tasks ON users.id = tasks.user_id 
    WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress')
    """
    )
    return cur.fetchall()


@db_connection
def get_users_and_their_task_counts(cur):
    cur.execute(
        """
    SELECT users.fullname, COUNT(tasks.id) 
    FROM users 
    LEFT JOIN tasks ON users.id = tasks.user_id 
    GROUP BY users.fullname
    """
    )
    return cur.fetchall()
