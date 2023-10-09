
CREATE TABLE IF NOT EXISTS tblTables
                    (
                        ID_tblTable INTEGER PRIMARY KEY NOT NULL,
                        code TEXT NOT NULL,
                        description TEXT NOT NULL,
                        FK_tblTables_tblSubSections INTEGER NOT NULL,
                        FOREIGN KEY (FK_tblTables_tblSubSections) REFERENCES tblSubSections(ID_tblSubSection),
                        UNIQUE (code)
                    );

                   
INSERT INTO tblTables (code, description, FK_tblTables_tblSubSections) VALUES 
	('5.10-7-1-0-32', 'Распределительные пункты и трансформаторные подстанции', 0), 
	('5.10-9-1-0-37', 'Электроналадочные работы технических средств АСУЭ в жилом доме', 0),
	('5.10-11-2-0-43', 'Сети связи и сигнализации в поликлиниках', 0);                   