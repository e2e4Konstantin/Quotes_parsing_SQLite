import sqlite3


# As of some recent version of Python (I am using 3.9.4) it has become even easier to get a dictionary of results
# from sqlite3. It is in the documentation for Python. Essentially just make the connection equal to a sqlite3.Row
# and off you go.

def try_insert(labor_cursor: sqlite3.Cursor, query: str, src_data: tuple, message: str) -> int | None:
    """ Пытается выполнить запрос на вставку записи в БД"""
    try:
        result = labor_cursor.execute(query, src_data)
        if result:
            return result.lastrowid
    except sqlite3.Error as error:
        print(f"SQLite error: {' '.join(error.args)},\t{message!r}")
    return None


con1 = sqlite3.connect("programs_aux.sqlite")
con1.row_factory = sqlite3.Row
cur1 = con1.cursor()
sql = 'select * from Main where watched is 0 order by Genre, Folder_runtime'
cur1.execute(sql)

rows = cur1.fetchall()
for row in rows:
    print(row['Title'])

con1.close()


curs.execute(
    "SELECT weight FROM Equipment WHERE name = ? AND price = ?",
    ["lead", 24],
)
curs.execute(
    "SELECT weight FROM Equipment WHERE name = :name AND price = :price",
    {"name": "lead", "price": 24},
)