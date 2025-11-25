from app.data.schema import create_users_table, create_datasets_metadata_table, create_it_tickets_table, cybersecurity_table
conn=create_users_table()
conn=create_datasets_metadata_table()
conn=create_it_tickets_table()
conn=cybersecurity_table()
