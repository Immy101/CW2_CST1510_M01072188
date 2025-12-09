from app.data.db import connect_database
from app.data.schema import create_users_table
conn=connect_database()
table=create_users_table(conn)
def get_user_by_username(username):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    )
    user = cursor.fetchone()
    return user

def insert_user(username, password_hash, role='user'):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, password_hash, role)
    )
    conn.commit()