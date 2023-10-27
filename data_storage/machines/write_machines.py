from config import SrcMachinesData
from data_storage.db_settings import dbControl

from data_storage.machines.sql_machines import sql_creates_machines


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
    """ Заполняет справочник элементов каталога для 'Машин'.
        Первый элемент ссылается сам на себя. Старшинство определяется tblMachineItems.rating
        Глава ссылается сама на себя.
    """
    with dbControl(db_filename) as db:
        items = [(items_data[item].name, item, items_data[item].parent, items_data[item].rank)
                 for item in items_data.keys()]
        db.cursor.executemany(sql_creates["insert_catalog_item"], items)






def write_raw_machines_to_operate_db(raw_file_db: str, operating_file_db: str):
    delete_machine_tables(operating_file_db)
    create_machine_tables(operating_file_db)


if __name__ == "__main__":
    data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    machines_data = SrcMachinesData(data_path, "STRUCTURE_MACHINES_2_68.xlsx", "MACHINES_2_68.xlsx")
    read_machines(raw_file_db=r'../../output/raw_test.sqlite', data=machines_data)
