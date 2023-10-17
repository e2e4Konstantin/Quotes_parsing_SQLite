import os
import sqlite3
from data_storage.db_settings import dbControl
from data_storage.sql_tools import sql_selects
from data_storage.re_patterns import split_code_int


def _index_look(src_list: list[tuple[int, str, str, int]] | None, target_value: int) -> int | None:
    if src_list:
        for i, x in enumerate(src_list):
            if x[3] == target_value:
                return i
    return None


def _get_directory(connection: sqlite3.Connection, period: int) -> tuple | None:
    item = 'справочник'
    result = connection.execute(sql_selects["select_period_item_catalog"], (period, item))
    row = result.fetchone()
    if row:
        return row['ID_tblCatalog'], row['period'], row['code'], row['name'], row['description']
    return None


def _slave_item_print(connection: sqlite3.Connection, master_id: int, deep_number: int = 0):
    """ Рекурсивная функция. Получает из БД строки у которых родитель == master_id,
        сортирует их по шифру, выводит на печать и запрашивает печать 'нижестоящей'.
    """
    tab = '    '
    result = connection.execute(sql_selects["select_parent_catalog"], (master_id,))
    rows = result.fetchall()
    if rows:
        deep_number += 1
        items = [x for x in rows]
        items.sort(key=lambda x: split_code_int(x['code']))
        for item in items:
            x = (item['period'], item['code'], item['item'], item['description'])
            print(f"{tab * deep_number}{x}")
            item_id = item['ID_tblCatalog']
            _slave_item_print(connection, item_id, deep_number)


def catalog_print(db_filename: str, period: int):
    """ Выводит на печать каталог для периода.  """
    with dbControl(db_filename) as db:
        direct = _get_directory(db.connection, period)
        direct_id = direct[0]
        print(direct)
        _slave_item_print(db.connection, direct_id, deep_number=0)


if __name__ == "__main__":
    # path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)
    period = 68
    catalog_print(operating_db, period)
