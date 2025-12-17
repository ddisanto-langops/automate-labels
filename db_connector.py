import os
import sqlite3
from fuzzy_match import get_similarity

class DBConnection:
    """
    Class DBConnection represents a connection to a local sqlite database.
    """
    def __init__(self):
        try:
            self.APP_FOLDER = os.path.dirname(os.path.abspath(__file__)) # Gets the directory of the current script
            self.CONNECTION = sqlite3.connect(":memory:")
            self.CONNECTION.row_factory = sqlite3.Row
            self.CURSOR = self.CONNECTION.cursor()
            print(f"✅ Connected to SQLite database file: {self.CONNECTION}")

        except sqlite3.Error as error:
            print(f"SQLite error occurred: {error}")
            return error
        
    
    def insert_data(self, title: str, data: list, label_id: int):
        """Inserts article data using executemany for high performance."""
        self.CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS article_data (
                id INTEGER PRIMARY KEY,
                article_title TEXT NOT NULL,
                data_string TEXT NOT NULL,
                label_id INTEGER NOT NULL
            );
        """)

        data_to_insert = [
            (title, data_string, label_id)
            for data_string in data
        ]
        
        sql_insert = "INSERT INTO article_data (article_title, data_string, label_id) VALUES (?, ?, ?)"
        rows_inserted = len(data_to_insert)

        try:
            self.CURSOR.executemany(sql_insert, data_to_insert)
            self.CONNECTION.commit()
            print(f"Successfully inserted {rows_inserted} rows into SQLite.")
        except Exception as e:
            # 5. Rollback on error
            self.CONNECTION.rollback()
            print(f"An error occurred during insertion. Transaction rolled back: {e}")
    
    
    def retreive_most_similar(self, min_score: int, string_to_compare: str) -> dict:
        """
        Compares a given string against the entire database and returns its closest match,
        along with similarity score.        
        """
        self.CURSOR.execute("SELECT data_string, article_title, label_id FROM article_data")
        db_strings = self.CURSOR.fetchall()
        most_similar_string = None
        highest_similarity = 0
        id_of_most_similar = None
        for row in db_strings:
            article_string = row['data_string']
            label_id = row['label_id']
            current_similarity = get_similarity(string_to_compare, article_string)
            if current_similarity >= min_score and current_similarity > highest_similarity:
                highest_similarity = current_similarity
                most_similar_string = article_string
                id_of_most_similar = label_id
        return {"most_similar_string": most_similar_string, "similarity": highest_similarity, "label_id": id_of_most_similar}


    def retreive_all(self):
        self.CURSOR.execute("SELECT data_string, article_title, label_id FROM article_data")
        data = self.CURSOR.fetchall()
        output = []
        for row in data:
            output.append(row['article_title'])
            output.append(row['label_id'])
        return output

    def close_connection(self):
        if self.CONNECTION:
            self.CONNECTION.close()
        print("Connection closed")


my_db = DBConnection()
my_db.insert_data("title",["string1", "string2", "string3"],4151)
sims = my_db.retreive_most_similar(70,"strin2")
print(sims)
