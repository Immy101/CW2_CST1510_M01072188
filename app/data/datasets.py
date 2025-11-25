import pandas as pd
from pathlib import Path
from db import connect_database
conn=connect_database()
csv_path=Path("DATA/datasets_metadata.csv")
def load_csv_to_table(conn, csv_path, table_name='Datasets_metadata'):
    if csv_path.is_file():
        df=pd.read_csv(csv_path)
        print("Data preview: ")
        print(df.head())
        print(f"Columns : {df.columns.tolist()}")
        df.to_sql(con=conn, name=table_name, if_exists='append', index=False)
        cursor=conn.cursor()
        cursor.execute( 
            f"SELECT COUNT(*) FROM {table_name}" 
        )
        row_count=cursor.fetchall()[0]
        return "Success fully loading of data", row_count
    else:
        print(f"{csv_path} does not exist.")
print(load_csv_to_table(conn, csv_path, table_name='Datasets_metadata'))