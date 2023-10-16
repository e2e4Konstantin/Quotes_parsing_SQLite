import os
import sqlite3
from data_storage.db_settings import dbControl
from data_storage.sql_tools import sql_selects
from file_features import output_message


def index_look(src_list: list[tuple[int, str, str, int]] | None, target_value: int) -> int | None:
    if src_list:
        for i, x in enumerate(src_list):
            if x[3] == target_value:
                return i
    return None


def get_directory(connection: sqlite3.Connection, period: int) -> tuple | None:
    item = 'справочник'
    result = connection.execute(sql_selects["select_period_item_catalog"], (period, item))
    row = result.fetchone()
    if row:
        return row['ID_tblCatalog'], row['period'], row['code'], row['name'], row['description']
    return None

def get_chapters(connection: sqlite3.Connection, period: int, directory_id: int):
    item = 'справочник'
    result = connection.execute(sql_selects["select_parent_catalog"], (directory_id, ))
    rows = result.fetchall()
    if rows:
        # ['ID_tblCatalog', 'period', 'code', 'description', 'raw_parent', 'ID_parent', 'FK_tblCatalogs_tblCatalogItems']
        r = [(x[0], x[1], x[2], x[3], x[4], x[5], x[6]) for x in rows]
        return r  #row['ID_tblCatalog'], row['period'], row['code'], row['name'], row['description']
    return None


def catalog_print(db_filename: str, period: int):
    """ Выводит на печать каталог для периода.
    """
    with dbControl(db_filename) as db:
        direct = get_directory(db.connection, period)
        print(direct)
        chapters = get_chapters(db.connection, period, direct[0])
        print(chapters)



        #
        # # получаем список названий и сортируем по старшинству
        # result = db.connection.execute(sql_selects["select_all_catalog_items"])
        #
        # item_rows = result.fetchall()
        # items = [(item['ID_tblCatalogItem'], item['name'], item['rank'])
        #          for item in item_rows]
        # items.sort(key=lambda x: x[2], reverse=True)
        # print(items)
        # tab_number = 0
        # tab = '   '
        # print(f"Период: {period}")
        # for item in items:
        #     result = db.connection.execute(sql_selects["select_period_item_catalog"], (period, item[1]))
        #     rows = result.fetchall()
        #     for row in rows:
        #         # x = (row['period'], row['code'], row['name'], row['description'])
        #         print(f"{tab * tab_number}{row['code']} {row['name']} {row['description']}")
        #     tab_number += 1


if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)
    period = 68
    catalog_print(operating_db, period)
