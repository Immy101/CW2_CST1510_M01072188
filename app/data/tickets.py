import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_it_tickets_table
conn=connect_database()
table=create_it_tickets_table(conn)
cursor = conn.cursor()#this is just to check the contents of the table created
cursor.execute("PRAGMA table_info(IT_tickets_table)")
print(cursor.fetchall()) 

csv_path=Path("DATA/it_tickets.csv")
def load_csv_to_table(conn, csv_path):
    if csv_path.is_file():
        #UNIQUE error concerning duplicates being imported into table
        existing_ids=pd.read_sql("SELECT ticket_id FROM IT_tickets_table", conn)
        existing_set=set(existing_ids['ticket_id'])
        df=pd.read_csv(csv_path) 
        df.columns=df.columns.str.strip()
        print("Data preview: ")
        print(df.head())
        print(f"Columns : {df.columns.tolist()}")
        column_mapping = {
        #csv_column_name:sql_table_column_name
        'ticket_id': 'ticket_id',
        'priority': 'priority',
        'status': 'status',
        'description': 'description',
        'created_at': 'created_date',
        'resolution_time_hours': 'resolved_date',
        'assigned_to': 'assigned_to'
        }
        df=df.rename(columns=column_mapping)
        required_columns = ["ticket_id", "priority", "status", "category", "subject", "description", "created_date", "resolved_date",
                        "assigned_to"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        df= df[required_columns]
        df['subject']= 'Imported ticket' #fix NOT NULL error
        df=df[~df['ticket_id'].isin(existing_set)]
        df.to_sql('IT_tickets_table', con=conn, if_exists='append', index=False)
        cursor=conn.cursor()
        cursor.execute( 
            f"SELECT COUNT(*) FROM IT_tickets_table" 
        )
        row_count=cursor.fetchall()[0]
        return "Success fully loading of data", row_count
    else:
        print(f"{csv_path} does not exist.")
#load_csv_to_table(conn, csv_path)

#functions to read, update and delete data from the metadata table
def insert_ticket(conn, ticket_id, priority, status, category, subject, description, created_date, assigned_to):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO IT_tickets_table(ticket_id, priority, status, category, subject, description, created_date, assigned_to) VALUES(?,?,?,?,?,?,?,?)", (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
    )
    conn.commit()
    ticket=cursor.lastrowid
    return ticket

def get_all_tickets(conn):
    df=pd.read_sql_query("SELECT * FROM IT_tickets_table", conn)
    return df
print(get_all_tickets(conn))

def update_ticket_status(conn, resolved_date,status, ticket_id):
    cursor=conn.cursor()
    cursor.execute(
        "UPDATE IT_tickets_table SET resolved_date =?, status =? WHERE ticket_id=?",(resolved_date, status, ticket_id)
    )
    conn.commit()
    rows=cursor.rowcount
    if rows > 0:
        return rows
    else:
        print(f"{id} not found")
        return False
    
def delete_ticket(conn, ticket_id):
    cursor=conn.cursor()
    cursor.execute(
        "DELETE FROM IT_tickets_table WHERE ticket_id=?", (ticket_id,)
    )
    conn.commit()
    rows_deleted=cursor.rowcount
    return rows_deleted