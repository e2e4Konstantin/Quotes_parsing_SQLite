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


def try_execute(labor_cursor: sqlite3.Cursor, query: str, src_data: tuple, message: str) -> int | None:
    """ Пытается выполнить запрос на вставку записи в БД"""
    try:
        result = labor_cursor.execute(query, src_data)
        if result:
            return result.lastrowid
    except sqlite3.Error as error:
        # print(f"SQLite error: {' '.join(error.args)},\t{message!r}")
        output_message(f"ошибка исполнения запроса БД Sqlite3: {' '.join(error.args)}", f"{message}")

    return None



def transfer_raw_subsection(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает Разделы из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_creates["select_items_from_raw_catalog"], (item_patterns['subsection'],))
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
        raw_cursor.execute(sql_creates["select_items_from_raw_catalog"], (item_patterns['table'],))
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


def add_null_subsections(db_filename: str, period: int):
    """ Добавляем 0-подразделы """

    with dbControl(db_filename) as cursor:
        cursor.execute(sql_selects["select_subsections_code_for_period"], (period,))
        # ID_tblSubSections, period, code, description, raw_parent, FK_tblSubSections_tblSections
        # получить все коды и убрать номер подраздела оставить только уникальные разделы
        codes = set([
            '-'.join(code[0].split('-')[:-1])
            for code in cursor.fetchall()
        ])
        print(codes)


def fill_catalog_items(db_filename: str):
    """ Заполняет справочник элементов каталога.
        Первый элемент ссылается сам на себя. Старшинство определяется ItemCatalog.rank
        Глава ссылается сама на себя.
    """
    with dbControl(db_filename) as cursor:
        items = [(items_data[item].name, item, items_data[item].rank-1) for item in items_data.keys()]
        items[0] = (items[0][0], items[0][1], 1)
        cursor.executemany(sql_creates["insert_catalog_item"], items)


def insert_upper_level_items(cursor: sqlite3.Cursor, period: int):
    """ Вставляем синтетическую запись 'Справочник' для самого верхнего уровня
        Эта запись ссылается сама на себя.
    """
    code = '0000'
    data_main = (period, code, 'Справочник расценок', code, 1, 1)
    message = ' '.join(["вставка 'Справочник'", code])
    inserted_id = try_execute(cursor, sql_creates["insert_catalog"], data_main, message)
    # ссылка родителя самого на себя
    up_data = (inserted_id, inserted_id)
    message = ' '.join(["UPDATE код родителя 'Справочник'", code, f"период: {period}"])
    inserted_id = try_execute(cursor, sql_update["update_catalog_id_parent"], up_data, message)


def transfer_raw_chapter_to_catalog(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает 'Главы' в каталог из сырой базы в рабочую и создает ссылки на родителя"""
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        # искусственная корневая запись справочника
        # insert_upper_level_items(operating_cursor, period)
        # выбираем из сырой базы только главы
        print(f" глава {items_data['chapter'].pattern}")
        raw_cursor.execute(sql_creates["select_raw_catalog_code_re"], (items_data['chapter'].pattern, ) )
        raw_chapters = raw_cursor.fetchall()
        for chapter in raw_chapters:
            raw_code = clear_code(chapter[1])
            check_types = identify_item(raw_code)

            if len(check_types) > 0 and check_types[0] == 'chapter':
                # period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
                code = raw_code
                description = title_extraction(chapter[2], item_name=check_types[0])
                raw_parent = clear_code(chapter[0])

                result = operating_cursor.execute(sql_selects["select_period_code_catalog"], (period, '0000'))
                id_parent = result.fetchall()[0] if result else None

                result =  operating_cursor.execute(sql_selects["select_name_catalog_items"], (items_data['chapter'].name, ))
                fk_catalog_items = operating_cursor.fetchall()[0] if result else None

                data = (period, code, description, raw_parent, id_parent[0], fk_catalog_items[0])
                print(data, chapter)





def transfer_raw_catalog(operating_db_filename: str, raw_db_filename: str, period: int):
    """ Записывает Каталог из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_cursor, dbControl(operating_db_filename) as operating_cursor:
        raw_cursor.execute(sql_creates["select_all_raw_catalog"])
        raw_items = raw_cursor.fetchall()
        # искусственная корневая запись справочника
        insert_upper_level_items(operating_cursor, period)

        for raw_item in raw_items[:6]:
            check_types = identify_item(raw_item[1])
            if len(check_types) > 0:
                item_type = check_types[0]
                # period, code, description, raw_parent, parent, FK_tblCatalogs_tblCatalogItems
                code = clear_code(raw_item[1])
                description = title_extraction(raw_item[2], item_name=item_type)
                raw_parent = clear_code(raw_item[0])
                id_parent = '?'
                message = ' '.join(["SELECT id родителя 'Справочник'", code, f"период: {period}"])
                inserted_id = try_execute(cursor, sql_update["update_catalog_id_parent"], up_data, message)

                result = operating_cursor.execute("""select ID_tblTable from tblTables where code IS ?""",
                                                  (table_code,))
                if result is None:
                    print(f"для расценки {quote_code!r} не найдена таблица {table_code!r}")

                data = (period, code, description, raw_parent)
                # operating_cursor.execute(sql_creates["insert_catalog_item"], data)



            else:
                output_message("не могу определить тип строки каталога", raw_item)

            print(f"{raw_item}, {item_type!r}, {code!r}, {description!r}")
