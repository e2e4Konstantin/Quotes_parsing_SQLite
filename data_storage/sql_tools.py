sql_selects = {

    "select_all_subsections": """SELECT * FROM tblSubSections;""",
    "select_all_subsections_code": """SELECT code FROM tblSubSections;""",
    "select_subsections_code_for_period": """SELECT code FROM tblSubSections WHERE period = ?;""",

    "select_name_catalog_items":    """SELECT ID_tblCatalogItem FROM tblCatalogItems WHERE name IS ?;""",
    "select_all_catalog_items":     """SELECT * FROM tblCatalogItems;""",
    "select_root_catalog_items":    """SELECT * FROM tblCatalogItems WHERE ID_tblCatalogItem = parent_item;""",




    "select_period_code_catalog":   """SELECT ID_tblCatalog FROM tblCatalogs WHERE period = ? and code = ?;""",
    "select_period_catalog":        """SELECT * FROM tblCatalogs WHERE period IS ?;""",
    "select_period_item_catalog":
        """
            SELECT ID_tblCatalog, period, code, item.name, description 
            FROM tblCatalogs 
            LEFT JOIN tblCatalogItems AS item ON item.ID_tblCatalogItem = FK_tblCatalogs_tblCatalogItems
            WHERE period = ? and item.name = ?;
        """,
    "select_parent_catalog":        """SELECT * FROM tblCatalogs WHERE id_parent = ? and id_parent <> ID_tblCatalog;""",

}

sql_update = {

    "update_catalog_id_parent": """UPDATE tblCatalogs SET ID_parent = ? WHERE ID_tblCatalog = ?;""",

}

sql_views = {

    # --- > Каталог ------------------------------
    "create_view_main_catalog": """
        CREATE VIEW IF NOT EXISTS viewMainCatalog AS
            SELECT
                main.period AS 'период',
                tblCatalogItems.name AS 'название',
                main.code AS 'шифр',
                main.description AS 'содержание'
            FROM tblCatalogs AS main
            LEFT JOIN tblCatalogItems ON tblCatalogItems.ID_tblCatalogItem = main.FK_tblCatalogs_tblCatalogItems
            ORDER BY main.code;
        """,

    "create_view_extended_catalog": """
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
    );
     """,

}
