import sqlite3
import os

db_path = r"D:\Academic\Sem Projects\sem 5 - 6 - 7 project\AI-Super-App\instance\database.db"
query = "UPDATE user SET credits = 50 WHERE email = 'alokagarwal629@gmail.com';"

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print(f"Successfully updated. Rows affected: {cursor.rowcount}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")