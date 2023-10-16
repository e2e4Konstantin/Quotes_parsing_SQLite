

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



CREATE VIEW viewCatalog AS
    SELECT
        main.period AS 'период',
        main.code AS 'шифр',
        tblCatalogItems.name AS 'название',
        main.description AS 'содержание',
        (SELECT link.code FROM tblCatalogs AS link WHERE link.ID_tblCatalog = main.ID_parent) AS 'шифр родителя',
        (SELECT link.description FROM tblCatalogs AS link WHERE link.ID_tblCatalog = main.ID_parent) AS 'родитель'
    FROM tblCatalogs AS main
    LEFT JOIN tblCatalogItems ON tblCatalogItems.ID_tblCatalogItem = main.FK_tblCatalogs_tblCatalogItems
    ORDER BY main.code


CREATE VIEW viewMainCatalog AS
    SELECT
        main.period AS 'период',
        tblCatalogItems.name AS 'название',
        main.code AS 'шифр',
        main.description AS 'содержание'
    FROM tblCatalogs AS main
    LEFT JOIN tblCatalogItems ON tblCatalogItems.ID_tblCatalogItem = main.FK_tblCatalogs_tblCatalogItems
    ORDER BY main.code




CREATE VIEW viewExtendCatalog AS
    SELECT
        main.ID_tblCatalog AS 'id',
        main.FK_tblCatalogs_tblCatalogItems AS id_item,
        main.period AS 'период',
        item.name AS 'название',
        main.code AS 'шифр',
        main.description AS 'содержание',
        main.ID_parent AS 'p.id',
        (SELECT link.code FROM tblCatalogs AS link WHERE link.ID_tblCatalog = main.ID_parent) AS 'р.шифр',
        (SELECT par_item.name FROM tblCatalogs AS m
            LEFT JOIN tblCatalogItems AS par_item ON par_item.ID_tblCatalogItem = m.FK_tblCatalogs_tblCatalogItems
            WHERE m.ID_tblCatalog = main.ID_parent)  AS 'р.название',
        (SELECT par_item.ID_tblCatalogItem FROM tblCatalogs AS m
            LEFT JOIN tblCatalogItems AS par_item ON par_item.ID_tblCatalogItem = m.FK_tblCatalogs_tblCatalogItems
            WHERE m.ID_tblCatalog = main.ID_parent)  AS 'par_id_item',
        (SELECT link.description FROM tblCatalogs AS link WHERE link.ID_tblCatalog = main.ID_parent) AS 'родитель'
    FROM tblCatalogs AS main
    LEFT JOIN tblCatalogItems AS item ON item.ID_tblCatalogItem = main.FK_tblCatalogs_tblCatalogItems
    ORDER BY main.code
