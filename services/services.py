import sqlite3
import os

def connect_to_database(db_name, database_dir='./database'):
    # Create the output directory if it doesn't exist
    os.makedirs(database_dir, exist_ok=True)

    # Connect to the SQLite database
    db_path = os.path.join(database_dir, db_name)
    connection = sqlite3.connect(db_path)

    return connection


def create_table(connection, table_name='dictionary'):
    try:
        cursor = connection.cursor()

        # Drop the table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        # Create the table
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                dictionary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL
            );
        """)
        
        connection.commit()
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Failed to create table. Error: {e}")


def insert_words_into_db(connection, words, table_name='dictionary'):
    try:
        cursor = connection.cursor()

        # Perform many insertions
        cursor.executemany(f"INSERT INTO {table_name} (word) VALUES (?)", [(word,) for word in words])

        connection.commit()
        print("Successfully inserted words into the database.")

    except Exception as e:
        print(f"Failed to insert words into the database. Error: {e}")


def search_word_by_length(connection, table_name='dictionary', length=5):
    try:
        # Use the connect_to_database function to get a connection
        cursor = connection.cursor()

        # Execute the query to count words 
        cursor.execute(f"SELECT COUNT(*), word FROM {table_name} WHERE LENGTH(word) > ?", (length,))
        count, word = cursor.fetchone() # Fetch the result

        print(f"There are {count} words that have a length greater than {length} (For example: {word}).")
        return count
    except Exception as e:
        print(f"Failed to count words. Error: {e}")
        return None
    

def search_word_with_same_first_and_last_character(connection, table_name='dictionary'):
    try:
        # Use the connect_to_database function to get a connection
        cursor = connection.cursor()

        # Execute the query to count words 
        cursor.execute(f"SELECT COUNT(*), word FROM {table_name} WHERE SUBSTR(word, 1, 1) = SUBSTR(word, -1, 1);")
        count, word = cursor.fetchone()  # Fetch the result

        print(f"There are {count} words that start and end with the same character (For example: {word}).")
        return count
    except Exception as e:
        print(f"Failed to count words. Error: {e}")
        return None