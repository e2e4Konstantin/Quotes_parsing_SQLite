
from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates


def create_tables(db_filename: str):
    """ Создает таблицы, индексы и триггеры. """

    with dbControl(db_filename) as cursor:
        # для хранения Разделов
        cursor.execute(sql_creates["create_table_subsections"])
        cursor.execute(sql_creates["create_index_subsections"])
        # для хранения истории Разделов
        cursor.execute(sql_creates["create_table_history_subsections"])
        cursor.execute(sql_creates["create_index_subsections_history"])
        cursor.execute(sql_creates["create_trigger_history_subsections"])

        # для хранения Таблиц расценок
        cursor.execute(sql_creates["create_table_tables"])
        cursor.execute(sql_creates["create_index_tables"])
        # для хранения истории Таблиц расценок
        cursor.execute(sql_creates["create_table_history_tables"])
        cursor.execute(sql_creates["create_index_tables_history"])
        cursor.execute(sql_creates["create_trigger_history_tables"])

        # для хранения Расценок
        cursor.execute(sql_creates["create_table_quotes"])
        cursor.execute(sql_creates["create_index_quotes"])
        # для хранения истории Расценок
        cursor.execute(sql_creates["create_table_history_quotes"])
        cursor.execute(sql_creates["create_index_quotes_history"])
        cursor.execute(sql_creates["create_trigger_history_quotes"])



