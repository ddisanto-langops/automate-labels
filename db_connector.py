import os
import sqlite3

class DatabaseConnection:
    """
    Class DatabaseConnection represents a connection to a local sqlite database.
    """
    def __init__(self):
        try:
            self.APP_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Gets the directory of the current script
            self.DB_FILE = os.path.join(self.APP_FOLDER, 'temp.db')
            self.CONNECTION = sqlite3.connect(self.DB_FILE)
            self.CURSOR = self.CONNECTION.cursor()
            print(f"✅ Connected to SQLite database file: {self.DB_FILE}")
            
        
        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            return error
    

    def close_connection(self):
        if self.CONNECTION:
            self.CONNECTION.close()
        print("Connection closed")
        
    
    def insert_data(self, title: str, data: list):
        """inserts article data."""
        # Create the Table (if it doesn't exist)
        self.CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS article_data (
                    id INTEGER PRIMARY KEY,
                    article_title TEXT NOT NULL,
                    data_string TEXT NOT NULL
                );
            """)
        
        sql_insert = "INSERT INTO article_data (article_title, data_string) VALUES (?, ?)"

        rows_inserted = 0
        for data_string in data:
            self.CURSOR.execute(sql_insert, (title, data_string))
            rows_inserted += 1

        self.CONNECTION.commit()
        print(f"Successfully inserted {rows_inserted} rows into SQLite.")

    
    def retreive_strings(self, title) -> list[str]:
        try:
            self.CURSOR.execute("SELECT data_string FROM article_data WHERE article_title = ?", 
                        (title,))
            results = self.CURSOR.fetchall()
            if results == []:
                return None
            else:
                results = [result[0] for result in results]
                return results
        except sqlite3.Error as e:
            print(e)
            return None
    
    
    def delete_data(self):
        os.remove("./temp.db")    