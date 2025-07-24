import sqlite3
from typing import List, Dict


DB_PATH = "hr.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            salary INTEGER
        )
        '''
    )
    # Thêm dữ liệu mẫu nếu bảng rỗng
    cursor.execute('SELECT COUNT(*) FROM employees')
    if cursor.fetchone()[0] == 0:
        data = [
            ("Nguyen Van A", "Kế toán", "Nhân viên", 12000000),
            ("Tran Thi B", "Kế toán", "Trưởng phòng", 20000000),
            ("Le Van C", "Nhân sự", "Nhân viên", 11000000),
            ("Pham Thi D", "IT", "Lập trình viên", 15000000),
            ("Hoang Van E", "IT", "Trưởng phòng", 22000000)
        ]
        sql_insert = (
            'INSERT INTO employees (name, department, position, salary) '
            'VALUES (?, ?, ?, ?)'
        )
        cursor.executemany(sql_insert, data)
    conn.commit()
    conn.close()


def query_db(sql: str) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [
        dict(zip(columns, row))
        for row in rows
    ] 