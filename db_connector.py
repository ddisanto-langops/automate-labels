import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv("./secrets.env")

# CONNECTION PARAMS
DB_NAME = "article_labels"
DB_USER = "langops_code_user"
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = "127.0.0.1"
DB_PORT = "5432"

class DatabaseConnector:
    def __init__(self):
        pass
    
    def insert_data(self, title, string):
        connection = None
        try:
            connection = psycopg2.connect(
                database = DB_NAME,
                user = DB_USER,
                password = DB_PASS,
                host = DB_HOST,
                port = DB_PORT
            )
            cursor = connection.cursor()

            sql_insert = """INSERT INTO article_data (article_title, data_string) VALUES (%s, %s);"""

            rows_inserted = 0
            for data_string in string:
                # The %s placeholders are safely replaced by the tuple
                cursor.execute(sql_insert, (title, data_string))
                rows_inserted += 1
        
            connection.commit()
            print(f"Successfully inserted {rows_inserted} rows for title: '{title}'")

            return "Connection Successful"
        
        except OperationalError as e:
            if connection:
                connection.rollback()
            return e
        
        except Exception as e:
            if connection:
                connection.rollback()
            return e
        
        finally:
            if connection:
                cursor.close()
                connection.close()