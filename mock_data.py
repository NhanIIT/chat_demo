from faker import Faker
import sqlite3
import random


def mock_data():
    conn = sqlite3.connect('hr.db')
    c = conn.cursor()
    fake = Faker('vi_VN')
    # Thêm phòng ban
    departments = ['Kỹ thuật', 'Kế toán', 'Nhân sự', 'Kinh doanh']
    for d in departments:
        c.execute("INSERT INTO departments (name) VALUES (?)", (d,))
    # Thêm vai trò
    roles = ['Admin', 'Manager', 'employee']
    for r in roles:
        c.execute("INSERT INTO roles (name) VALUES (?)", (r,))
    # Thêm user
    for _ in range(20):
        name = fake.name()
        email = fake.email()
        department_id = random.randint(1, len(departments))
        role_id = random.randint(1, len(roles))
        c.execute(
            "INSERT INTO users (name, department_id, email, role_id) "
            "VALUES (?, ?, ?, ?)",
            (name, department_id, email, role_id)
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    mock_data()