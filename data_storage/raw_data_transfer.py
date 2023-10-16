import re
import sqlite3
import sys
import traceback

from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates
from data_storage.sql_tools import sql_selects, sql_update

from data_storage.re_patterns import identify_item, items_data, remove_wildcard, clear_code, title_extraction
from file_features import output_message


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
#


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
        raw_cursor.execute(sql_creates["select_quotes_from_raw"])
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


def fill_catalog_items(db_filename: str):
    """ Заполняет справочник элементов каталога.
        Первый элемент ссылается сам на себя. Старшинство определяется ItemCatalog.rank
        Глава ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        items = [(items_data[item].name, item, items_data[item].parent, items_data[item].rank)
                 for item in items_data.keys()]
        db.cursor.executemany(sql_creates["insert_catalog_item"], items)


def _insert_upper_level_items(item_name: str, db_filename: str, period: int) -> int | None:
    """ Вставляем синтетическую запись 'Справочник' для самого верхнего уровня
        Эта запись ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        code = '0'
        # period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
        query = sql_selects["select_name_catalog_items"]
        id_catalog_items = db.get_id(query, items_data[item_name].name)
        data = (period, code, 'Справочник расценок', code, 1, id_catalog_items)

        message = ' '.join(["вставка 'Справочник'", code])
        inserted_id = db.try_insert(sql_creates["insert_catalog"], data, message)
        # ссылка родителя самого на себя
        up_data = (inserted_id, inserted_id)
        message = ' '.join(["UPDATE код родителя 'Справочник'", code, f"период: {period}"])
        inserted_id = db.try_insert(sql_update["update_catalog_id_parent"], up_data, message)
        print(f"добавлена запись: {items_data[item_name].name.capitalize()!r} id: {inserted_id}, период {period}. ")
        return inserted_id


def _get_parent_id_item_id(item_name: str, connect: dbControl, period: int, parent_code: str) -> tuple:
    id_parent = connect.get_id(sql_selects["select_period_code_catalog"], period, parent_code)
    if id_parent is None:
        output_message(f"код родителя для {item_name!r} не найден:", f"шифр родителя: {parent_code!r}")
    id_catalog_items = connect.get_id(sql_selects["select_name_catalog_items"], items_data[item_name].name)
    if id_catalog_items is None:
        output_message(f"id для {item_name!r} не найден:", f"название: {items_data[item_name].name!r}")
    return id_parent, id_catalog_items


def _transfer_raw_items_to_catalog(item_name: str, operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает item_name в каталог из сырой базы в рабочую и создает ссылки на родителя """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        raw_db.cursor.execute(sql_creates["select_raw_catalog_code_re"], (items_data[item_name].pattern,))
        raw_items = raw_db.cursor.fetchall()
        if raw_items:
            success = []
            for item in raw_items:
                code = clear_code(item[1])
                check_types = identify_item(code)
                if len(check_types) > 0 and check_types[0] == item_name:
                    raw_parent = clear_code(item[0])

                    id_parent, id_items = _get_parent_id_item_id(item_name, operating_db, period, raw_parent)
                    if id_parent and id_items:
                        # period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
                        data = (
                            period, code, title_extraction(item[2], check_types[0]), raw_parent, id_parent, id_items
                        )
                        message = ' '.join([f"INSERT {item_name} {code!r} в каталог", code, f"период: {period}"])
                        inserted_id = operating_db.try_insert(sql_creates["insert_catalog"], data, message)
                        if inserted_id:
                            success.append(inserted_id)
                            # print(inserted_id, data, item)
                    else:
                        output_message(f"запись {item}", f"не добавлена в БД")
                else:
                    output_message(f"не распознан шифр записи {code}:", f"{items_data[item_name].pattern}")
            print(f"добавлено {len(success)} записей {items_data[item_name].name.capitalize()!r}, период {period}.")
        else:
            output_message(f"в сырой БД Sqlite3 не найдено ни одной записи типа: {items_data[item_name].name!r}",
                           f"{items_data[item_name].pattern}")


def transfer_raw_data_to_catalog(operating_db: str, raw_db: str, period: int):
    """ Заполняет каталог данными из сырой базы для указанного периода """
    _insert_upper_level_items('directory', operating_db, period)
    items = ['chapter', 'collection', 'section', 'subsection', 'table']
    for item in items:
        _transfer_raw_items_to_catalog(item, operating_db, raw_db, period)
