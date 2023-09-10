import psycopg2
from config import *


def creating_tables():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS contracts(
                        id SERIAL PRIMARY KEY,
                        contract_name VARCHAR(100) NOT NULL UNIQUE,
                        date_of_creation timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
                        date_of_signing timestamp with time zone,
                        status VARCHAR(100) DEFAULT 'Черновик'
                        );
                    CREATE TABLE IF NOT EXISTS projects (
                        id SERIAL PRIMARY KEY,
                        project_name VARCHAR(100) NOT NULL UNIQUE,
                        date_of_creation timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
                        contract_id INT,
                        CONSTRAINT FK_projects_contracts FOREIGN KEY (contract_id) REFERENCES contracts(id)
                        ON DELETE CASCADE
                        );
                    ALTER TABLE contracts ADD to_project VARCHAR(100) REFERENCES projects(project_name) 
                    ON DELETE CASCADE DEFAULT NULL;"""
            )
        return None

    except Exception as exc:
        return f'Возникла ошибка при создании таблиц в базе данных: {exc}'

    finally:
        if connection:
            connection.close()
