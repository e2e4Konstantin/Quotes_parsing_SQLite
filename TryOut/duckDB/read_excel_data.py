# https://duckdb.org/docs/guides/import/excel_import.html
# https://github.com/duckdb/sqlite_scanner
# https://www.youtube.com/watch?v=6iyuMJeGhZk
# https://uwekorn.com/2019/10/19/taking-duckdb-for-a-spin.html
# https://nuancesprog.ru/p/17357/
# https://www.cyberforum.ru/blogs/1966431/blog7546.html


import duckdb
from icecream import ic
import pandas as pd

con = duckdb.connect("statistics.duckdb")
con.install_extension("spatial")
con.load_extension("spatial")

# con.execute("INSTALL spatial;")
# con.execute("LOAD spatial;")
#
# result = con.execute("CREATE TABLE new_tbl AS SELECT * FROM st_read('statistics.xlsx', layer='Export Worksheet', open_options=ARRAY[OGR_XLSX_HEADERS=FORCE, OGR_XLSX_FIELD_TYPES = STRING]);")
# ic(result.execute('select count(*) from new_tbl').fetchall())
#
# result = con.execute("""
#     INSERT INTO new_tbl SELECT * FROM st_read('statistics.xlsx', layer='Sheet1', open_options=ARRAY[OGR_XLSX_HEADERS=DISABLE, OGR_XLSX_FIELD_TYPES = STRING]);
#     """)

print(con.execute("SHOW ALL TABLES;").fetchall())
print(con.execute("DESCRIBE new_tbl;").fetchall())
print(con.table('new_tbl').show())





rel = con.sql('SELECT ANY_VALUE(PRESSMARK), sum(VOLUME) AS vol_sum FROM new_tbl')

vol_sum_column = rel["vol_sum"]
print(vol_sum_column)



# ic(result.show())
ic(con.execute('select count(*) from new_tbl').fetchall())

df = con.execute('select * from new_tbl').df()
print(df)

print(con.execute('select * from new_tbl LIMIT 5').fetchall())
# result.close()
con.close()

