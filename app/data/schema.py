from app.data.db import connect_database
conn=connect_database()
def create_users_table(conn):
    cursor=conn.cursor()
    create_table_sql="""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT ,
    created at TIMESTAMP CURRENT_TIMESTAMP)
    """
    cursor.execute(create_table_sql)
    conn.commit()
    return True
def cybersecurity_table(conn):
    cursor=conn.cursor()
    #date TEXT(format: YYYY-MM-DD),
    #incident_type TEXT (e.g. 'Phishing', 'Malware', 'DDoS'),
    #severity TEXT (e.g. 'Critical', 'High', 'Medium', 'Low'),
    #status TEXT (e.g 'Open', 'Investigating', 'Resolved', 'Closed'),
    #description TEXT,
    #reported_by TEXT (username of reporter),
    create_table="""
    CREATE TABLE IF NOT EXISTS incidents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    incident_type TEXT ,
    severity TEXT ,
    status TEXT ,
    description TEXT,
    reported_by TEXT ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table)
    conn.commit()
    return True
def create_datasets_metadata_table(conn):
    cursor=conn.cursor()
    #category TEXT #(e.g., 'Threat Intelligence', 'Network Logs')
    #source TEXT (origin of the dataset)
    #last_updated TEXT (format: YYYY-MM-DD)
    create_datasets_metadata="""
    CREATE TABLE IF NOT EXISTS datasets_metadata(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT NOT NULL,
    category TEXT ,
    source TEXT ,
    last_updated TEXT ,
    record_count INTEGER,
    file_size_mb REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_datasets_metadata)
    conn.commit()
    return True
def create_it_tickets_table(conn):
    cursor=conn.cursor()
     #priority TEXT (e.g., 'Critical', 'High', 'Medium', 'Low')
    #status TEXT (e.g., 'Open', 'In Progress', 'Resolved', 'Closed')
    #category TEXT (e.g., 'Hardware', 'Software', 'Network')
    create_it_tickets="""
    CREATE TABLE IF NOT EXISTS it_tickets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT UNIQUE NOT NULL,
    priority TEXT,
    status TEXT,
    category TEXT,
    subject TEXT NOT NULL,
    description TEXT,
    created_date TEXT,
    resolved_date TEXT,
    assigned_to TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_it_tickets)
    conn.commit()
    return True
def create_all_tables(conn):
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    cybersecurity_table(conn)
    create_users_table(conn)
    return True
create_all_tables(conn)