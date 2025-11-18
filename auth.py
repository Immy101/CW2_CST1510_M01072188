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
    with open("C:/Users/Admin/OneDrive/Desktop/CW2_CST1510_M01072188/CW2_CST1510_M01072188/DATA/users.txt", 'r') as f:
        for line in f.readlines():
            try:
                user, hashp, roles=line.strip().split(',',2)
                if user == username:
                    return verify(username, password)
                return False
            except ValueError:
                continue
def register(username, password, role):
    password_strength=pw_strength(password)
    hash_password1=hash_password(password)
    with open("C:/Users/Admin/OneDrive/Desktop/CW2_CST1510_M01072188/CW2_CST1510_M01072188/DATA/users.txt", 'a') as f:
        #use "a" for append because the "w" for write would write over everything and erase the already entered information
        f.write(f"{username}, {hash_password1}, {role}\n")
    print(f"{username}, {role} has registered.")
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