import re
import sqlite3
import sys
import traceback
from icecream import ic

from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates
from data_storage.sql_tools import sql_selects, sql_update

from data_storage.re_patterns import (
    identify_item, items_data, remove_wildcard, clear_code,
    title_extraction, split_code, split_code_int, extract_code, check_code_item
)
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


def _clean_quote(src_quote: sqlite3.Row) -> tuple[int, str, str, str, str]:
    """ Получает данные о расценке очищает/готовит их и возвращает обратно """
    period = src_quote["PERIOD"]
    table_code = extract_code(source=src_quote["GROUP_WORK_PROCESS"], item_name='table')
    quote_code = extract_code(source=src_quote["PRESSMARK"], item_name='quote')
    description = remove_wildcard(src_quote["TITLE"])
    if description:
        words = description.split(maxsplit=1)
        if len(words) > 1:
            (first_word, rest) = words
            description = " ".join([first_word.capitalize(), rest])
        else:
            description = description.capitalize()
    measure = remove_wildcard(src_quote["UNIT_OF_MEASURE"])
    return period, table_code, quote_code, description, measure


def transfer_raw_quotes(operating_db_filename: str, raw_db_filename: str):
    """ Записывает расценки из сырой базы в рабочую """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        ic()
        result = raw_db.connection.execute(sql_creates["select_quotes_from_raw"])
        if result:
            rows = result.fetchall()
            success = []
            quotes = [x for x in rows]
            quotes.sort(key=lambda x: split_code_int(x['PRESSMARK']))
            for quote in quotes:
                period, table_code, quote_code, description, measure = _clean_quote(quote)
                query = sql_selects["select_period_code_catalog"]
                result = operating_db.connection.execute(query, (period, table_code,))
                if result is None:
                    print(f"для расценки {quote_code!r} не найдена таблица {table_code!r}")
                else:
                    (found_table_id,) = result.fetchone()
                    # print(f"{found_table_id=}")
                    # period, code, description, measure, statistics, parent_quote, absolute_code, FK_tblQuotes_tblTables
                    parent_quote = 0
                    statistics = 0
                    absolute_code = f"{table_code}-{split_code(quote_code)[-1]}"
                    data = (period, quote_code, description, measure, statistics, parent_quote, absolute_code, found_table_id)
                    message = f"вставка расценки {quote_code}"
                    inserted_id = operating_db.try_insert(sql_creates["insert_quote"], data, message)
                    if inserted_id:
                        success.append(inserted_id)
                    #     print(f"вставлена расценка: {quote_code} id: {inserted_id}")
            log = f"добавлено {len(success)} записей {items_data['quote'].name.capitalize()!r}."
            ic(log)


def fill_catalog_items(db_filename: str):
    """ Заполняет справочник элементов каталога.
        Первый элемент ссылается сам на себя. Старшинство определяется ItemCatalog.rank
        Глава ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        items = [(items_data[item].name, item, items_data[item].parent, items_data[item].rank)
                 for item in items_data.keys()]
        db.cursor.executemany(sql_creates["insert_catalog_item"], items)


def _insert_upper_level_items(item_name: str, db_filename: str) -> int | None:
    """ Вставляем синтетическую запись 'Справочник' для самого верхнего уровня
        Эта запись ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        code = '0'
        # period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
        query = sql_selects["select_name_catalog_items"]
        id_catalog_items = db.get_id(query, items_data[item_name].name)
        data = (1, code, 'Справочник расценок', code, 1, id_catalog_items)
        message = f"вставка 'Справочник' {code}"
        inserted_id = db.try_insert(sql_creates["insert_catalog"], data, message)
        # ссылка родителя самого на себя
        up_data = (inserted_id, inserted_id)
        message = f"UPDATE код родителя 'Справочник' {code!r}"
        inserted_id = db.try_insert(sql_update["update_catalog_id_parent"], up_data, message)
        log = f"добавлена запись: {items_data[item_name].name.capitalize()!r} id: {inserted_id}"
        ic(log)
        return inserted_id


def _get_item_id(code: str, period: int, db: dbControl) -> int | None:
    """ Ищем в таблице Каталога запись по шифру и периоду """
    id_parent = db.get_id(sql_selects["select_period_code_catalog"], period, code)
    if id_parent is None:
        output_message(f"В каталоге не найдена запись:", f"шифр: {code!r} и период: {period}")
    return id_parent


