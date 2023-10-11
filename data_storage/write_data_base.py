import sqlite3
from pandas import DataFrame

from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates


def write_quotes_to_db(quotes_data: DataFrame, db_name: str):
    """
    Записывает расценки из DF в базу данных.
    :param data: Расценки
    :param db_name: Имя файла базы данных
    :return:
    """
    with dbControl(db_name) as cursor:
        cursor.execute(sql_creates["delete_table_raw_quote"])
        quotes_data.to_sql(name=sql_creates["table_name_raw_quotes"], con=cursor.connection, if_exists='append', index=False)


def write_catalog_to_db(catalog_data: DataFrame, db_name: str):
    """
    Записывает каталог из DF в базу данных.
    :param catalog_data: Каталог
    :param db_name: Имя файла базы данных
    :return:
    """
    with dbControl(db_name) as cursor:
        cursor.execute(sql_creates["delete_table_raw_catalog"])
        catalog_data.to_sql(name=sql_creates["table_name_raw_catalog"], con=cursor.connection, if_exists='append', index=False)



# # if __name__ == "__main__":
#     from data_extraction import read_data_frame
#
#     file = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\src\catalog_3_68.xlsx"
#     data = read_data_frame(excel_file_name=file, sheet_name='catalog', use_columns=[0, 1, 2])
#
#     db_name = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output\rawCatalog.sqlite"
#     write_catalog_to_db(data, db_name)

#     name = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output\Quotes.sqlite"
#     d = dbControl(name)
#     d.inform_db()
#     d.close_db()
#
#     with dbControl(name) as cursor:
#         cursor.execute('SELECT SQLITE_VERSION()')
#         print(f"SQLite version: {cursor.fetchone()[0]}")

