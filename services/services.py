import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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
        cursor = connection.cursor()

        # Execute the query to count words 
        cursor.execute(f"SELECT COUNT(*), word FROM {table_name} WHERE LENGTH(word) > ?", (length,))
        count, word = cursor.fetchone() # Fetch the result

        if count is None:
            print(f"No words with its length greater than {length}.")
        else:
            print(f"There are {count} words that have a length greater than {length} (For example: {word}).")

        return count if count else 0
    
    except Exception as e:
        print(f"Failed to count words. Error: {e}")
        return None
    

def search_word_with_two_or_more_same_characters(connection, table_name='dictionary'):
    try:
        cursor = connection.cursor()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        # For each letter in the alphabet, check if the word has at least 2 of the same character
        query_parts = [f"LENGTH(word) - LENGTH(REPLACE(word, '{letter}', '')) >= 2" for letter in alphabet]

        cursor.execute(f"SELECT COUNT(*), word FROM {table_name} WHERE {' OR '.join(query_parts)}")
        count, word = cursor.fetchone()

        if count is None:
            print("No words with two or more identical characters were found.")
        else:
            print(f"There are {count} words that have two or more same characters in the word (For example: {word}).")

        return count if count else 0
    
    except Exception as e:
        print(f"Failed to count words. Error: {e}")
        return None


def search_word_with_same_first_and_last_character(connection, table_name='dictionary'):
    try:
        cursor = connection.cursor()

        # Execute the query to count words 
        cursor.execute(f"SELECT COUNT(*), word FROM {table_name} WHERE SUBSTR(word, 1, 1) = SUBSTR(word, -1, 1);")
        count, word = cursor.fetchone()  # Fetch the result

        if count is None:
            print("No words that start and end with the same character were found.")
        else:
            print(f"There are {count} words that start and end with the same character (For example: {word}).")

        return count if count else 0
    except Exception as e:
        print(f"Failed to count words. Error: {e}")
        return None
    

def capitalize_the_first_character_of_all_words(connection, table_name='dictionary'):
    try:
        cursor = connection.cursor()
        
        # || = concat strings together
        cursor.execute(f"UPDATE {table_name} SET word = UPPER(SUBSTR(word, 1, 1)) || SUBSTR(word, 2)")
        connection.commit()

        print("Successfully capitalize the first character for every words.")

    except Exception as e:
        print(f"Failed to update words. Error: {e}")
        connection.rollback() 


def export_dictionary_to_pdf(connection, table_name='dictionary', output_pdf='reportDB.pdf'):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT word FROM {table_name} ORDER BY word")
        words = cursor.fetchall()

        c = canvas.Canvas(output_pdf, pagesize=A4)
        _, height = A4 
        y_position = height - 40 

        c.setFont("Courier-Bold", 16)
        c.drawString(150, y_position, "Dictionary Words Report")
        y_position -= 20

        # Set font for the words
        c.setFont("Courier", 12)

        for word in words:
            if y_position < 40: 
                c.showPage()
                c.setFont("Courier", 12)
                y_position = height - 40 

            c.drawString(30, y_position, word[0])
            y_position -= 15

        c.save()

        print(f"Successfully exported dictionary PDF report from the database, it has been saved as {output_pdf}.")
    
    except Exception as e:
        print(f"Error occurred: {e}")