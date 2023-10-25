import sqlite3
from pandas import DataFrame
import os
from data_extraction import read_data_frame
from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates
from config import DataFile


def read_raw_file_data_to_db(db_name: str, data_file: DataFile):
    """ Читает данные из файла в DF. Добавляет столбец 'PERIOD'. Записывает DF в базу данных. """
    catalog_data = read_data_frame(excel_file_name=data_file.name, sheet_name='catalog', use_columns=[0, 1, 2])
    catalog_data['PERIOD'] = data_file.period
    quotes_data = read_data_frame(excel_file_name=data_file.name, sheet_name='quotes', use_columns=[0, 1, 2, 3])
    quotes_data['PERIOD'] = data_file.period
    with dbControl(db_name) as db:
        catalog_data.to_sql(name=sql_creates["table_name_raw_catalog"], con=db.connection, if_exists='append',
                            index=False)
        quotes_data.to_sql(name=sql_creates["table_name_raw_quotes"], con=db.connection, if_exists='append',
                           index=False)
    del catalog_data
    del quotes_data


def read_raw_statistics_data_to_db(db_name: str, statistics_file: DataFile):
    """ Читает статистику по расценкам из файла в DF. DF записывает в raw базу данных. """
    # читаем статистику в DataFrame
    statistics_data = read_data_frame(excel_file_name=statistics_file.name, sheet_name='statistics', use_columns=[0, 1])
    statistics_data['PERIOD'] = statistics_file.period
    with dbControl(db_name) as db:
        # создаем новую таблицу и записываем туда данные статистики
        statistics_data.to_sql(name=sql_creates["table_name_raw_statistics"], con=db.connection, if_exists='append',
                               index=False)
    del statistics_data
