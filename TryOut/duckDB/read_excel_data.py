# https://duckdb.org/docs/guides/import/excel_import.html

import duckdb
from icecream import ic

con = duckdb.connect()
con.install_extension("spatial")
con.load_extension("spatial")

# con.execute("INSTALL spatial;")
# con.execute("LOAD spatial;")

result = con.execute("CREATE TABLE new_tbl AS SELECT * FROM st_read('statistics.xlsx', layer='Export Worksheet');")
ic(result)
# ic(result.show())
ic(result.execute('select count(*) from new_tbl').fetchall())



# print(result.execute('select * from new_tbl').fetchall())  #count(*)
# result.close()
# con.close()

# with duckdb.connect('file.db') as con:
#     con.sql('CREATE TABLE test(i INTEGER)')
#     con.sql('INSERT INTO test VALUES (42)')
#     con.table('test').show()




# INSERT INTO tbl
# SELECT * FROM st_read('test_excel.xlsx', layer='Sheet1');