

SELECT * FROM sqlite_master WHERE type = 'table';


INSERT INTO users (first_name, last_name)
VALUES ('Jane', 'Doe')
RETURNING id;


x=my_conn.execute('''select last_insert_rowid()''')
id=x.fetchone()
print(id[0])


r_set=my_conn.execute(q,my_data)
print(r_set.lastrowid)

my_data=[(18, 'Big John', 'Four', 55, 'female'),
(19, 'Ronald', 'Six', 89, 'female'),
(20, 'ONe more', 'Six', 89, 'female')]
my_query="INSERT INTO student values(?,?,?,?,?)"
curs=my_conn.executemany(my_query,my_data)
print(curs.rowcount)



CREATE TABLE IF NOT EXISTS tblQuotes (
            ID_tblQuote            INTEGER PRIMARY KEY NOT NULL,
            period                 INTEGER NOT NULL,
            code                   TEXT    NOT NULL,
            description            TEXT    NOT NULL,
            measure                TEXT    NOT NULL,
            related_quote          INTEGER REFERENCES tblQuotes (ID_tblQuote), -- родительская расценка
            FK_tblQuotes_tblTables INTEGER NOT NULL,
            FOREIGN KEY (FK_tblQuotes_tblTables) REFERENCES tblTables (ID_tblTable),
            UNIQUE (code)
        );


CREATE TABLE IF NOT EXISTS _tblQuotesHistory (
            _rowid                 INTEGER,
            ID_tblQuote            INTEGER PRIMARY KEY NOT NULL,
            period                 INTEGER NOT NULL,
            code                   TEXT    NOT NULL,
            description            TEXT    NOT NULL,
            measure                TEXT    NOT NULL,
            related_quote          INTEGER,
            FK_tblQuotes_tblTables INTEGER NOT NULL,
            _version INTEGER,
            _updated INTEGER
        );