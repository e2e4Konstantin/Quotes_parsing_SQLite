sql_queries = {
    "delete_table_raw_quote": """DROP TABLE IF EXISTS tblRawQuotes;""",
    "delete_table_raw_catalog": """DROP TABLE IF EXISTS tblRawCatalog;""",

    "create_table_chapters": """CREATE TABLE IF NOT EXISTS tblChapters (ID_tblChapter INTEGER PRIMARY KEY NOT NULL, code TEXT NOT NULL, description TEXT NOT NULL, UNIQUE (code));""",
    "create_index_chapters": """CREATE UNIQUE INDEX idx_code_tblChapters ON tblChapters (code);""",
    "insert_chapters_from_catalog": r"""INSERT INTO tblChapters (code, description) SELECT PRESSMARK, TITLE FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+$";""",

    # --- Collections
    "create_table_collections": """CREATE TABLE IF NOT EXISTS tblCollections(ID_tblCollections INTEGER PRIMARY KEY NOT NULL, code TEXT NOT NULL, description TEXT NOT NULL, FK_tblCollections_tblChapters INTEGER NOT NULL, FOREIGN KEY (FK_tblCollections_tblChapters) REFERENCES tblChapters(ID_tblChapter), UNIQUE (code));""",
    "create_index_collections": """CREATE UNIQUE INDEX idx_code_tblCollections ON tblCollections (code);""",
    "insert_collections_from_catalog": r"""
                INSERT INTO tblCollections (code, description, FK_tblCollections_tblChapters)
                SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblChapters.ID_tblChapter 
                FROM tblRawCatalog 
                JOIN tblChapters ON tblRawCatalog.PARENT_PRESSMARK = tblChapters.code
                WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+$";
            """,

    # --- Sections
    "create_table_sections": """CREATE TABLE IF NOT EXISTS tblSections (ID_tblSections INTEGER PRIMARY KEY NOT NULL, code TEXT NOT NULL, description TEXT NOT NULL, FK_tblSections_tblCollections INTEGER NOT NULL,	FOREIGN KEY (FK_tblSections_tblCollections) REFERENCES tblCollections(ID_tblCollections), UNIQUE (code));""",
    "create_index_sections": """CREATE UNIQUE INDEX idx_code_tblSections ON tblSections (code);""",
    "insert_sections_from_catalog": r"""
                INSERT OR IGNORE INTO tblSections (code, description, FK_tblSections_tblCollections)
                SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblCollections.ID_tblCollections
                FROM tblRawCatalog 
                JOIN tblCollections ON tblRawCatalog.PARENT_PRESSMARK = tblCollections.code
                WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+-\d+$";
     """,
    # --- SubSections

    "create_table_subsections": """
                CREATE TABLE IF NOT EXISTS tblSubSections
                    (
                        ID_tblSubSections				INTEGER PRIMARY KEY NOT NULL,
                        code	 						TEXT NOT NULL,								
                        description						TEXT NOT NULL,
                        FK_tblSubSections_tblSections	INTEGER NOT NULL,	
                        FOREIGN KEY (FK_tblSubSections_tblSections) REFERENCES tblSections(ID_tblSections),
                        UNIQUE (code)
                    );
                """,
    "create_index_subsections": r"""""",
    "insert_subsections_from_catalog": """ """,

    # --- Tables
    "create_table_tables": """
                CREATE TABLE IF NOT EXISTS tblTables
                    (
                        ID_tblTable					INTEGER PRIMARY KEY NOT NULL,
                        code	 					TEXT NOT NULL,
                        description					TEXT NOT NULL,
                        FK_tblTables_tblSubSections	INTEGER NOT NULL,
                        FOREIGN KEY (FK_tblTables_tblSubSections) REFERENCES tblSubSections(ID_tblSubSection),
                        UNIQUE (code)
                    );
                """,
    "create_index_tables": r"""CREATE UNIQUE INDEX IF NOT EXISTS idx_code_tblTable ON tblTables (code);""",

    # --- Quotes
    "create_table_quotes": """
                CREATE TABLE IF NOT EXISTS tblQuotes
                    (
                        ID_tblQuote				INTEGER PRIMARY KEY NOT NULL,
                        code	 				TEXT NOT NULL,								
                        description				TEXT NOT NULL,
                        FK_tblQuotes_tblTables	INTEGER NOT NULL,	
                        FOREIGN KEY (FK_tblQuotes_tblTables) REFERENCES tblTables(ID_tblTable),
                        UNIQUE (code)
                    );
                """,
    "create_index_quote": """CREATE UNIQUE INDEX IF NOT EXISTS idx_code_tblQuotes ON tblQuotes (code);""",
}





