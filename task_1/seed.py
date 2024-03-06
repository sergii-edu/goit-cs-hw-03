from faker import Faker
import random

from db import db_connection


@db_connection
def create_tables(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
        INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed') ON CONFLICT (name) DO NOTHING;
        """
    )


@db_connection
def remove_tables(cur):
    cur.execute(
        """
        DROP TABLE IF EXISTS tasks;
        DROP TABLE IF EXISTS status;
        DROP TABLE IF EXISTS users;
        """
    )


@db_connection
def populate_database(cur):
    fake = Faker()

    for _ in range(10):
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email)
        )

    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]
    status_ids = [1, 2, 3]  # ID для статусів 'new', 'in progress', 'completed'

    def sometimes_empty_text(max_length):
        probability_of_empty = 0.3
        if random.random() < probability_of_empty:
            return ""
        else:
            return fake.text(max_length)

    for _ in range(20):
        title = fake.text(24)
        description = sometimes_empty_text(48)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id),
        )
