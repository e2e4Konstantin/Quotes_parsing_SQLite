import re
import sqlite3
import sys
import traceback

from data_storage.db_settings import dbControl
from data_storage.sql_queries import sql_queries
from data_storage.re_patterns import item_patterns, extract_code, remove_wildcard, title_extraction


def transfer_raw_tables(operating_db_filename: str, raw_db_filename: str, period: int):
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_queries["select_tables_from_raw_catalog"], (item_patterns['table'],))
        raw_tables = raw_cursor.fetchall()
        for raw_table in raw_tables[:3]:
            description = title_extraction(raw_table[2], item_name='table')
            try:
                operating_cursor.execute(
                    sql_queries["insert_table_to_tblTables"], (period, raw_table[1].strip(), description, 0)
                )
            except sqlite3.Error as error:
                print(f"SQLite error: {' '.join(error.args)},\t{raw_table[1].strip()}")


def clean_quote(src_quote: tuple[str, str, str, str]) -> tuple[str, str, str, str]:
    table_code = extract_code(source=src_quote[0], item_name='table')
    quote_code = extract_code(source=src_quote[1], item_name='quote')
    description = remove_wildcard(src_quote[2])
    if description:
        (first_word, rest) = description.split(maxsplit=1)
        description = " ".join([first_word.capitalize(), rest])
    measure = remove_wildcard(src_quote[3])
    return table_code, quote_code, description, measure


def transfer_raw_quotes(operating_db_filename: str, raw_db_filename: str, period: int):
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_queries["select_quotes_from_raw"])
        quotes = raw_cursor.fetchall()
        for quote in quotes[:5]:
            table_code, quote_code, description, measure = clean_quote(quote)
            operating_cursor.execute("""select ID_tblTable from tblTables where code IS ?""", (table_code, ))
            print(f"{operating_cursor.fetchone()=}")


            # FK_tblQuotes_tblTables = operating_cursor.fetchone()
            # print(f"{FK_tblQuotes_tblTables}")

            print(f"{table_code=} {quote_code=} {description=} {measure=} | {quote=} ")
