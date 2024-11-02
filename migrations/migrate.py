import logging
import os
import sys

import psycopg2
import time

db_name = os.environ["POSTGRES_DB"]
db_user = os.environ["POSTGRES_USER"]
db_password = os.environ["POSTGRES_PASSWORD"]
db_host = os.environ.get("POSTGRES_HOST", "localhost")
db_port = os.environ.get("POSTGRES_PORT", 5432)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def create_connection():
    while True:
        try:
            connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
            return connection
        except Exception as e:
            print(
                "Не удалось подключиться к базе данных, повторная попытка через 5 секунд..."
            )
            logging.error(e)
            time.sleep(5)


def main():
    connection = create_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(100) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """

    cursor.execute(create_table_query)
    connection.commit()

    logging.info("Таблица users была успешно создана или уже существует.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
