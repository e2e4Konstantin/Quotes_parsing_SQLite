
sql_creates = {
    "table_name_raw_catalog": """tblRawCatalog""",
    "delete_table_raw_catalog": """DROP TABLE IF EXISTS tblRawCatalog;""",
    "table_name_raw_quotes": """tblRawQuotes""",
    "delete_table_raw_quote": """DROP TABLE IF EXISTS tblRawQuotes;""",

    "select_items_from_raw_catalog": """SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP ?;""",

    "select_raw_catalog_code_re": """SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP ?;""",

    "select_all_raw_catalog": """SELECT * FROM tblRawCatalog;""",

    "select_quotes_from_raw": """SELECT * FROM tblRawQuotes""",



    # --- > Расценки --------------------------------------------------------------------------------------------
    # поля: id, период действия, шифр, содержание, измеритель, родительская расценка,
    # id элемента каталога к которому принадлежит расценка.
    #
    "drop_table_quotes": """DROP TABLE tblQuotes;""",

    "create_table_quotes": """
        CREATE TABLE IF NOT EXISTS tblQuotes (
            ID_tblQuote                 INTEGER PRIMARY KEY NOT NULL,
            period                      INTEGER NOT NULL,
            code                        TEXT    NOT NULL,
            description                 TEXT    NOT NULL,
            measure                     TEXT    NOT NULL,
            parent_quote                INTEGER REFERENCES tblQuotes (ID_tblQuote),
            absolute_code               TEXT    NOT NULL,  
            FK_tblQuotes_tblCatalogs    INTEGER NOT NULL,
            FOREIGN KEY (FK_tblQuotes_tblCatalogs) REFERENCES tblCatalogs (ID_tblCatalog),
            UNIQUE (code)
        );
        """,
    "create_index_quotes": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_period_code_tblQuotes ON tblQuotes (code);
        """,

    "insert_quote": """
        INSERT INTO tblQuotes (
            period, code, description, measure, parent_quote, absolute_code, FK_tblQuotes_tblCatalogs
            ) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,

    # для истории Расценок
    "create_table_history_quotes": """
        CREATE TABLE IF NOT EXISTS _tblQuotesHistory (
            _rowid                      INTEGER, 
            ID_tblQuote                 INTEGER NOT NULL,
            period                      INTEGER NOT NULL,
            code                        TEXT    NOT NULL,
            description                 TEXT    NOT NULL,
            measure                     TEXT    NOT NULL,
            parent_quote                INTEGER,
            absolute_code               TEXT    NOT NULL,
            FK_tblQuotes_tblCatalogs    INTEGER NOT NULL,
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
            INSERT INTO _tblQuotesHistory (
                _rowid, ID_tblQuote, period, code, description, measure, parent_quote, absolute_code, 
                FK_tblQuotes_tblCatalogs, _version, _updated
                )
            VALUES (
                new.rowid, new.ID_tblQuote, new.period, new.code, new.description, new.measure, 
                new.parent_quote, new.absolute_code, new.FK_tblQuotes_tblCatalogs, 1, 
                cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer)
                );
        END;
        """,

    # --- > Каталог ------------------------------
    "create_table_catalogs": """
        CREATE TABLE IF NOT EXISTS tblCatalogs
            (
                ID_tblCatalog			        INTEGER PRIMARY KEY NOT NULL,
                period                 	        INTEGER NOT NULL,
                code	 				        TEXT NOT NULL,								
                description				        TEXT NOT NULL,
                raw_parent                      TEXT NOT NULL,
                ID_parent                       INTEGER REFERENCES tblCatalogs (ID_tblCatalog), 
                FK_tblCatalogs_tblCatalogItems  INTEGER NOT NULL,	
                FOREIGN KEY (FK_tblCatalogs_tblCatalogItems) REFERENCES tblCatalogItems(ID_tblCatalogItem),
                UNIQUE (code)
            );
        """,

    "create_index_code_catalog": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_code_catalog ON tblCatalogs (code);
        """,

    "insert_catalog": """
        INSERT INTO tblCatalogs (period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems) 
        VALUES (?, ?, ?, ?, ?, ?);
        """,


    "create_table_history_catalog": """
        CREATE TABLE IF NOT EXISTS _tblCatalogsHistory (
                _rowid                          INTEGER, 
                ID_tblCatalog			        INTEGER,
                period                 	        INTEGER NOT NULL,
                code	 				        TEXT NOT NULL,								
                description				        TEXT NOT NULL,
                raw_parent                      TEXT NOT NULL,
                ID_parent                       INTEGER NOT NULL,
                FK_tblCatalogs_tblCatalogItems  INTEGER NOT NULL,	   
                _version INTEGER,
                _updated INTEGER
        );
        """,

    "create_index_catalog_history": """
        CREATE INDEX IF NOT EXISTS idx_rowid_catalog_history ON _tblCatalogsHistory (_rowid);
        """,

    "create_trigger_history_catalog": """
        CREATE TRIGGER IF NOT EXISTS tgr_insert_tblCatalogsHistory
        AFTER INSERT ON tblCatalogs
        BEGIN
            INSERT INTO _tblCatalogsHistory (
                _rowid, ID_tblCatalog, period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems, 
                _version, _updated
                )
            VALUES (
                new.rowid, new.ID_tblCatalog, new.period, new.code, new.description, new.raw_parent, new.ID_parent,
                new.FK_tblCatalogs_tblCatalogItems, 1, cast((julianday('now') - 2440587.5) * 86400 * 1000 as integer)
                );
        END;
        """,
    "create_trigger_update_catalog": """
        CREATE TRIGGER IF NOT EXISTS create_trigger_update_tblCatalogs
        AFTER UPDATE ON tblCatalogs
        FOR EACH ROW
        BEGIN
            INSERT INTO _tblCatalogsHistory (_rowid, ID_tblCatalog, period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems, _version, _updated)
            SELECT old.rowid, new.ID_tblCatalog, new.period, new.code, new.description, new.raw_parent, new.ID_parent, new.FK_tblCatalogs_tblCatalogItems, 
                (SELECT MAX(_version) FROM _tblCatalogsHistory WHERE _rowid = old.rowid) + 1, 
                cast((julianday('now') - 2440587.5) * 86400 * 1000 AS INTEGER)
            WHERE old.ID_tblCatalog != new.ID_tblCatalog or old.period != new.period or old.code != new.code or old.description != new.description or 
            old.raw_parent != new.raw_parent or old.ID_parent != new.ID_parent or  old.FK_tblCatalogs_tblCatalogItems != new.FK_tblCatalogs_tblCatalogItems;
        END;
    """,


    # --- > Справочник типов элементов каталога ------------------------------
    "create_table_catalog_items": """
        CREATE TABLE IF NOT EXISTS tblCatalogItems
            (
                ID_tblCatalogItem   INTEGER PRIMARY KEY NOT NULL,
                name       			TEXT NOT NULL,
                eng_name    		TEXT NOT NULL,
                parent_item         INTEGER REFERENCES tblCatalogItems (ID_tblCatalogItem),
                rank                INTEGER NOT NULL,
                UNIQUE (name)
            );
        """,

    "create_index_name_catalog_items": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_name_catalog_items ON tblCatalogItems (name);
        """,

    "insert_catalog_item": """INSERT INTO tblCatalogItems (name, eng_name, parent_item, rank) VALUES (?, ?, ?, ?);""",

}





