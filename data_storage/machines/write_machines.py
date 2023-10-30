from icecream import ic

from file_features import construct_abs_file_name, output_message_exit
from data_storage.db_settings import dbControl

from data_storage.machines.sql_machines import sql_creates_machines, sql_tools_machines
from data_storage.machines.machine_items import machine_items

from data_storage.re_patterns import (
    identify_item, items_data, remove_wildcard, clear_code,
    title_extraction, split_code, split_code_int, extract_code, check_code_item
)

def delete_machine_tables(db_filename: str):
    """ Удаляет таблицы и индексы для работы с 'Машинами' из рабочей БД. """
    with dbControl(db_filename) as db:
        db.cursor.execute(sql_creates_machines["delete_table_machines"])
        db.cursor.execute(sql_creates_machines["delete_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["delete_table_machine_items"])
        db.cursor.execute(sql_creates_machines["delete_index_machines"])
        db.cursor.execute(sql_creates_machines["delete_index_machines_catalog"])
        db.cursor.execute(sql_creates_machines["delete_index_machine_items"])


def create_machine_tables(db_filename: str):
    """ Создает таблицы и индексы для работы с 'Машинами'. """
    with dbControl(db_filename) as db:
        db.cursor.execute(sql_creates_machines["create_table_machine_items"])
        db.cursor.execute(sql_creates_machines["create_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_table_machines"])
        db.cursor.execute(sql_creates_machines["create_index_machine_items"])
        db.cursor.execute(sql_creates_machines["create_index_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_index_machines"])


def create_machine_catalog_items(db_filename: str):
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


def _insert_upper_level_items_to_catalog(item_name: str, db_filename: str) -> int | None:
    """ Вставляем синтетическую запись 'Справочник' для самого верхнего уровня каталога.
        Эта запись ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        # ID_tblMachinesCatalog, period, code, description, raw_parent, ID_parent, ID_tblMachinesCatalog_tblMachineItems
        id_catalog_items = db.get_id(sql_tools_machines["select_name_item_machines"], item_name)
        if id_catalog_items:
            code = '0'
            data = (1, code, 'Справочник расценок', code, 1, id_catalog_items)
            message = f"вставка 'Справочник' {code} в каталог 'Машин'"
            inserted_id = db.try_insert(sql_tools_machines["insert_machines_catalog"], data, message)
            # ссылка родителя самого на себя
            up_data = (item_name, inserted_id, inserted_id)
            message = f"UPDATE код родителя 'Справочник' {code!r} в каталоге 'Машин'"
            inserted_id = db.try_insert(sql_tools_machines["update_machines_catalog_id_parent"], up_data, message)
            log = f"добавлена запись: {item_name.capitalize()!r} id: {inserted_id}"
            ic(log)
            return inserted_id
        return None

def _transfer_raw_items_to_machines(item_name: str, raw_db_filename: str, operating_db_filename: str):
    """ Записывает item_name в каталог из сырой базы в рабочую и создает ссылки на родителя """
    with dbControl(raw_db_filename) as raw_db, dbControl(operating_db_filename) as operating_db:
        # ищем в сырой БД объекты типа item_name
        result = raw_db.run_execute(
            sql_creates_machines["select_raw_machines_catalog_code_re"],
            (machine_items[item_name].pattern,))
        if result:
            rows = result.fetchall()
            success = []
            for row in rows:
                code = clear_code(row["PRESSMARK"])
                description = title_extraction(row["TITLE"], item_name)
                ic(code, description)


def create_machine_catalog(raw_db: str, operating_db: str):
    """ Заполняет каталог 'Машин' данными из сырой базы. """
    ic()
    items = []
    with dbControl(operating_db) as db:
        item_main = machine_items['directory'].name
        result = db.run_execute(sql_tools_machines["select_items_machines_catalog"], (item_main,))
        if result is None:
            _insert_upper_level_items_to_catalog(item_main, operating_db)

        result = db.run_execute(sql_tools_machines["select_all_machine_items"])
        if result:
            rows = result.fetchall()
            items = [x for x in rows]
            items.sort(key=lambda x: x['rating'], reverse=True)
            ic([tuple(x) for x in items])
    if items:
        # проходим всех, кроме категории 'справочник'
        for item in items[1:3]:
            _transfer_raw_items_to_machines(item["eng_name"], raw_db, operating_db)
    else:
        output_message_exit("в справочнике категорий каталога Машин", "нет ни одной категории")


def write_raw_machines_to_operate_db(raw_file_db: str, operating_file_db: str):
    # delete_machine_tables(operating_file_db)
    # create_machine_tables(operating_file_db)
    # create_machine_catalog_items(operating_file_db)
    create_machine_catalog(raw_file_db, operating_file_db)


if __name__ == "__main__":
    data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    db_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output"
    db_name = r"main_test.sqlite"
    dbf = construct_abs_file_name(db_path, db_name)

    raw_db_name = r"raw_test.sqlite"
    rdbf = construct_abs_file_name(db_path, raw_db_name)

    write_raw_machines_to_operate_db(rdbf, dbf)

