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