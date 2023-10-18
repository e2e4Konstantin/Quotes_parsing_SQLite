import sqlite3
from pandas import DataFrame
import os
from data_extraction import read_data_frame
from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates


def write_file_raw_data(db_name: str, data_file: str):
    """ Читает данные из файла в DF. DF записывает в raw базу данных. """

    catalog_data = read_data_frame(excel_file_name=data_file, sheet_name='catalog', use_columns=[0, 1, 2])
    quotes_data = read_data_frame(excel_file_name=data_file, sheet_name='quotes', use_columns=[0, 1, 2, 3])
    with dbControl(db_name) as db:
        catalog_data.to_sql(name=sql_creates["table_name_raw_catalog"], con=db.connection, if_exists='append',
                            index=False)
        quotes_data.to_sql(name=sql_creates["table_name_raw_quotes"], con=db.connection, if_exists='append',
                           index=False)
    del catalog_data
    del quotes_data


def write_statistics_raw_data(db_name: str, statistics_file: str, period: int):
    """ Читает статистику по расценкам из файла в DF. DF записывает в raw базу данных. """
    # читаем статистику в DataFrame
    statistics_data = read_data_frame(excel_file_name=statistics_file, sheet_name='statistics', use_columns=[0, 1])
    statistics_data['PERIOD'] = period

    with dbControl(db_name) as db:
        # создаем новую таблицу и записываем туда данные статистики
        statistics_data.to_sql(
            name=sql_creates["table_name_raw_statistics"],
            con=db.connection, if_exists='append', index=False
        )
    del statistics_data