def _get_type_id(item_name: str, db: dbControl) -> int | None:
    """ Ищем в таблице типов объектов нужный тип, возвращаем id """
    id_catalog_items = db.get_id(sql_selects["select_name_catalog_items"], items_data[item_name].name)
    if id_catalog_items is None:
        output_message(f"В таблице типов не найден тип {item_name!r}:",
                       f"название: {items_data[item_name].name!r}")
    return id_catalog_items


def _transfer_raw_items_to_catalog(item_name: str, operating_db_filename: str, raw_db_filename: str):
    """ Записывает item_name в каталог из сырой базы в рабочую и создает ссылки на родителя """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        # ищем в сырой БД объекты типа item_name
        result = raw_db.connection.execute(sql_creates["select_raw_catalog_code_re"], (items_data[item_name].pattern,))
        if result:
            raw_items = result.fetchall()
            success = []
            for item in raw_items:
                code = clear_code(item["PRESSMARK"])
                # по коду определяем тип записи и проверяем на соответствие
                if check_code_item(code, item_name):
                    value = item["PARENT_PRESSMARK"]
                    raw_parent_code = clear_code(value) if value is not None else "0"
                    period = item["PERIOD"]
                    parent_period = period if item_name != "chapter" else 1
                    # получить id родителя
                    id_parent = _get_item_id(raw_parent_code, parent_period, operating_db )
                    # получить id типа записи
                    id_items = _get_type_id(item_name, operating_db)
                    if id_parent and id_items:
                        description = title_extraction(item["TITLE"], item_name)
                        #       period, code, description, raw_parent, ID_parent, FK_tblCatalogs_tblCatalogItems
                        data = (period, code, description, raw_parent_code, id_parent, id_items)
                        message = f"INSERT {item_name} {code!r} в каталог {code} период: {period}"
                        inserted_id = operating_db.try_insert(sql_creates["insert_catalog"], data, message)
                        if inserted_id:
                            success.append(inserted_id)
                    else:
                        output_message(f"запись {tuple(item)}", f"не добавлена в БД")
                else:
                    output_message(f"не распознан шифр записи {code}:", f"{items_data[item_name].pattern}")
            log = f"добавлено {len(success)} записей {items_data[item_name].name.capitalize()!r}."
            ic(log)
        else:
            output_message(f"в сырой БД Sqlite3 не найдено ни одной записи типа: {items_data[item_name].name!r}",
                           f"{items_data[item_name].pattern}")


def transfer_raw_data_to_catalog(operating_db: str, raw_db: str):
    """ Заполняет каталог данными из сырой базы для указанного периода """
    ic()
    _insert_upper_level_items('directory', operating_db)
    items = ['chapter', 'collection', 'section', 'subsection', 'table']
    for item in items:
        _transfer_raw_items_to_catalog(item, operating_db, raw_db)


def update_statistics_from_raw_data(operating_db_file: str, raw_db_file: str):
    """ Обновляет статистику для каждой расценки из raw таблицы статистики """
    with dbControl(raw_db_file) as raw_db, dbControl(operating_db_file) as operate_db:
        result = operate_db.connection.execute(sql_selects["select_quotes_all"])
        if result:
            quotes = result.fetchall()
            success = []
            for quote in quotes:
                # print(tuple(quote))
                code = quote['code']
                period = quote['period']
                stat_result = raw_db.connection.execute(sql_creates["select_raw_statistics_code"], (period, code))
                if stat_result:
                    raw_quote_stat = stat_result.fetchone()
                    ic(raw_quote_stat)
                    update = operate_db.connection.execute(sql_update["update_quote_statistics_by_id"], (raw_quote_stat['POSITION'], quote['ID_tblQuote']))
                    success.append(tuple(raw_quote_stat))
            log = f"обновили статистику у {len(success)} расценок."
            ic(log)

        raw_6 = raw_db.connection.execute("""SELECT * FROM tblRawStatistics WHERE PRESSMARK REGEXP "^6\.\d+";""")
        raw_stat_chapter_6 = raw_6.fetchall()
        raw_list = [x['PRESSMARK'] for x in raw_stat_chapter_6]
        r_all = len(raw_list)
        print(f"6 глава, статистика, исходных записей: {r_all}, дублей: {r_all-len(set(raw_list))}")