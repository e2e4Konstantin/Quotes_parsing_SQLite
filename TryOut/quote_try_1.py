import sqlite3
import os

# path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"

# читаем данные из исходных файлов во временную БД
raw_db_name = r"output\RawCatalog.sqlite"
raw_db = os.path.join(path, raw_db_name)
operating_db_name = r"output\Quotes.sqlite"
operating_db = os.path.join(path, operating_db_name)
period = 68


# con_raw = sqlite3.connect(raw_db)
# con_raw.row_factory = sqlite3.Row
# cursor_raw = con_raw.cursor()
# sql = 'select * from Main where watched is 0 order by Genre, Folder_runtime'
# cursor_raw.execute(sql)
# rows = cursor_raw.fetchall()
# for row in rows:
#     print(row)
# con_raw.close()


con = sqlite3.connect(operating_db)
# con.row_factory = sqlite3.Row
cursor = con.cursor()

sql = """SELECT * FROM tblCatalogs WHERE period = ? and code = ?;""" # ID_tblCatalog
par = (68, '0000')

cursor.execute(sql, par)
rows = cursor.fetchall()

print(rows[0])

for row in rows:
    print(row)
con.close()





# curs.execute(
#     "SELECT weight FROM Equipment WHERE name = ? AND price = ?",
#     ["lead", 24],
# )
# curs.execute(
#     "SELECT weight FROM Equipment WHERE name = :name AND price = :price",
#     {"name": "lead", "price": 24},
# )