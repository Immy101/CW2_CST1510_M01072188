import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table
conn=connect_database()
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
    with open("DATA/users.txt", 'r') as f:
        for line in f.readlines():
            try:
                user, hashp, roles=line.strip().split(',',2)
                if user == username:
                    return verify(username, password)
                return False
            except ValueError:
                continue

def register(username, password, role):
    conn= connect_database()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?" ,(username,))
    if cursor.fetchone():
        return False, f"Username '{username}' already exists."
    
    valid=False #initialise the validity of password to false
    while valid:
        password_strength=pw_strength(password)
        valid=True #the checker will confirm if its valid and then we break the loop
    
    hash_password1=hash_password(password)
    #write the new data into the database
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES(?,?,?)", (username, hash_password1, role)
    )
    conn.commit()
    conn.close()
    
    with open("DATA/users.txt", 'a') as f:
        #use "a" for append because the "w" for write would write over everything and erase the already entered information
        f.write(f"{username}, {hash_password1}, {role}\n")
    print(f"{username}, {role} has registered successfully.")
    return True

def pw_strength(password):
    if len(password) <=0:
        print("password too short. invalid.")
    else:
        specialchar=["<>,./?:;|\}{[]_-=+!@#$%^&*()"]
        for x in password:
            if x==password.isdigit():
                pass
            elif x==password.isalpha():
                pass
            elif x==password.isspace():
                pass
            elif x in specialchar:
                pass
            else:
                return False
        return True
def migrate_users(conn, filepath="DATA/users.txt"):
    if not filepath.exists():
        print(f"Filepath not found: {filepath}")
        print("No users to migrate.")
        return
    cursor=conn.cursor()
    migrated_count=0
    with open(filepath, 'r') as f:
        for line in f:#why can't i use  the f.read() method
            line=line.strip()
            if not line:
                continue
            parts=line.split(',')
            if len(parts)>=2:
                username=parts[0]
                password_hash=parts[1]
                try:
                    cursor.execute("INSERT OR IGNORE INTO users(username, password_hash, role) VALUES(?,?,?)",(username, password_hash, role))
                    if cursor.rowcount>0:
                        migrated_count+=1
                except sqlite3.Error as e:
                    print(f"Error migrating {username}: {e}")
    conn.commit()
    print(f"Migrated {migrated_count} users from {filepath.name}")
    conn=connect_database()
    cursor=conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users=cursor.fetchall()
    print("users in database: ")
    print(f"{'ID':<5}, {'USERNAME':<15}, {'ROLE':<10}")
    print("-"*35)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")
    print(f"\nTotal users: {len(users)}")
    conn.close()

#Welcome/ display page  
on=True
while on:
    print("*"*60)
    print("Multi-domain Intelligence platform")
    print("*"*60)
    print("Welcome! Please choose from the list of options below.")
    print("*"*60)
    print("1.LOGIN")
    print("2.REGISTER")
    print("*"*60)
    option=input("Enter your choice: ")
    if option == '1':
        username=input("Enter your username: ")
        password=input("Enter your password: ")
        role=input("Enter your role(position): ")
        login(username, password)
        on= False
    elif option == '2':
        username=input("Enter your username: ")
        password=input("Enter your password: ")
        role=input("Enter your role(position): ")
        register(username, password, role)
        on= False
    else:
        print("invalid entry")