sql_selects = {

    "select_all_subsections":               """SELECT * FROM tblSubSections;""",
    "select_all_subsections_code":          """SELECT code FROM tblSubSections;""",
    "select_subsections_code_for_period":   """SELECT code FROM tblSubSections WHERE period = ?;""",

    "select_name_catalog_items":   """SELECT ID_tblCatalogItem FROM tblCatalogItems WHERE name IS ?;""",

    "select_period_code_catalog":   """SELECT ID_tblCatalog FROM tblCatalogs WHERE period = ? and code = ?;""",

}

sql_update = {

    "update_catalog_id_parent": """UPDATE tblCatalogs SET ID_parent = ? WHERE ID_tblCatalog = ?;""",


}



