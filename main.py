from services.services import capitalize_the_first_character_of_all_words, connect_to_database, create_table, export_dictionary_to_pdf, insert_words_into_db, search_word_by_length, search_word_with_same_first_and_last_character, search_word_with_two_or_more_same_characters
from utils.utils import load_words_from_csv, create_text_file_with_ThreadPoolExecutor, get_folder_size_and_report, zip_first_level_directories_with_ThreadPoolExecutor
import time

def main():
    csv_file_path = 'dict.csv'  
    database = 'dictionary.db'
    
    start_time = time.time() 

    # 1. หาไฟล์ dictionary อังกฤษ > 20,000 คำ ทำเป็น text file 
    words = load_words_from_csv(csv_file_path)

    # 2. เอามาสร้างไฟล์ text โดยให้ชื่อไฟล์เป็นชื่อคำศัพท์ เช่น joke --> joke.txt โดยในเนื้อหาไฟล์เป็นคำ ๆ นั้น (เปิดไฟล์ joke.txt เจอคำว่า joke ในไฟล์ โดยให้มีซ้ำ ๆ ไป 100 ครั้ง) 
    # 3. ใช้เป็นตัวอักษรตัวเล็กทั้งหมด 
    # 4. ไฟล์เหล่านี้ ให้เก็บไว้ใน directory ตำมตัวอักษร 2 level
    create_text_file_with_ThreadPoolExecutor(words)

    # 6. zip ไฟล์ทีละไดเรคทอรี เป็น a.zip, b.zip,... แล้วทำ report เปรียบเทียบว่า ขนาดก่อน zip กับหลัง zip ต่างกันเป็นกี่ % 
    zip_first_level_directories_with_ThreadPoolExecutor()

    # 5. ทำ report ของ folder size ว่ามีขนาดเท่าไหร่เป็น Kbyte และมีลิสต์ของแต่ละไฟล์ด้วย นึกถึงคำสั่ง ls -l ใน unix และทำเฉพำะ level 1
    get_folder_size_and_report()

    # 7. เอา dictionary ลงใน Database แบบไหนก็ได้เช่น SqlLite โดยรันแบบ embeded mode  โดยการออกแบบให้สามารถ query เพื่อตอบคำถามเหล่านี้ได้ 
    connection = connect_to_database(database)
    create_table(connection)
    insert_words_into_db(connection, words)

    # 7.1 มีคำกี่คำที่มีความยาว > 5 ตัวอักษร
    q7_1 = search_word_by_length(connection)

    # 7.2 มีคำกี่คำที่มีตัวอักษรซ้ำในคำมากกว่าหรือเท่ากับ 2 characters
    q7_2 = search_word_with_two_or_more_same_characters(connection)

    # 7.3 มีคำกี่คำที่ขึ้นต้นและลงท้ำยด้วยตัวอักษรเดียวกัน
    q7_3 = search_word_with_same_first_and_last_character(connection)

    # 7.4 ให้สั่งอัพเดตคำที่มีทั้งหมดให้ตัวอักษรตัวแรกเป็นตัวพิมพ์ใหญ่
    q7_4 = capitalize_the_first_character_of_all_words(connection)

    # 8. Export คำใน database ทั้งหมดออกมาเป็น pdf file เรียงบรรทัดละคำ (ขนาดใช้เป็น A4) 
    export_dictionary_to_pdf(connection=connection, q7_1=q7_1, q7_2=q7_2, q7_3=q7_3, q7_4=q7_4)

    connection.close()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken for the process: {elapsed_time:.2f} seconds")


if __name__ == '__main__':
    main()
