from data_storage.db_settings import dbControl
from data_storage.machines.sql_machines import sql_creates_machines


def create_machine_tables(db_filename: str):
    """ Удаляет таблицы. Создает таблицы и индексы для работы с 'Машинами'. """

    with dbControl(db_filename) as db:
        db.cursor.execute(sql_creates_machines["delete_table_machines"])
        db.cursor.execute(sql_creates_machines["delete_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["delete_table_machine_items"])

        db.cursor.execute(sql_creates_machines["create_table_machine_items"])
        db.cursor.execute(sql_creates_machines["create_table_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_table_machines"])

        db.cursor.execute(sql_creates_machines["create_index_machine_items"])
        db.cursor.execute(sql_creates_machines["create_index_machines_catalog"])
        db.cursor.execute(sql_creates_machines["create_index_machines"])





def create_tables(db_filename: str):
    """ Создает таблицы, индексы и триггеры. """

    with dbControl(db_filename) as db:
        # # для хранения Разделов
        # cursor.execute(sql_creates["create_table_subsections"])
        # cursor.execute(sql_creates["create_index_subsections"])
        # # для хранения истории Разделов
        # cursor.execute(sql_creates["create_table_history_subsections"])
        # cursor.execute(sql_creates["create_index_subsections_history"])
        # cursor.execute(sql_creates["create_trigger_history_subsections"])
        #
        # # для хранения Таблиц расценок
        # cursor.execute(sql_creates["create_table_tables"])
        # cursor.execute(sql_creates["create_index_tables"])
        # # для хранения истории Таблиц расценок
        # cursor.execute(sql_creates["create_table_history_tables"])
        # cursor.execute(sql_creates["create_index_tables_history"])
        # cursor.execute(sql_creates["create_trigger_history_tables"])

        # для хранения Справочника элементов каталога
        db.cursor.execute(sql_creates["create_table_catalog_items"])
        db.cursor.execute(sql_creates["create_index_name_catalog_items"])

        # для хранения Каталога
        db.cursor.execute(sql_creates["create_table_catalogs"])
        db.cursor.execute(sql_creates["create_index_code_catalog"])
        # для хранения истории Каталога
        db.cursor.execute(sql_creates["create_table_history_catalog"])
        db.cursor.execute(sql_creates["create_index_catalog_history"])
        db.cursor.execute(sql_creates["create_trigger_history_catalog"])
        db.cursor.execute(sql_creates["create_trigger_update_catalog"])
        # представления каталога
        db.cursor.execute(sql_views["create_view_main_catalog"])




        # для хранения Расценок
        db.cursor.execute(sql_creates["create_table_quotes"])
        db.cursor.execute(sql_creates["create_index_quotes"])
        # для хранения истории Расценок
        db.cursor.execute(sql_creates["create_table_history_quotes"])
        db.cursor.execute(sql_creates["create_index_quotes_history"])
        db.cursor.execute(sql_creates["create_trigger_history_quotes"])



