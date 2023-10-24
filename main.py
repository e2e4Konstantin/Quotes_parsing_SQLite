# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite

import os
import re
from pprint import pprint
import sqlite3

from pprint import pprint

from data_extraction import read_data_frame, info_data_frame
from data_storage import (dbControl, sql_creates, write_file_raw_data, update_statistics_from_raw_data,
                          create_tables, transfer_raw_quotes, write_statistics_raw_data,
                          fill_catalog_items, transfer_raw_data_to_catalog, catalog_print)



def get_raw_data(db_path: str, db_name):
    # file_names = [r"src\catalog_3_68.xlsx", r"src\catalog_4_68.xlsx", r"src\catalog_5_67.xlsx"]
    file_names = [r"src\catalog_6_68.xlsx", r"src\catalog_10_68.xlsx"]
    files = [os.path.join(db_path, file) for file in file_names]

    with dbControl(db_name) as db:
        db.connection.execute(sql_creates["delete_table_raw_quote"])
        db.connection.execute(sql_creates["delete_table_raw_catalog"])

    for file in files:
        write_file_raw_data(db_name, data_file=file)


if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    # path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"

    src_statistics_file = r"src\statistics_all_68.xlsx"
    stat_file = os.path.join(path, src_statistics_file)


    raw_db_name = r"output\RawCatalog.sqlite"
    raw_db = os.path.join(path, raw_db_name)
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)
    period = 68

    # # читаем данные из исходных файлов во raw БД
    # # читаем статистику в отдельную таблицу
    # get_raw_data(path, raw_db)
    # write_statistics_raw_data(raw_db, stat_file, period)
    # d = dbControl(raw_db)
    # d.inform()
    # d.close()

    # создаем структуру бд
    create_tables(operating_db)
    # создаем справочник объектов каталога
    fill_catalog_items(operating_db)
    transfer_raw_data_to_catalog(operating_db, raw_db, period)
    transfer_raw_quotes(operating_db, raw_db, period)

    update_statistics_from_raw_data(operating_db, raw_db)

    # catalog_print(operating_db, period)
    #
    # d = dbControl(operating_db)
    # d.inform()
    # d.close()
