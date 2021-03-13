import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()
import json
def connect(db_params):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn
    
# def create_database(db_params):
#     '''Creates and connects to Category database. Returns cursor and connection to DB'''
#     # connect to default database
#     # conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=postgres") 
#     conn = connect(**db_params)  
#     conn.set_session(autocommit=True)
#     cur = conn.cursor()
    
#     # create Category database with UTF8 encoding
#     cur.execute("DROP DATABASE IF EXISTS Category")
#     cur.execute("CREATE DATABASE Category WITH ENCODING 'utf8' TEMPLATE template0")

#     # close connection to default database
#     conn.close()    
    
#     # connect to Category database
#     conn = psycopg2.connect("host=127.0.0.1 dbname=Category user=postgres password=postgres")    
#     cur = conn.cursor()
    
#     return cur, conn


# def drop_tables(cur, conn):
#     '''Drops all tables created on the database'''
#     for query in drop_table_queries:
#         cur.execute(query)
#         conn.commit()
# def create_tables(cur, conn):
#     '''Created tables defined on the sql_queries script: [songplays, users, songs, artists, time]'''
#     for query in create_table_queries:
#         cur.execute(query)
#         conn.commit()
if __name__ == "__main__":
    db_params = json.loads(os.environ.get('DATABASE_INFO'))