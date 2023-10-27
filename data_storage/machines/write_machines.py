from config import SrcMachinesData
from file_features import construct_abs_file_name, output_message_exit
from data_storage.db_settings import dbControl

from data_storage.machines.sql_machines import sql_creates_machines
from data_storage.machines.machine_items import machine_items


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
            db.run_execute(sql_creates_machines["update_parent_references"])
        else:
            output_message_exit("неудача, справочник элементов каталога для 'Машин'", "не заполнился")


def write_raw_machines_to_operate_db(raw_file_db: str, operating_file_db: str):
    delete_machine_tables(operating_file_db)
    create_machine_tables(operating_file_db)
    create_machine_catalog_items(operating_file_db)


if __name__ == "__main__":
    data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    db_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite\output"
    db_name = r"main_test.sqlite"
    dbf = construct_abs_file_name(db_path, db_name)
    write_raw_machines_to_operate_db("", dbf)
