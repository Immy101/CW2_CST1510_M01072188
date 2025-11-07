import bcrypt
import os
def hash_password(password):
    password_bytes=password.encode('utf-8')
    salt=bcrypt.gensalt(rounds=12)
    hash=bcrypt.hashpw(password_bytes, salt)
    return hash
def verify(username, password):
    password_bytes=password.encode('utf-8')
    hash_password1=hash_password(password)
    result1=bcrypt.checkpw(password_bytes, hash_password1)
    if result1:
        print(f"{username} is verified.")
    else:
        return False
    return True
def login(username, password):
    with open("users.txt", 'r') as f:
        for line in f.readlines():
            try:
                user, hashp, roles=line.strip().split(',',2)
                if user == username:
                    return verify(username, password)
                return False
            except ValueError:
                continue
def register(username, password, role):
    hash_password1=hash_password(password)
    with open("users.txt", 'a') as f:
        #use "a" for append because the "w" for write would write over everything and erase the already entered information
        f.write(f"{username}, {hash_password1}, {role}\n")
    print(f"{username}, {role} has registered.")
    return True
username=input("Enter your username: ")
password=input("Enter your password: ")
role=input("Enter your role(position): ")
register(username, password, role)
login(username, password)