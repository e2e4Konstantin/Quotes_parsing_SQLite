import duckdb
from icecream import ic

r1 = duckdb.query("""
SELECT f1 FROM parquet_scan('test.pq') WHERE f2 > 1
""")

result = r1.execute()
r1.create_view('table_name')

# 2---
conn = duckdb.connect()
conn.execute("create table t as SELECT f1 FROM parquet_scan('test.pq') where f2 > 1 ")
r2 = r1.filter("f1>10")
