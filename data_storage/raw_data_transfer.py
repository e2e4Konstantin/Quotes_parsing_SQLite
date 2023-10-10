import re
import sqlite3
import sys
import traceback

from data_storage.db_settings import dbControl
from data_storage.sql_queries import sql_queries
from data_storage.re_patterns import item_patterns, extract_code, remove_wildcard, title_extraction


# Exception
# |__Warning
# |__Error
#    |__InterfaceError
#    |__DatabaseError
#       |__DataError
#       |__OperationalError
#       |__IntegrityError
#       |__InternalError
#       |__ProgrammingError
#       |__NotSupportedError


def try_insert(labor_cursor: sqlite3.Cursor, query_name: str, src_data: tuple, message: str) -> int | None:
    """ Пытается выполнить запрос на вставку записи в БД"""
    try:
        result = labor_cursor.execute(sql_queries[query_name], src_data)
        if result:
            return result.lastrowid
    except sqlite3.Error as error:
        print(f"SQLite error: {' '.join(error.args)},\t{message!r}")
    return None


def transfer_raw_subsection(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает Разделы из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_queries["select_items_from_raw_catalog"], (item_patterns['subsection'],))
        raw_subsections = raw_cursor.fetchall()
        for raw_subsection in raw_subsections:
            description = title_extraction(raw_subsection[2], item_name='subsection')
            code = raw_subsection[1].strip()
            raw_parent = raw_subsection[0].strip()
            data = (period, code, description, raw_parent, 0)
            message = ' '.join(['вставка Раздела', code])
            inserted_id = try_insert(operating_cursor, "insert_subsection", data, message)


def transfer_raw_tables(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает таблицы из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_queries["select_items_from_raw_catalog"], (item_patterns['table'],))
        raw_tables = raw_cursor.fetchall()
        for raw_table in raw_tables:
            description = title_extraction(raw_table[2], item_name='table')
            table_code = raw_table[1].strip()
            raw_parent = raw_table[0].strip()
            data = (period, table_code, description, raw_parent, 0)
            message = ' '.join(['вставка таблицы', table_code])
            inserted_id = try_insert(operating_cursor, "insert_table_to_tables", data, message)


def clean_quote(src_quote: tuple[str, str, str, str]) -> tuple[str, str, str, str]:
    """ Получает данные о расценке очищает/готовит их и возвращает обратно """
    table_code = extract_code(source=src_quote[0], item_name='table')
    quote_code = extract_code(source=src_quote[1], item_name='quote')
    description = remove_wildcard(src_quote[2])
    if description:
        words = description.split(maxsplit=1)
        if len(words) > 1:
            (first_word, rest) = words
            description = " ".join([first_word.capitalize(), rest])
        else:
            description = description.capitalize()
    measure = remove_wildcard(src_quote[3])
    return table_code, quote_code, description, measure


def transfer_raw_quotes(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает расценки из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_queries["select_quotes_from_raw"])
        quotes = raw_cursor.fetchall()
        for quote in quotes:
            table_code, quote_code, description, measure = clean_quote(quote)
            result = operating_cursor.execute("""select ID_tblTable from tblTables where code IS ?""", (table_code,))
            if result is None:
                print(f"для расценки {quote_code!r} не найдена таблица {table_code!r}")
            else:
                (found_table_id,) = result.fetchone()
                # print(f"{found_table_id=}")
                # period, code, description, measure, related_quote, FK_tblQuotes_tblTables
                data = (period, quote_code, description, measure, 0, found_table_id)
                message = ' '.join(['вставка расценки', quote_code])
                inserted_id = try_insert(operating_cursor, "insert_quote", data, message)
                # if inserted_id:
                #     print(f"вставлена расценка: {quote_code} id: {inserted_id}")
