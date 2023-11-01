import sqlite3

from icecream import ic
import os

from file_features import construct_abs_file_name, output_message_exit, output_message
from data_storage.db_settings import dbControl

from data_storage.machines.sql_machines import sql_creates_machines, sql_tools_machines
from data_storage.machines.machine_items import machine_items, extract_parent_code, machines_title_extraction

from data_storage.re_patterns import clear_code, remove_wildcard, keep_just_numbers, keep_just_numbers_dots


def _delete_machine_tables(db_filename: str):
    """ Удаляет таблицы и индексы для работы с 'Машинами' из рабочей БД. """
    with dbControl(db_filename) as db:
        db.cursor.execute(sql_creates_machines["delete_table_machines"])
        db.cursor.execute(sql_creates_machines["delete_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["delete_table_machine_items"])
        db.cursor.execute(sql_creates_machines["delete_index_machines"])
        db.cursor.execute(sql_creates_machines["delete_index_machines_catalog"])
        db.cursor.execute(sql_creates_machines["delete_index_machine_items"])


def _create_machine_tables(db_filename: str):
    """ Создает таблицы и индексы для работы с 'Машинами'. """
    with dbControl(db_filename) as db:
        db.cursor.execute(sql_creates_machines["create_table_machine_items"])
        db.cursor.execute(sql_creates_machines["create_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_table_machines"])

        db.cursor.execute(sql_creates_machines["create_index_machine_items"])
        db.cursor.execute(sql_creates_machines["create_index_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_index_machines"])

        db.cursor.execute(sql_creates_machines["create_view_machines"])
        db.cursor.execute(sql_creates_machines["create_view_machines_catalog"])


def _create_machine_catalog_items(db_filename: str):
    """ Заполняет справочник элементов каталога для 'Машин' Создает ссылки на родителей.
        Первый элемент ссылается сам на себя. Старшинство определяется tblMachineItems.rating
        Глава ссылается сама на себя.
    """
    # ('справочник', 'directory', 'справочник', 100), ('глава', 'chapter', 'справочник', 90)
    items = [(machine_items[item].name, item, machine_items[item].parent_item, machine_items[item].rating)
             for item in machine_items.keys()]
    items.sort(key=lambda x: x[3], reverse=True)

    with dbControl(db_filename) as db:
        result = db.connection.executemany(sql_creates_machines["insert_machine_items"], items)
        if result:
            result = db.run_execute(sql_creates_machines["update_parent_references"])
            if result:
                db.run_execute(sql_creates_machines["delete_parent_item_column"])
        else:
            output_message_exit("неудача, справочник элементов каталога для 'Машин'", "не заполнился")


def _insert_upper_level_items_to_catalog(item_name: str, db: dbControl) -> int | None:
    """ Вставляем синтетическую запись 'Справочник' для самого верхнего уровня каталога.
        Эта запись ссылается сама на себя.
    """
    # ID_tblMachinesCatalog, period, code, description, raw_parent, ID_parent, ID_tblMachinesCatalog_tblMachineItems
    id_catalog_items = db.get_id(sql_tools_machines["select_name_item_machines"], item_name)
    if id_catalog_items:
        code = '0'
        data = (1, code, 'Справочник расценок', code, 1, id_catalog_items)
        message = f"вставка 'Справочник' {code} в каталог 'Машин'"
        inserted_id = db.try_insert(sql_tools_machines["insert_machines_catalog"], data, message)
        # ссылка родителя самого на себя
        up_data = (inserted_id, inserted_id)
        message = f"UPDATE код родителя 'Справочник' {code!r} в каталоге 'Машин'"
        inserted_id = db.try_insert(sql_tools_machines["update_machines_catalog_id_parent"], up_data, message)
        log = f"добавлена запись: {item_name.capitalize()!r} id: {inserted_id}"
        ic(log)
        return inserted_id
    return None


def _get_item_id(db: dbControl, item_name: str) -> int | None:
    """ Ищем в таблице типов объектов нужный тип, возвращаем id """
    id_items = db.get_id(sql_tools_machines["select_name_item_machines"], item_name)
    if id_items is None:
        output_message(f"В БД: {db.path!r}:", f"не найден тип: {item_name!r}")
    return id_items


def _get_parent_item_id(db: dbControl, item_id: int) -> int:
    """ Получить id родительского типа, по id потомка: для 'группы' -> 'раздел'. """
    result = db.run_execute(sql_tools_machines["select_id_parent_item"], (item_id,))
    if result:
        row = result.fetchone()
        return row['ID_parent'] if row else 0
    return 0


def _get_parent_id(db: dbControl, code: str, period: int) -> int:
    parent_code = extract_parent_code(child_code=code)
    if parent_code == '0':
        period = 1
    return db.get_id(sql_tools_machines["select_id_by_period_code_machines_catalog"], period, parent_code)


def _get_code_by_id_from_catalog(catalog_db: dbControl, id_catalog: int) -> str:
    result = catalog_db.run_execute(sql_tools_machines["select_code_by_id_machines_catalog"], (id_catalog,))
    if result:
        row = result.fetchone()
        return row['code'] if row else ""
    return ""


def _insert_item_to_machines_catalog(catalog_db: dbControl, data: tuple) -> int:
    inserted_id = catalog_db.try_insert(sql_tools_machines["insert_machines_catalog"], data, f"{data}")
    return inserted_id


def _transfer_raw_catalog_items_to_machines(item_name: str, raw_db_filename: str, operating_db_filename: str):
    """ Записывает item_name в каталог из сырой базы каталога в рабочую и создает ссылки на родителя """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        # ищем в сырой БД объекты типа item_name
        result = raw_db.run_execute(
            sql_creates_machines["select_raw_machines_catalog_code_re"],
            (machine_items[item_name].pattern,))
        if result:
            rows = result.fetchall()
            # success = []
            for row in rows:
                # ic(tuple(row))
                period = row["PERIOD"]
                code = clear_code(row["PRESSMARK"])
                description = machines_title_extraction(row["TITLE"], item_name)
                id_item = _get_item_id(operating_db, machine_items[item_name].name)
                # ic(id_item)
                id_parent = _get_parent_id(operating_db, code, period)
                # ic(id_parent)
                if id_parent:
                    raw_parent_code = _get_code_by_id_from_catalog(operating_db, id_parent)
                    # period, code, description, raw_parent, ID_parent, ID_tblMachinesCatalog_tblMachineItems
                    data = (period, code, description, raw_parent_code, id_parent, id_item)
                    # ic(data)
                    _insert_item_to_machines_catalog(operating_db, data)
                else:
                    output_message_exit("не найден родитель для", f"период: {period}, шифр: {code}")
        else:
            output_message("не найдено ни одной записи в черновой БД для",
                           f"тип записи: {machine_items[item_name].name}")

# def _get_


def _create_machine_catalog(raw_db: str, operating_db: str):
    """ Для каталога 'Машин': Создает главную запись каталога.
        Готовит список категорий справочника отсортированный по старшинству.
        Последовательно от старших категорий к младшим заполняет каталог данными из черновой базы.
    """
    ic()
    items = []
    with dbControl(operating_db) as db:
        item_main = machine_items['directory'].name
        result = db.run_execute(sql_tools_machines["select_items_machines_catalog"], (item_main,))
        if len(list(result)) == 0:
            _insert_upper_level_items_to_catalog(item_main, db)
        result = db.run_execute(sql_tools_machines["select_all_machine_items"])
        if result:
            rows = result.fetchall()
            items = [x for x in rows if x['name'] not in ['справочник', 'машина']]
            items.sort(key=lambda x: x['rating'], reverse=True)
            ic([tuple(x) for x in items])
    if items:
        for item in items:
            ic(tuple(item))
            _transfer_raw_catalog_items_to_machines(item["eng_name"], raw_db, operating_db)
    else:
        output_message_exit("в справочнике категорий каталога Машин", "нет ни одной категории")


def _insert_raw_machine_to_operate_db(machine_data: sqlite3.Row, operating_db: dbControl) -> int:
    """ """
    # ID_tblMachine, period, code, description, measure, okp, okpd2, base_price, wages, electricity, statistics
    # "Шифр", "Наименование", "Ед.изм", "ОКП", "ОКПД2", "Базисная цена", "ЗП", "Электроэнергия", "PERIOD"
    period = machine_data["PERIOD"]
    code = machine_data["Шифр"]
    description = machines_title_extraction(machine_data["Наименование"], item_name='machine')
    measure = remove_wildcard(machine_data["Ед.изм"])
    okp = keep_just_numbers(machine_data["ОКП"])
    okpd2 = keep_just_numbers_dots(machine_data["ОКПД2"])
    base_price = float(machine_data["Базисная цена"])
    wages = float(machine_data["ЗП"])
    electricity = float(machine_data["Электроэнергия"])
    statistics = 0
    parent_id = _get_parent_id(operating_db, code, period)
    if parent_id < 2:
        output_message("не найден родитель для записи", f"{tuple(machine_data)}")
    data = (period, code, description, measure, okp, okpd2, base_price, wages, electricity, statistics, parent_id)
    # ic(data)
    inserted_id = operating_db.try_insert(sql_tools_machines["insert_machine"], data, f"{data}")
    return inserted_id


def _create_machine_data(raw_db_filename: str, operating_db_filename: str):
    """ Заполняет данные 'Машин' из сырой базы. Устанавливает ссылки на родительские элементы каталога. """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        ic()
        result = raw_db.run_execute(sql_creates_machines["select_all_raw_machines"])
        if result:
            rows = result.fetchall()
            count_row_machines = len(rows)
            count_operate_machines = 0
            print(f"всего машин в черновой базе: {count_row_machines}")
            for row in rows:
                # print(tuple(row))
                ins_id = _insert_raw_machine_to_operate_db(row, operating_db)
                if ins_id > 0:
                    count_operate_machines += 1
            print(f"записано машин в рабочую базу: {count_row_machines}")
        else:
            output_message_exit("не найдено ни одной записи для Машин в черновой БД",
                                f"таблица: {sql_creates_machines['table_name_machine_items']}")


def write_raw_machines_to_operate_db(raw_file_db: str, operating_file_db: str):
    """ Удаляет таблицы для машин из рабочей БД. Создает новые таблицы.
        Заполняет каталог машин данными из черновой БД. Записывает машины из черновой БД в рабочую."""
    _delete_machine_tables(operating_file_db)
    _create_machine_tables(operating_file_db)
    # заполняет категории справочника
    _create_machine_catalog_items(operating_file_db)
    # заполняет каталог
    _create_machine_catalog(raw_file_db, operating_file_db)
    # заполняет машины
    _create_machine_data(raw_file_db, operating_file_db)


if __name__ == "__main__":
    data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    # data_path = r"C:\Users\kazak.ke\Documents\Задачи\Парсинг_параметризация\SRC"

    # db_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output"
    db_path = r"..\..\output"
    db_path = os.path.abspath(db_path)
    db_name = r"Quotes.sqlite"
    dbf = construct_abs_file_name(db_path, db_name)
    ic(dbf)
    raw_db_name = r"RawCatalog.sqlite"
    rdbf = construct_abs_file_name(db_path, raw_db_name)
    ic(rdbf)

    write_raw_machines_to_operate_db(rdbf, dbf)
