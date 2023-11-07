import duckdb
from icecream import ic


cursor = db.execute("""
select *
from read_parquet('/tmp/places/type=place/*')
where
    bbox.minx > -122.5292336382 
    AND bbox.maxx < -122.403920833 
    AND bbox.miny > 37.4239030609 
    AND bbox.maxy < 37.5611068793
""")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
dicts = [dict(zip(columns, row)) for row in rows]

Now I can insert those into a table in a SQLite database:

# %pip install sqlite-utils first if it's not installed
import sqlite_utils

hmb = sqlite_utils.Database("/tmp/hmb.db")
hmb["places"].insert_all(dicts, pk="id", replace=True)


str = join(repeat('?', length(table_data)), ',')
write_query = DBInterface.prepare(con_sqlite, "INSERT INTO data VALUES($str)")
@time DBInterface.executemany(write_query, table_data)


# ----------------------------/
using SQLite, DuckDB, Tables

con_sqlite = DBInterface.connect(SQLite.DB, "test.sqlite3")
con_duckdb = DBInterface.connect(DuckDB.DB, "test1.duckdb")

len = 10_000
table_data = (a = collect(1:len), b = rand(1:100, len))

# create a table
create_query = map((k,v)->"$k INT NOT NULL,", keys(table_data), table_data) |> # $(SQLite.sqlitetype(eltype(v)))
    x->join(x, "\r\n")[1:end-1] |>
    x->"CREATE TABLE data(\r\n$x\r\n);" #
DBInterface.execute(con_sqlite, create_query)
DBInterface.execute(con_duckdb, create_query)

# write file
str = join(repeat('?', length(table_data)), ',')
write_query = DBInterface.prepare(con_sqlite, "INSERT INTO data VALUES($str)")
@time DBInterface.executemany(write_query, table_data)
# first run: 0.211553 seconds (440.17 k allocations: 24.565 MiB, 95.13% compilation time)
# second run: 0.010278 seconds (89.52 k allocations: 6.404 MiB

write_query = DBInterface.prepare(con_duckdb, "INSERT INTO data VALUES($str)")
@time DBInterface.executemany(write_query, table_data)
# first run: 3.263211 seconds (1.10 M allocations: 80.216 MiB, 0.40% gc time, 6.34% compilation time)
# second run: 8.388220 seconds (797.40 k allocations: 64.408 MiB, 0.23% gc time)

# read file
@time table_rd = DBInterface.execute(con_sqlite, "SELECT * FROM data") |> columntable
# first run: 0.874020 seconds (3.02 M allocations: 156.725 MiB, 8.00% gc time, 96.61% compilation time)
# second run: 0.011222 seconds (78.53 k allocations: 3.363 MiB)

@time table_rd = DBInterface.execute(con_duckdb, "SELECT * FROM data") |> columntable
# first run: 0.553115 seconds (1.93 M allocations: 98.399 MiB, 4.10% gc time, 99.20% compilation time)
# second run: 0.005292 seconds (58.69 k allocations: 1.397 MiB)

DBInterface.close!(con_sqlite)
DBInterface.close!(con_duckdb)