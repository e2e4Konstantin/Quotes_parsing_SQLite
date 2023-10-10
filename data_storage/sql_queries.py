sql_queries = {
    "table_name_raw_catalog": """tblRawCatalog""",
    "delete_table_raw_catalog": """DROP TABLE IF EXISTS tblRawCatalog;""",
    "table_name_raw_quotes": """tblRawQuotes""",
    "delete_table_raw_quote": """DROP TABLE IF EXISTS tblRawQuotes;""",

    "select_items_from_raw_catalog": """SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP ?""",
    "select_quotes_from_raw": """SELECT * FROM tblRawQuotes""",

    # --- Tables
    "create_table_tables": """
                CREATE TABLE IF NOT EXISTS tblTables
                    (
                        ID_tblTable					INTEGER PRIMARY KEY NOT NULL,
                        period                      INTEGER NOT NULL,
                        code	 					TEXT NOT NULL,
                        description					TEXT NOT NULL,
                        raw_parent                  TEXT NOT NULL,
                        FK_tblTables_tblSubSections	INTEGER NOT NULL,
                        FOREIGN KEY (FK_tblTables_tblSubSections) REFERENCES tblSubSections(ID_tblSubSection),
                        UNIQUE (code)
                    );
                """,
    "create_index_tables": """CREATE UNIQUE INDEX IF NOT EXISTS idx_code_tblTable ON tblTables (code);""",

    "insert_table_to_tables": """
                INSERT INTO tblTables (period, code, description, raw_parent, FK_tblTables_tblSubSections) 
                VALUES (?, ?, ?, ?, ?);
                """,

    "create_table_history_tables": """
        CREATE TABLE IF NOT EXISTS _tblTablesHistory (
                _rowid                      INTEGER, 
                ID_tblTable                 INTEGER,    
                period                      INTEGER NOT NULL,
                code	 					TEXT NOT NULL,
                description					TEXT NOT NULL,
                FK_tblTables_tblSubSections	INTEGER NOT NULL,    
                _version INTEGER,
                _updated INTEGER
        );
        """,

    "create_index_tables_history": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_rowid_tables_history ON _tblTablesHistory (_rowid);
        """,

    "create_trigger_history_tables": """
        CREATE TRIGGER IF NOT EXISTS tgr_insert_tblTablesHistory
        AFTER INSERT ON tblTables
        BEGIN
            INSERT INTO _tblTablesHistory (_rowid, ID_tblTable, period, code, description, FK_tblTables_tblSubSections, _version, _updated)
            VALUES (new.rowid, new.ID_tblTable, new.period, new.code, new.description, new.FK_tblTables_tblSubSections, 1, cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer));
        END;
        """,


    # --- Quotes
    "drop_table_quotes": """DROP TABLE tblQuotes;""",
    "create_table_quotes": """
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
        """,
    "create_index_quotes": """CREATE UNIQUE INDEX IF NOT EXISTS idx_code_tblQuotes ON tblQuotes (code);""",

    "insert_quote": """
                INSERT INTO tblQuotes (period, code, description, measure, related_quote, FK_tblQuotes_tblTables) 
                VALUES (?, ?, ?, ?, ?, ?);
                """, #  RETURNING ID_tblQuote


    "create_table_history_quotes": """
        CREATE TABLE IF NOT EXISTS _tblQuotesHistory (
            _rowid                      INTEGER, 
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
        """,

    "create_index_quotes_history": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_rowid_quotes_history ON _tblQuotesHistory (_rowid);
        """,

    "create_trigger_history_quotes": """
        CREATE TRIGGER IF NOT EXISTS tgr_insert_tblQuotesHistory
        AFTER INSERT ON tblQuotes
        BEGIN
            INSERT INTO _tblQuotesHistory (_rowid, ID_tblQuote, period, code, description, 
                measure, related_quote, FK_tblQuotes_tblTables, _version, _updated)
            VALUES (new.rowid, new.ID_tblQuote, new.period, new.code, new.description, 
                new.measure, new.related_quote, new.FK_tblQuotes_tblTables, 1, 
                cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer));
        END;
        """,

    "create_table_subsections": """
            CREATE TABLE IF NOT EXISTS tblSubSections
                (
                    ID_tblSubSections				INTEGER PRIMARY KEY NOT NULL,
                    period                 			INTEGER NOT NULL,
                    code	 						TEXT NOT NULL,								
                    description						TEXT NOT NULL,
                    raw_parent                      TEXT NOT NULL,
                    FK_tblSubSections_tblSections	INTEGER NOT NULL,	
                    FOREIGN KEY (FK_tblSubSections_tblSections) REFERENCES tblSections(ID_tblSections),
                    UNIQUE (code)
                );
        """,

    "create_index_subsections": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_id_sub_sections ON tblSubSections (ID_tblSubSections);
        """,

    "insert_subsection": r"""
            INSERT INTO tblSubSections (period, code, description, raw_parent, FK_tblSubSections_tblSections) VALUES (?, ?, ?, ?, ?);
        """,

}





