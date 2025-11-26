import pandas as pd
from pathlib import Path
from db import connect_database
from app.data.schema import create_datasets_metadata_table
conn=connect_database()
table=create_datasets_metadata_table(conn)
cursor = conn.cursor()#this is just to check the contents of the table created
cursor.execute("PRAGMA table_info(metadata_table)")
print(cursor.fetchall()) 
csv_path=Path("DATA/datasets_metadata.csv")
def load_csv_to_table(conn, csv_path):
    if csv_path.is_file():
        df=pd.read_csv(csv_path)
        df.columns=df.columns.str.strip()
        print("Data preview: ")
        print(df.head())
        print(f"Columns : {df.columns.tolist()}")
        column_mapping = {
        #csv_column_name:sql_table_column_name
        'name': 'dataset_name',
        'rows': 'record_count',
        'uploaded_by': 'source',
        'upload_date': 'last_updated'
        }
        df=df.rename(columns=column_mapping)
        df=df.drop(columns=["dataset_id"], errors='ignore')
        required_columns = ["dataset_name", "category", "record_count", "source",
                        "last_updated", "file_size_mb"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        df= df[required_columns]
        df.to_sql('metadata_table', con=conn, if_exists='append', index=False)
        cursor=conn.cursor()
        cursor.execute( 
            f"SELECT COUNT(*) FROM metadata_table" 
        )
        row_count=cursor.fetchall()[0]
        return "Success fully loading of data", row_count
    else:
        print(f"{csv_path} does not exist.")
print(load_csv_to_table(conn, csv_path))

#functions to read, update and delete data from the metadata table
def insert_metadata(conn, dataset_name, category, record_count, source, last_updated, file_size_mb):
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO metadata_table(dataset_name, category, record_count, source, last_updated, file_size_mb) VALUES(?,?,?,?,?,?)", (dataset_name, category, record_count, source, last_updated, file_size_mb)
    )
    conn.commit()
    dataset=cursor.lastrowid
    conn.close()
    return dataset

def get_all_metadata(conn):
    df=pd.read_sql_query("SELECT * FROM metadata_table", conn)
    return df
print(get_all_metadata(conn))

def update_metadata_status(conn, category, dataset_name):
    cursor=conn.cursor()
    cursor.execute(
        "UPDATE metadata_table SET category =? WHERE dataset_name=?",(category, dataset_name)
    )
    conn.commit()
    rows=cursor.rowcount
    if rows > 0:
        conn.close()
        return rows
    else:
        print(f"{dataset_name} not found")
        return False
def delete_metadata(conn, dataset_name):
    cursor=conn.cursor()
    cursor.execute(
        "DELETE FROM metadata_table WHERE dataset_name=?", (dataset_name,)
    )
    conn.commit()
    rows_deleted=cursor.rowcount
    return rows_deleted