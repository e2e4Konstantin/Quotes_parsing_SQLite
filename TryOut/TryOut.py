import sqlite3

# As of some recent version of Python (I am using 3.9.4) it has become even easier to get a dictionary of results
# from sqlite3. It is in the documentation for Python. Essentially just make the connection equal to a sqlite3.Row
# and off you go.

con1 = sqlite3.connect("programs_aux.sqlite")
con1.row_factory = sqlite3.Row
cur1 = con1.cursor()
sql = 'select * from Main where watched is 0 order by Genre, Folder_runtime'
cur1.execute(sql)

rows = cur1.fetchall()
for row in rows:
    print(row['Title'])

con1.close()