from app.data.db import connect_database
from app.data.schema import cybersecurity_table
conn=connect_database()
table=cybersecurity_table(conn)
def debug_table_structure(conn):
    try:
        # Method 1: Get all column names
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(cyber_incidents)")
        columns = cursor.fetchall()
        
        print("🔍 TABLE STRUCTURE: cyber_incidents")
        print("=" * 50)
        
        if not columns:
            print("❌ Table 'cyber_incidents' doesn't exist!")
            return
        
        print("📋 Column names and types:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")  # col[1] is name, col[2] is type
        
        # Method 2: Show sample data
        print(f"\n📊 Sample data (first 3 rows):")
        cursor.execute("SELECT * FROM cyber_incidents LIMIT 3")
        sample_rows = cursor.fetchall()
        
        if sample_rows:
            for i, row in enumerate(sample_rows):
                print(f"  Row {i+1}: {row}")
        else:
            print("  Table is empty")
            
    except Exception as e:
        print(f"❌ Error examining table: {e}")

debug_table_structure(conn)
conn.close() 