from pathlib import Path
import sqlite3
Path("app/__init__.py").touch()
Path("app/data/__init__.py").touch()
Path("app/services/__init__.py").touch()
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR/"intelligence_platform.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)
print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")
def connect_database(db_path=DB_PATH):#this defines the function to create the databse but doesn't actually create it
    #this will connect to the SQL database.
    return sqlite3.connect(str(db_path))