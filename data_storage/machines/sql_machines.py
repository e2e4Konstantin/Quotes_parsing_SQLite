sql_creates_machines = {
    # --- > Имена таблиц для машин ----------------------------------------------------------------
    "table_name_machines":          """tblMachines""",
    "table_name_machines_catalog":  """tblMachinesCatalog""",
    "table_name_machine_items":     """tblMachineItems""",


    # ------ > Имена raw таблиц --------------------------------------------------------------------------
    "table_name_raw_machines_catalog":  """tblRawMachinesCatalog""",
    "table_name_raw_machines":          """tblRawMachines""",

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
                parent_item         INTEGER REFERENCES tblMachineItems (ID_tblMachineItem),
                rating              INTEGER NOT NULL,
                UNIQUE (name, rating)
            );
        """,
    "create_index_machine_items": """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_name_tblMachineItems ON tblMachineItems (name);
        """,

    # ------- > Каталог для машин -----------------------------------------------------------------
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
