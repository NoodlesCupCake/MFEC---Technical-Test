import sqlite3
import os

def create_table(db_path, table_name='dictionary', output_dir='./database'):
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Connect to the SQLite database (this will create the file if it doesn't exist)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # SQL command to create the table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                dictionary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL
            );
            """)
        
        connection.commit()
        connection.close()
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create table. Error: {e}")


def insert_words_into_db(words, db_path, table_name='dictionary'):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Perform many insertions
        cursor.executemany(f"INSERT INTO {table_name} (word) VALUES (?)", [(word,) for word in words])

        connection.commit()
        connection.close()
        print("Successfully inserted words into the database.")
    except Exception as e:
        print(f"Failed to insert words into the database. Error: {e}")