from icecream import ic

from data_storage import dbControl
from data_storage.sql_tools import sql_selects, sql_update
from data_storage.sql_creates import sql_creates
from data_storage.re_patterns import identify_item, items_data

item_name = 'directory'
db_filename = 'C:\\Users\\kazak.ke\\Documents\\Задачи\\Парсинг_параметризация\\SRC\\Quotes.sqlite'

with dbControl(db_filename) as db:
    # db.run_execute("""DROP TABLE IF EXISTS tblCatalogs;""")
    # db.run_execute(sql_creates["create_table_catalogs"])


    code = '0'
    period = 0
    # period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
    query = sql_selects["select_name_catalog_items"]
    id_catalog_items = db.get_id(query, items_data[item_name].name)
    ic(id_catalog_items)
    data = (period, code, 'Справочник расценок', code, 1, id_catalog_items)
    message = f"вставка 'Справочник' код: {code!r}"
    inserted_id = db.try_insert(sql_creates["insert_catalog"], data, message)
    if inserted_id:
        ic(inserted_id)
        # ссылка родителя самого на себя
        up_data = (inserted_id, inserted_id)
        message = f"UPDATE код родителя 'Справочник' {code!r}"

        inserted_id = db.run_execute(sql_update["update_catalog_id_parent"], up_data)
        # inserted_id = db.try_insert(sql_update["update_catalog_id_parent"], up_data, message)

        log = f"добавлена запись: {items_data[item_name].name.capitalize()!r} id: {inserted_id}"
        ic(log)
    else:
        log = f"запись НЕ добавлена: {items_data[item_name].name.capitalize()!r} id: {inserted_id}"
        ic(log)