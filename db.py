import sqlite3


def init_db():
    conn = sqlite3.connect('hr.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department_id INTEGER,
            email TEXT,
            role_id INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()