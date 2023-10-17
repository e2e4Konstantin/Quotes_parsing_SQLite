import sqlite3
from pandas import DataFrame
import os
from data_extraction import read_data_frame
from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates


# def write_quotes_to_db(quotes_data: DataFrame, db_name: str):
#     """
#     Записывает расценки из DF в базу данных.
#     :param data: Расценки
#     :param db_name: Имя файла базы данных
#     :return:
#     """
#     with dbControl(db_name) as db:
#         # cursor.execute(sql_creates["delete_table_raw_quote"])
#         quotes_data.to_sql(name=sql_creates["table_name_raw_quotes"], con=db.connection, if_exists='append', index=False)
#
#
# def write_catalog_to_db(catalog_data: DataFrame, db_name: str):
#     """
#     Записывает каталог из DF в базу данных.
#     :param catalog_data: Каталог
#     :param db_name: Имя файла базы данных
#     :return:
#     """
#     with dbControl(db_name) as db:
#         # cursor.execute(sql_creates["delete_table_raw_catalog"])
#         catalog_data.to_sql(name=sql_creates["table_name_raw_catalog"], con=db.connection, if_exists='append', index=False)


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
