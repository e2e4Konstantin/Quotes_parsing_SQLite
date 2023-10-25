# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite

import os
import re
import sqlite3
from icecream import ic

from data_extraction import read_data_frame, info_data_frame
from data_storage import (dbControl, sql_creates, read_raw_file_data_to_db, read_raw_statistics_data_to_db,
                          update_statistics_from_raw_data,
                          create_tables, transfer_raw_quotes,
                          fill_catalog_items, transfer_raw_data_to_catalog, catalog_print)
from config import DataFile


def read_raw_data_to_db(db_path: str, db_name):
    file_names_periods = [
        DataFile(r"catalog_3_68.xlsx", 68), DataFile(r"catalog_4_68.xlsx", 68), DataFile(r"catalog_5_67.xlsx", 67),
        DataFile(r"catalog_6_68.xlsx", 68), DataFile(r"catalog_10_68.xlsx", 68),
    ]
    sources_place = r"src"

    files = [DataFile(os.path.join(db_path, sources_place, file.name), file.period) for file in file_names_periods]
    ic(files)

    statistics_file = r"statistics_all_68.xlsx"
    statistics = DataFile(os.path.join(path, sources_place, statistics_file), 68)
    ic(statistics)

    # удаляем все таблицы из БД
    with dbControl(db_name) as db:
        db.connection.execute(sql_creates["delete_table_raw_quote"])
        db.connection.execute(sql_creates["delete_table_raw_catalog"])
        db.connection.execute(sql_creates["delete_table_raw_statistics"])
    for file in files:
        read_raw_file_data_to_db(db_name, data_file=file)

    read_raw_statistics_data_to_db(raw_db, statistics)



if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    # path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"

    raw_db_name = r"output\RawCatalog.sqlite"
    raw_db = os.path.join(path, raw_db_name)
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)

    # # читаем данные из исходных файлов во raw БД
    # # читаем статистику в отдельную таблицу
    # read_raw_data_to_db(path, raw_db)
    # d = dbControl(raw_db)
    # d.inform()
    # d.close()

    # # создаем структуру БД
    # create_tables(operating_db)
    # # создаем справочник объектов каталога
    # fill_catalog_items(operating_db)
    # transfer_raw_data_to_catalog(operating_db, raw_db)
    #
    # transfer_raw_quotes(operating_db, raw_db)
    #
    update_statistics_from_raw_data(operating_db, raw_db)

    # catalog_print(operating_db, period)
    #
    # d = dbControl(operating_db)
    # d.inform()
    # d.close()
