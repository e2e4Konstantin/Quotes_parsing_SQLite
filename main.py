# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite

import os
import re
from pprint import pprint
import sqlite3

from pprint import pprint

from data_extraction import read_data_frame, info_data_frame
from data_storage import (write_catalog_to_db, write_quotes_to_db,
                          dbControl, create_tables, transfer_raw_subsection,
                          transfer_raw_tables, transfer_raw_quotes, add_null_subsections)

from data_storage import item_patterns, title_prefix, title_extraction


def get_raw_data(db_path: str, db_name):
    file_names = [r"src\catalog_3_68.xlsx", r"src\catalog_4_68.xlsx", r"src\catalog_5_67.xlsx"]
    files = [os.path.join(db_path, file) for file in file_names]
    for file in files:
        catalog_data = read_data_frame(excel_file_name=file, sheet_name='catalog', use_columns=[0, 1, 2])
        write_catalog_to_db(catalog_data, db_name)
        del catalog_data

        quotes_data = read_data_frame(excel_file_name=file, sheet_name='quotes', use_columns=[0, 1, 2, 3])
        write_quotes_to_db(quotes_data, db_name)
        del quotes_data


if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
    # path = r"C:\Users\kazak.ke\PycharmProjects\development\Quotes_parsing_SQLite"

    # читаем данные из исходных файлов во временную БД
    raw_db_name = r"output\RawCatalog.sqlite"
    raw_db = os.path.join(path, raw_db_name)
    operating_db_name = r"output\Quotes.sqlite"
    operating_db = os.path.join(path, operating_db_name)
    period = 68

    # get_raw_data(path, raw_db)
    # create_tables(operating_db)
    # transfer_raw_subsection(operating_db, raw_db, period)
    # transfer_raw_tables(operating_db, raw_db, period)
    # transfer_raw_quotes(operating_db, raw_db, period)

    add_null_subsections(operating_db,  period)

    # d = dbControl(operating_db)
    # d.inform_db()
    # d.close_db()
