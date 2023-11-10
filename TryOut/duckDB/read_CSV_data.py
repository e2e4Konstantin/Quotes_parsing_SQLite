import duckdb
from icecream import ic

csv_file_name = r"Статистика_20_utf8.csv"
# csv_file_name = r"statistics.csv"

q = f"CREATE TABLE tblStatistics AS SELECT * FROM read_csv_auto('{csv_file_name}');"


# q = f"SELECT * FROM read_csv_auto('statistics_utf8.csv');" # , delim=';', quote='', header=true, sample_size=-1 AUTO_DETECT=TRUE , quote='\"' , delim=';', header=True,  IGNORE_ERRORS=1
#
# conn.execute("""SELECT date, SUM(failure) as failures
#                 FROM read_csv('data/*/*.csv', delim=',', header=True,  IGNORE_ERRORS=1,
#                     columns={
#                             'date': 'DATE',
#                             'serial_number' : 'VARCHAR',
#                             'model' : 'VARCHAR',
#                             'capacity_bytes' : 'VARCHAR',
#                             'failure' : 'INT'
#                             })
#              GROUP BY date;""")


ic(q)

with duckdb.connect("statistics.duckdb") as con:
    con.execute(q)
    print(con.execute("SHOW ALL TABLES;").fetchall())
    print(con.execute("DESCRIBE tblStatistics;").fetchall())
    print(con.table('tblStatistics').show())
    print(con.execute("SELECT count(*) FROM tblStatistics").fetchall())

