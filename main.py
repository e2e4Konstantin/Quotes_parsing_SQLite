# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite

import os
import re
import sqlite3
from icecream import ic

from data_extraction import read_data_frame, info_data_frame
from data_storage import (
    write_raw_catalog_file_to_db, write_raw_quotes_file_to_db, dbControl,
    read_raw_machines, write_raw_machines_to_operate_db, update_machines_statistics_from_raw_db,
    sql_creates, read_raw_statistics_data_to_db,
    update_statistics_from_raw_data,
    create_tables, transfer_raw_quotes,
    fill_catalog_items, transfer_raw_data_to_catalog, catalog_print
)
from config import DataFile, SrcData, SrcMachinesData
import typing


def files_prepare(
        db_path: str, catalog_filenames: typing.Sequence, quote_filenames: typing.Sequence, statistics_filename: str
) -> SrcData:
    """ Готовит полные имена файлов, выделяет номер периода, возвращает структуру списков (файл, период). """
    ic.disable()
    period = re.compile(r"_(\d+)\.")
    catalog_period_filenames = [period.search(name).groups()[0] for name in catalog_filenames]
    catalog_files = [DataFile(os.path.join(db_path, name), int(period))
                     for name, period in zip(catalog_filenames, catalog_period_filenames)]
    ic(catalog_files)
    quote_period_filenames = [period.search(name).groups()[0] for name in quote_filenames]
    quote_files = [DataFile(os.path.join(db_path, name), int(period))
                   for name, period in zip(quote_filenames, quote_period_filenames)]
    ic(quote_files)

    statistics_period = period.search(statistics_filename).groups()[0]
    statistics_file = DataFile(os.path.join(db_path, statistics_filename), period=int(statistics_period))
    ic(statistics_file)
    ic.enable()
    return SrcData(catalog_files, quote_files, statistics_file)


def read_raw_data_to_db(db_path: str, db_name):
    # получить полные имена файлов и выделить периоды
    src_data = files_prepare(db_path,
                             catalog_filenames=(r"TABLES_67.xlsx", r"TABLES_68.xlsx"),
                             quote_filenames=(r"WORK_PROCESS_67.xlsx", r"WORK_PROCESS_68.xlsx"),
                             statistics_filename=r"statistics_all_68.xlsx"            #r"Статистика_20_22.xlsx"
                             )
    ic(src_data.catalog, src_data.quote, src_data.statistics)
    # удаляем все таблицы из БД
    # with dbControl(db_name) as db:
    #     db.connection.execute(sql_creates["delete_table_raw_quote"])
    #     db.connection.execute(sql_creates["delete_table_raw_catalog"])
    #     db.connection.execute(sql_creates["delete_table_raw_statistics"])
    # for file in src_data.catalog:
    #     write_raw_catalog_file_to_db(db_name, data_file=file)
    # for file in src_data.quote:
    #     write_raw_quotes_file_to_db(db_name, data_file=file)
    read_raw_statistics_data_to_db(raw_db, src_data.statistics)
    with dbControl(db_name) as db:
        db.inform()


if __name__ == "__main__":
    # ic.disable()

    # output_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output"
    output_path = r".\output"
    output_path = os.path.abspath(output_path)

    # data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    data_path = r"C:\Users\kazak.ke\Documents\Задачи\Парсинг_параметризация\SRC"

    raw_db_name = r"RawCatalog.sqlite"
    raw_db = os.path.join(output_path, raw_db_name)
    operating_db_name = r"Quotes.sqlite"
    operating_db = os.path.join(output_path, operating_db_name)
    ic(raw_db, operating_db)

    # ---- Расценки--------------------------------------------------------------------------------
    # читаем данные из исходных файлов в raw БД. Статистику читаем в отдельную таблицу.
    # read_raw_data_to_db(data_path, raw_db)

    # создаем структуру БД
    # create_tables(operating_db)
    # # создаем справочник объектов каталога
    # # fill_catalog_items(operating_db)
    # transfer_raw_data_to_catalog(operating_db, raw_db)
    #
    # transfer_raw_quotes(operating_db, raw_db)
    #
    # update_statistics_from_raw_data(operating_db, raw_db)

    # catalog_print(operating_db, period)

    # ---- Машины ---------------------------------------------------------------------------------
    # machines_data = SrcMachinesData(data_path, "STRUCTURE_MACHINES_2_68.xlsx", "MACHINES_2_68.xlsx")
    # ic(machines_data)
    # # читать данные из excel файлов в черновую БД
    # read_raw_machines(raw_db, machines_data)
    # # перенести данные по машинам из черновой БД в рабочую
    # write_raw_machines_to_operate_db(raw_db, operating_db)

    update_machines_statistics_from_raw_db(operating_db, raw_db)


    # d = dbControl(operating_db)
    # d.inform()
    # d.close()
