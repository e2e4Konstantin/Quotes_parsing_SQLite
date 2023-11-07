# https://duckdb.org/docs/guides/import/excel_import.html
# https://motherduck.com/blog/duckdb-tutorial-for-beginners/

import duckdb
from icecream import ic

con = duckdb.connect('my_database.duckdb')

# Configure settings
con.execute("PRAGMA threads=4") # Use 4 threads
con.execute("PRAGMA memory_limit='4GB'") # Limit memory usage to 4GB


# results = duckdb.sql('SELECT 42').fetchall()
# ic(results)
#
# duckdb.sql('SELECT * FROM "example.csv"')

#
# conn = duckdb.connect("my_db.db")
# # conn = duckdb.connect("my_db.db", read_only=True)
# conn.sql("""
#   SELECT *
#   FROM 'dataset/*.csv'
#   LIMIT 10
# """)
#
# df = conn.sql("""
#   SELECT *
#   FROM 'dataset/*.csv'
#   LIMIT 10
# """).df()
#
# print(df)


# duckdb.sql('INSTALL spatial;')
# duckdb.sql('LOAD spatial;')
# duckdb.sql("""CREATE TABLE new_tbl AS SELECT * FROM st_read('C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite\src\catalog_10_68.xlsx', layer='quotes');""")

# CREATE TABLE new_tbl AS
# SELECT * FROM st_read('test_excel.xlsx', layer='Sheet1');
#
#
#
# INSERT INTO tbl
# SELECT * FROM st_read('test_excel.xlsx', layer='Sheet1');