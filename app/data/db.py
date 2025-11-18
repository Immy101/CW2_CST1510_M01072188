from pathlib import Path
import sqlite3
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR/"intelligence_platform.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)
print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")
def connect_database(db_path=DB_PATH):
    #this will connect to the SQL database.
    return sqlite3.connect(str(db_path))
