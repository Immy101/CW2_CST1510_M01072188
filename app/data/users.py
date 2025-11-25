from app.data.db import connect_database
conn=connect_database()
def get_user_by_username(username):
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username= ?",
        (username,)
    )
    user=cursor.fetchone()
    conn.commit()
    conn.close()
    return user
