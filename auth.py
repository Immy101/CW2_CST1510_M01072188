import bcrypt
import os
def hash_password(password):
    password_bytes=password.encode('utf-8')
    salt=bcrypt.gensalt(rounds=12)
    hash=bcrypt.hashpw(password_bytes, salt)
    return hash
def register(username, password):
    hash_password1=hash_password(password)
    with open("users.txt", 'w') as f:
        f.write(f"{username}, {hash_password1}")
username=input("Enter your username: ")
password=input("Enter your password: ")
register(username, password)