import sqlite3
import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import shutil

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


def create_text_file(words):
    for word in words:
        if len(word) < 2:
            continue

        try:
            # Capitalize the first letter of the word
            capitalized_word = word.capitalize()
            
            # Extract the first and second letters for directory structure
            first_letter = capitalized_word[0].upper()  # First letter (upper case)
            second_letter = capitalized_word[1].upper() if len(capitalized_word) > 1 else ''  # Second letter (upper case)

            # Create the directory structure if it doesn't exist
            directory_path = os.path.join("./vocab", first_letter, second_letter)
            os.makedirs(directory_path, exist_ok=True)  # Create the directory if it doesn't exist

            filename = f"{capitalized_word}.txt"
            file_path = os.path.join(directory_path, filename)

            with open(file_path, "w") as f:
                f.write((word + "\n") * 100)
            
            print(f"File '{file_path}' created and written with the word '{word}' 100 times.")
        
        except Exception as e:
            print(f"Failed to create or write to '{word}': {e}")


def get_folder_size_and_report(base_dir='./vocab', output_pdf='report.pdf'):
    total_size = 0
    first_letter_sizes = {}  # Dictionary to store size of each first-letter folder

    # Create a new PDF canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    _, height = A4 

    c.setFont("Courier", 8)  # Use Courier for a monospaced font, like in a terminal
    
    y_position = height - 40

    c.drawString(30, y_position, "Size          File Name")
    y_position -= 20

    for first_letter in os.listdir(base_dir):
        first_letter_size = 0
        first_letter_path = os.path.join(base_dir, first_letter)

        # Get the size for each of the file in the 2-level folder
        for second_letter in os.listdir(first_letter_path):
            second_letter_path = os.path.join(first_letter_path, second_letter)

            for filename in os.listdir(second_letter_path):
                file_path = os.path.join(second_letter_path, filename)
                
                if os.path.isfile(file_path):  # Check if it's a file
                    file_size = os.path.getsize(file_path)
                    file_size_kb = file_size / 1024 
                    total_size += file_size_kb
                    first_letter_size += file_size_kb  # Add to 1-level folder size

        # Store the size of the 1-level folder in the dictionary
        first_letter_sizes[first_letter] = first_letter_size

        # Format the output: Only size and folder name
        file_info = f"{first_letter_size:10.2f} KB        {first_letter}"
        c.drawString(15, y_position, file_info)
        y_position -= 15 # \n

        # Make sure the content fits within the page
        if y_position < 40:
            c.showPage()
            c.setFont("Courier", 8)  # Reset the font and add a new page
            y_position = height - 40

    # Print the total size at the bottom of the report
    c.drawString(30, y_position, f"Total size of files in {base_dir}: {total_size:.2f} KB")
    
    # Save the PDF
    c.save()

    print(f"PDF report has been saved as {output_pdf}")


def zip_first_level_directories(base_dir='./vocab', output_dir='./zipped'):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop through the first-level directories
    for first_letter in os.listdir(base_dir):
        first_letter_path = os.path.join(base_dir, first_letter)
        
        zip_filename = os.path.join(output_dir, first_letter)
        
        shutil.make_archive(zip_filename, 'zip', first_letter_path)
        
        print(f"Zipped {first_letter_path} into {zip_filename}.zip")


def load_words_from_csv(file_path):
    try:
        # Read the CSV
        df = pd.read_csv(file_path)

        # Filter out empty or NULL words
        words = df['word'].dropna().str.strip()  # Remove NaN values and strip whitespace
        words = words[words != ""]  # Remove any empty strings

        print(f"Successfully loaded {len(words)} words from CSV.")
        return words.tolist()
    except Exception as e:
        print(f"Failed to load words from CSV. Error: {e}")
        return []


def insert_words_into_db(words, db_path, table_name='dictionary'):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Perform batch insertions
        cursor.executemany(f"INSERT INTO {table_name} (word) VALUES (?)", [(word,) for word in words])

        connection.commit()
        connection.close()
        print("Successfully inserted words into the database.")
    except Exception as e:
        print(f"Failed to insert words into the database. Error: {e}")


def main():
    csv_file_path = 'dict.csv'  
    db_path = './database/dictionary.db'  # Using a valid SQLite database file extension
    
    # Load words from the CSV file
    words = load_words_from_csv(csv_file_path)

    # # Convert to text file
    # create_text_file(words)

    # # Create the table
    # create_table(db_path)

    # # Check if words were loaded successfully
    # if words:
    #     # Insert words into the database
    #     insert_words_into_db(words, db_path)
    # else:
    #     print("No words to insert into the database.")

    # Report as PDF file
    get_folder_size_and_report('./vocab', 'report.pdf')

    zip_first_level_directories()

if __name__ == '__main__':
    main()
