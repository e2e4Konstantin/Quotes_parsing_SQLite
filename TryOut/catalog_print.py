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




def catalog_print(db_filename: str, period: int):
    """ Выводит на печать каталог для периода.
    """
    with dbControl(db_filename) as db:
        # получаем список названий и сортируем по старшинству
        result = db.connection.execute(sql_selects["select_all_catalog_items"])

        item_rows = result.fetchall()
        items = [(item['ID_tblCatalogItem'], item['name'], item['rank'])
                for item in item_rows]
        items.sort(key=lambda x: x[2], reverse=True)
        print(items)
        tab_number = 0
        tab = '\t'
        for item in items[:3]:
            result = db.connection.execute(sql_selects["select_period_item_catalog"], (period, item[1]))
            rows = result.fetchall()
            for row in rows:
                # print(row.keys())
                t = f"{tab * tab_number}"
                x = (row['period'], row['code'], row['name'], row['description'])
                print(t, x)
            tab_number +=1











if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)
    period = 68
    catalog_print(operating_db, period)
