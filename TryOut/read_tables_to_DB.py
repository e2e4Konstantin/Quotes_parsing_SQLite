import os
import sqlite3
from data_storage import sql_queries


path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
db = r"output\Quotes_v_0.sqlite"
db = os.path.join(path, db)


conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute(sql_queries["create_table_tables"])
cur.execute(sql_queries["create_index_tables"])

conn.commit()
conn.close()

