import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import cybersecurity_table
conn=connect_database()
table=cybersecurity_table(conn)
csv_path=Path("DATA/cyber_incidents.csv")
def load_csv_to_table(conn, csv_path):
    cursor=conn.cursor()
    if csv_path.is_file():
        df=pd.read_csv(csv_path)
        df.columns=df.columns.str.strip()
        print("Data preview: ")
        print(df.head())
        print(f"Columns : {df.columns.tolist()}")
        column_mapping = {
        #csv_column_name:sql_table_column_name
        'timestamp': 'date',
        'category': 'incident_type',
        'severity': 'severity',
        'status': 'status',
        'description': 'description'
        }
        df=df.rename(columns=column_mapping)
        df=df.drop(columns=["incident_id"], errors='ignore')
        required_columns = ["date", "incident_type", "severity",
                        "status", "description", "reported_by"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        df= df[required_columns]
        df.to_sql('incidents', con=conn, if_exists='append', index=False)
        cursor=conn.cursor()
        cursor.execute( 
            f"SELECT COUNT(*) FROM incidents" 
        )
        row_count=cursor.fetchall()[0]
        return "Success fully loading of data", row_count
    else:
        print(f"{csv_path} does not exist.")
#print(load_csv_to_table(conn, csv_path))

#functions to read, update and delete data from the cyber incidents table
def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO incidents(date, incident_type, severity, status, description, reported_by) VALUES(?,?,?,?,?,?)", (date, incident_type, severity, status, description, reported_by)
    )
    conn.commit()
    incident=cursor.lastrowid
    return incident

def get_all_incidents(conn):
    df=pd.read_sql_query("SELECT * FROM incidents", conn)
    return df
print(get_all_incidents(conn))
def update_incident_status(conn, status, reported_by, incident_type):
    cursor=conn.cursor()
    cursor.execute(
        "UPDATE incidents SET status =?, reported_by=? WHERE incident_type=?",(status, reported_by, incident_type)
    )
    conn.commit()
    rows=cursor.rowcount
    if rows > 0:
        conn.close()
        return rows
    else:
        print(f"{id} not found")
        return False
    
def delete_incident(conn,incident_type, reported_by):
    cursor=conn.cursor()
    cursor.execute(
        "DELETE FROM incidents WHERE incident_type=?, reported_by=?", (incident_type, reported_by)
    )
    conn.commit()
    rows_deleted=cursor.rowcount
    return rows_deleted

#get statistical analysis from the data in cyber_incidents table
def get_incidents_by_type_count(conn):
    query = """
    SELECT incident_type, 
    COUNT(*) as count
    FROM incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    query = """
    SELECT status, 
    COUNT(*) as count
    FROM incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_incident_types_with_many_cases(conn, min_count=5):
    query = """
    SELECT incident_type, 
    COUNT(*) as count
    FROM incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df

