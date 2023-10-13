import sqlite3
import os

path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
# path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"

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

def get_id(cursor: sqlite3.Cursor, query: str, *args) -> int | None:
    """ Выбрать id записи по запросу """
    try:
        result = cursor.execute(query, args)
        if result:
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error as error:
        print(f"ошибка поиск в БД Sqlite3: {' '.join(error.args)}\n\t", f"получить id записи {args}")
    return None


con = sqlite3.connect(operating_db)
# con.row_factory = sqlite3.Row
cur = con.cursor()

sql = """SELECT * FROM tblCatalogs WHERE period = ? and code = ?;""" # ID_tblCatalog
par = (68, '0000')

id = get_id(cur, sql, 68, '0000')
# id = get_id(cur, sql)
print(id)
#
#
# rowCount = cursor.execute(sql, par)
# print(rowCount)
# print(cursor.__dir__())
# print(cursor.lastrowid)
# print(cursor.row_factory)
# print(cursor.rowcount)
# print(cursor.description)
#
# if rowCount :
#     rows = cursor.fetchall()
#     print(len(rows))
#     for row in rows:
#         print(row)

con.close()





# curs.execute(
#     "SELECT weight FROM Equipment WHERE name = ? AND price = ?",
#     ["lead", 24],
# )
# curs.execute(
#     "SELECT weight FROM Equipment WHERE name = :name AND price = :price",
#     {"name": "lead", "price": 24},
# )