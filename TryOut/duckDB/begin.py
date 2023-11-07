import duckdb
from icecream import ic

duckdb.execute('CREATE TABLE tbl AS SELECT 42 a')
con = duckdb.connect(':default:')
con.sql('SELECT * FROM tbl')

r1 = duckdb.sql('SELECT 42 AS i')
ic(r1)
duckdb.sql('SELECT i * 2 AS k FROM r1').show()



con.sql('SELECT 42 AS x').show()