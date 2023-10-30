sql_creates_machines = {
    # --- > Имена таблиц для машин ----------------------------------------------------------------
    "table_name_machines":          """tblMachines""",
    "table_name_machines_catalog":  """tblMachinesCatalog""",
    "table_name_machine_items":     """tblMachineItems""",


    # ------ > Имена raw таблиц --------------------------------------------------------------------------
    "table_name_raw_machines_catalog":  """tblRawMachinesCatalog""",
    "table_name_raw_machines":          """tblRawMachines""",
    "select_raw_machines_catalog_code_re": """SELECT * FROM tblRawMachinesCatalog WHERE PRESSMARK REGEXP ?;""",

    # --- > Удаление таблиц -----------------------------------------------------------------------
    "delete_table_machines":            """DROP TABLE IF EXISTS tblMachines;""",
    "delete_table_machines_catalog":    """DROP TABLE IF EXISTS tblMachinesCatalog;""",
    "delete_table_machine_items":       """DROP TABLE IF EXISTS tblMachineItems;""",

    "delete_index_machines":            """DROP INDEX IF EXISTS idx_period_code_tblMachines;""",
    "delete_index_machines_catalog":    """DROP INDEX IF EXISTS idx_period_code_tblMachinesCatalog;""",
    "delete_index_machine_items":       """DROP INDEX IF EXISTS idx_name_tblMachineItems;""",



    # --- > Создание таблиц -----------------------------------------------------------------------
    # ------- > Типы записей каталога -------------------------------------------------------------
    "create_table_machine_items": """
        CREATE TABLE IF NOT EXISTS tblMachineItems
            (
                ID_tblMachineItem   INTEGER PRIMARY KEY NOT NULL,
                name       			TEXT NOT NULL,
                eng_name    		TEXT NOT NULL,
                parent_item         TEXT NOT NULL,
                rating              INTEGER NOT NULL,
                ID_parent           INTEGER REFERENCES tblMachineItems (ID_tblMachineItem),
                UNIQUE (name, rating)
            );
        """,
    "create_index_machine_items": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_name_tblMachineItems ON tblMachineItems (name);
        """,
    "insert_machine_items": """
        INSERT INTO tblMachineItems (name, eng_name, parent_item, rating) VALUES (?, ?, ?, ?);
        """,
    "update_parent_references": """
        UPDATE tblMachineItems 
            SET ID_parent = 
                (
                    SELECT mi.ID_tblMachineItem 
                    FROM tblMachineItems mi 
                    WHERE mi.name = tblMachineItems.parent_item
                ) 
            WHERE tblMachineItems.name IN (SELECT cat.name FROM tblMachineItems cat);
        """,
    "delete_parent_item_column": """
        ALTER TABLE tblMachineItems DROP COLUMN parent_item;
    """,


    # ------- > Каталог для машин -----------------------------------------------------------------

    # ID_tblMachinesCatalog, period, code, description, raw_parent, ID_parent, ID_tblMachinesCatalog_tblMachineItems
    "create_table_machines_catalog": """
        CREATE TABLE IF NOT EXISTS tblMachinesCatalog
            (
                ID_tblMachinesCatalog	        INTEGER PRIMARY KEY NOT NULL,
                period                 	        INTEGER NOT NULL,
                code	 				        TEXT NOT NULL,
                description				        TEXT NOT NULL,
                raw_parent                      TEXT NOT NULL,
                ID_parent             			INTEGER REFERENCES tblMachinesCatalog (ID_tblMachinesCatalog),
                ID_tblMachinesCatalog_tblMachineItems INTEGER NOT NULL,
                FOREIGN KEY (ID_tblMachinesCatalog_tblMachineItems) REFERENCES tblMachineItems(ID_tblMachineItem),
                UNIQUE (period, code)
            );
        """,
    "create_index_machines_catalog": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_period_code_tblMachinesCatalog ON tblMachinesCatalog (period, code);
        """,

    # ------- > Машины -----------------------------------------------------------------
    "create_table_machines": """
        CREATE TABLE IF NOT EXISTS tblMachines
            (
                ID_tblMachine	INTEGER PRIMARY KEY NOT NULL,
                period          INTEGER NOT NULL, -- номер периода
                code            TEXT    NOT NULL, -- шифр
                description     TEXT    NOT NULL, -- наименование
                measure         TEXT    NOT NULL, -- единица измерения
                okp             TEXT    NOT NULL, -- ОКП — классификатор продукции
                okpd2           TEXT    NOT NULL, -- ОКПД2 — классификатор продукции по видам деятельности
                base_price		REAL	DEFAULT 0.0 NOT NULL,   -- базисная цен
                wages			REAL	DEFAULT 0.0 NOT NULL,   -- заработная плата
                electricity		REAL	DEFAULT 0.0 NOT NULL,   -- электроэнергия
                statistics      INTEGER DEFAULT 0 NOT NULL,     -- статистика применений
                
                FK_tblMachines_tblMachinesCatalog INTEGER NOT NULL,
                FOREIGN KEY (FK_tblMachines_tblMachinesCatalog) REFERENCES tblMachinesCatalog (ID_tblMachinesCatalog),
                UNIQUE (period, code)
            );
    """,
    "create_index_machines": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_period_code_tblMachines ON tblMachines (period, code);
    """,

}

# --- > Выборка элементов ---------------------------------------------------------------------
sql_tools_machines = {

    "select_name_item_machines":    """SELECT ID_tblMachineItem FROM tblMachineItems WHERE name = ?;""",
    "select_all_machine_items":     """SELECT * FROM tblMachineItems;""",

    "insert_machines_catalog": """
        INSERT INTO tblMachinesCatalog (period, code, description, raw_parent, ID_parent, ID_tblMachinesCatalog_tblMachineItems) 
        VALUES (?, ?, ?, ?, ?, ?);
        """,

    "update_machines_catalog_id_parent": """
        UPDATE tblMachinesCatalog SET raw_parent =?, ID_parent = ? WHERE ID_tblMachinesCatalog = ?;
        """,


    "select_items_machines_catalog": """
        SELECT tblMachinesCatalog.ID_tblMachinesCatalog 
        FROM tblMachinesCatalog
        LEFT JOIN tblMachineItems AS item ON item.ID_tblMachineItem = ID_tblMachinesCatalog_tblMachineItems
        WHERE item.name = ?;
        """,
}


