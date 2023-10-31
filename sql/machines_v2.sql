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

CREATE UNIQUE INDEX IF NOT EXISTS idx_name_tblMachineItems ON tblMachineItems (name);

INSERT INTO tblMachineItems (name, eng_name, parent_item, rating) VALUES (?, ?, ?, ?);

UPDATE tblMachineItems
    SET ID_parent =
        (
            SELECT mi.ID_tblMachineItem
            FROM tblMachineItems mi
            WHERE mi.name = tblMachineItems.parent_item
        )
    WHERE tblMachineItems.name IN (SELECT cat.name FROM tblMachineItems cat);

ALTER TABLE tblMachineItems DROP COLUMN parent_item;

-- tblMachinesCatalog
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

CREATE UNIQUE INDEX IF NOT EXISTS idx_period_code_tblMachinesCatalog ON tblMachinesCatalog (period, code);

-- ----- > Машины -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tblMachines
    (
        ID_tblMachine	INTEGER PRIMARY KEY NOT NULL,
        period          INTEGER NOT NULL,               -- номер периода
        code            TEXT    NOT NULL,               -- шифр
        description     TEXT    NOT NULL,               -- наименование
        measure         TEXT    NOT NULL,               -- единица измерения
        okp             TEXT    NOT NULL,               -- ОКП — классификатор продукции
        okpd2           TEXT    NOT NULL,               -- ОКПД2 — по видам деятельности
        base_price		REAL	DEFAULT 0.0 NOT NULL,   -- базисная цен
        wages			REAL	DEFAULT 0.0 NOT NULL,   -- заработная плата
        electricity		REAL	DEFAULT 0.0 NOT NULL,   -- электроэнергия
        statistics      INTEGER DEFAULT 0 NOT NULL,     -- статистика применений

        FK_tblMachines_tblMachinesCatalog INTEGER NOT NULL,
        FOREIGN KEY (FK_tblMachines_tblMachinesCatalog) REFERENCES tblMachinesCatalog (ID_tblMachinesCatalog),
        UNIQUE (period, code)
    );

CREATE UNIQUE INDEX IF NOT EXISTS idx_period_code_tblMachines ON tblMachines (period, code);