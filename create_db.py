import psycopg2
from psycopg2 import OperationalError, errors

def create_connection():
    try:
        conn = psycopg2.connect(
            database="bazy_danych_warsztat",
            user="postgres",
            password="coderslab",
            host="127.0.0.1",
            port="5433"
        )
        return conn
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except errors.DuplicateTable:
        print("Table already exists")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        c.close()

def main():
    database_connection = create_connection()
    if database_connection is not None:
        # Utwórz tabelę użytkowników
        create_table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            hashed_password VARCHAR(80) NOT NULL
        );
        """
        create_table(database_connection, create_table_users)

        # Utwórz tabelę wiadomości
        create_table_messages = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            from_id INTEGER NOT NULL REFERENCES users(id),
            to_id INTEGER NOT NULL REFERENCES users(id),
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            text VARCHAR(255) NOT NULL
        );
        """
        create_table(database_connection, create_table_messages)

        database_connection.commit()
        database_connection.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
