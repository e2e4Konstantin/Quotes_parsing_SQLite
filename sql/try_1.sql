CREATE TABLE IF NOT EXISTS tblChapters 
(
	ID_tblChapter	INTEGER PRIMARY KEY NOT NULL,
	code 			TEXT NOT NULL,								
    description		TEXT NOT NULL,
	UNIQUE (code)
);
CREATE UNIQUE INDEX idx_code_tblChapters ON tblChapters (code);

SELECT * FROM tblRawCatalog WHERE PRESSMARK IN (1,2,3, 4);

SELECT PRESSMARK, TITLE FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+$";

SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+\.\d+$";

INSERT INTO tblChapters ( code, description) SELECT PRESSMARK, TITLE FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+$";

CREATE TABLE IF NOT EXISTS tblCollections
(
	ID_tblCollection	INTEGER PRIMARY KEY NOT NULL,
	code	 			TEXT NOT NULL,								
    description			TEXT NOT NULL,
	FK_tblCollections_tblChapters INTEGER NOT NULL,	
	FOREIGN KEY (FK_tblCollections_tblChapters) REFERENCES tblChapters(ID_tblChapter),
	UNIQUE (code)
);
CREATE UNIQUE INDEX idx_code_tblCollections ON tblCollections (code);

--INSERT INTO tblCollections 

SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblChapters.ID_tblChapter AS inCollection
FROM tblRawCatalog 
JOIN tblChapters ON tblRawCatalog.PARENT_PRESSMARK = tblChapters.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+$";

INSERT INTO tblCollections ( code, description, FK_tblCollections_tblChapters)
SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblChapters.ID_tblChapter 
FROM tblRawCatalog 
JOIN tblChapters ON tblRawCatalog.PARENT_PRESSMARK = tblChapters.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+$";


-- tblSections

CREATE TABLE IF NOT EXISTS tblSections
(
	ID_tblSection					INTEGER PRIMARY KEY NOT NULL,
	code	 						TEXT NOT NULL,								
    description						TEXT NOT NULL,
	FK_tblSections_tblCollections	INTEGER NOT NULL,	
	FOREIGN KEY (FK_tblSections_tblCollections) REFERENCES tblCollections(ID_tblCollections),
	UNIQUE (code)
);
CREATE UNIQUE INDEX idx_code_tblSection ON tblSections (code);

SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+\.\d+-\d+$";


SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblCollections.ID_tblCollections
FROM tblRawCatalog 
JOIN tblCollections ON tblRawCatalog.PARENT_PRESSMARK = tblCollections.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+-\d+$";


INSERT OR IGNORE INTO tblSections (code, description, FK_tblSections_tblCollections)
SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblCollections.ID_tblCollections
FROM tblRawCatalog 
JOIN tblCollections ON tblRawCatalog.PARENT_PRESSMARK = tblCollections.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+-\d+$";

--- SubSections

CREATE TABLE IF NOT EXISTS tblSubSections
(
	ID_tblSubSection				INTEGER PRIMARY KEY NOT NULL,
	code	 						TEXT NOT NULL,								
    description						TEXT NOT NULL,
	FK_tblSubSections_tblSections	INTEGER NOT NULL,	
	FOREIGN KEY (FK_tblSubSections_tblSections) REFERENCES tblSections(ID_tblSections),
	UNIQUE (code)
);
CREATE UNIQUE INDEX idx_code_tblSubSections ON tblSections (code);

SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+\.\d+(-\d+){2}$";

SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblSections.ID_tblSections
FROM tblRawCatalog 
JOIN tblSections ON tblRawCatalog.PARENT_PRESSMARK = tblSections.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+(-\d+){2}$";


--- Tables

CREATE TABLE IF NOT EXISTS tblTables
(
	ID_tblTable					INTEGER PRIMARY KEY NOT NULL,
	code	 					TEXT NOT NULL,								
    description					TEXT NOT NULL,
	FK_tblTables_tblSubSections	INTEGER NOT NULL,	
	FOREIGN KEY (FK_tblTables_tblSubSections) REFERENCES tblSubSections(ID_tblSubSection),
	UNIQUE (code)
);
CREATE UNIQUE INDEX idx_code_tblTable ON tblTables (code);

SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP "^\d+\.\d+(-\d+){4}$";

SELECT tblRawCatalog.PRESSMARK, tblRawCatalog.TITLE, tblSections.ID_tblSections
FROM tblRawCatalog 
JOIN tblSections ON tblRawCatalog.PARENT_PRESSMARK = tblSections.code
WHERE tblRawCatalog.PRESSMARK REGEXP "^\d+\.\d+(-\d+){2}$";



--- Quotes

CREATE TABLE IF NOT EXISTS tblQuotes
(
	ID_tblQuote				INTEGER PRIMARY KEY NOT NULL,
	code	 				TEXT NOT NULL,								
    description				TEXT NOT NULL,
	FK_tblQuotes_tblTables	INTEGER NOT NULL,	
	FOREIGN KEY (FK_tblQuotes_tblTables) REFERENCES tblTables(ID_tblTable),
	UNIQUE (code)
);

CREATE UNIQUE INDEX idx_code_tblQuotes ON tblQuotes (code);






