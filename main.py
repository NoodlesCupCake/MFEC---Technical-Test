from services.services import create_table, insert_words_into_db
from utils.utils import load_words_from_csv, create_text_file, get_folder_size_and_report, zip_first_level_directories

def main():
    csv_file_path = 'dict.csv'  
    db_path = './database/dictionary.db'
    
    # 1. หาไฟล์ dictionary อังกฤษ > 20,000 คำ ทำเป็น text file 
    words = load_words_from_csv(csv_file_path)

    # 2. เอามาสร้างไฟล์ text โดยให้ชื่อไฟล์เป็นชื่อคำศัพท์ เช่น joke --> joke.txt โดยในเนื้อหาไฟล์เป็นคำ ๆ นั้น (เปิดไฟล์ joke.txt เจอคำว่า joke ในไฟล์ โดยให้มีซ้ำ ๆ ไป 100 ครั้ง) 
    # 3. ใช้เป็นตัวอักษรตัวเล็กทั้งหมด 
    # 4. ไฟล์เหล่านี้ ให้เก็บไว้ใน directory ตำมตัวอักษร 2 level
    create_text_file(words)

    # 5. ทำ report ของ folder size ว่ำมีขนาดเท่ำไหร่เป็น Kbyte และมีลิสต์ของแต่ละไฟล์ด้วย นึกถึงคำสั่ง ls -l ใน unix และทำเฉพำะ level 1
    get_folder_size_and_report()

    # 6. zip ไฟล์ทีละไดเรคทอรี เป็น a.zip, b.zip,... แล้วทำ report เปรียบเทียบว่า ขนาดก่อน zip กับหลัง zip ต่างกันเป็นกี่ % 
    zip_first_level_directories()

    # 7. เอา dictionary ลงใน Database แบบไหนก็ได้เช่น SqlLite โดยรันแบบ embeded mode  โดยการออกแบบให้สามารถ query เพื่อตอบคำถามเหล่านี้ได้ 
    create_table(db_path)
    insert_words_into_db(words, db_path)

    # 8. Export คำใน database ทั้งหมดออกมำเป็น pdf file เรียงบรรทัดละค ำ (ขนำดใช้เป็น A4) 

if __name__ == '__main__':
    main()
