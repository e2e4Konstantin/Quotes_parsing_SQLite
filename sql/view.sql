

CREATE VIEW quotes_view AS
    SELECT
        main.period AS 'период',
        tblTables.code AS 'таблица',
        main.code AS 'шифр',
        main.description AS 'содержание',
        main.measure AS 'измеритель',
        (SELECT code FROM tblQuotes AS sec WHERE sec.ID_tblQuote = main.related_quote) AS 'родитель'
    FROM tblQuotes AS main
    LEFT JOIN tblTables ON tblTables.ID_tblTable = main.FK_tblQuotes_tblTables
