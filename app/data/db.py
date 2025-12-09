from pathlib import Path
import sqlite3
#Path("app/__init__.py").touch()
#Path("app/data/__init__.py").touch()
#Path("app/services/__init__.py").touch()
#DATA_DIR = Path("DATA")
#DB_PATH = DATA_DIR/"intelligence_platform.db"
#print(" Imports successful!")
#print(f" DATA folder: {DATA_DIR.resolve()}")
#print(f" Database will be created at: {DB_PATH.resolve()}")
def connect_database():
    #this defines the function to create the databse but doesn't actually create it
    #this will connect to the SQL database.
    base_dir = Path(__file__).resolve().parent.parent.parent
    db_path = base_dir / "DATA" / "intelligence_platform.db"
    print("DEBUG — db_path:", db_path)
    print("DEBUG — exists:", db_path.exists())
    print("DEBUG — file location:", __file__)
    print("DEBUG — base_dir:", base_dir)

    return sqlite3.connect(str(db_path), check_same_thread=False)