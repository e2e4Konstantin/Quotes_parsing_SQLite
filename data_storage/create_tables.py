
from data_storage.db_settings import dbControl
from data_storage.sql_queries import sql_queries


def create_tables(db_filename: str):
    """ Создает таблицы, индексы и триггеры. """

    with dbControl(db_filename) as cursor:
        # для хранения таблиц расценок
        cursor.execute(sql_queries["create_table_tables"])
        cursor.execute(sql_queries["create_index_tables"])

        # для хранения истории таблиц расценок
        cursor.execute(sql_queries["create_table_history_tables"])
        cursor.execute(sql_queries["create_index_tables_history"])
        cursor.execute(sql_queries["create_trigger_history_tables"])

        # для хранения расценок
        cursor.execute(sql_queries["create_table_quotes"])
        cursor.execute(sql_queries["create_index_quotes"])

        # для хранения истории расценок
        cursor.execute(sql_queries["create_table_history_quotes"])
        cursor.execute(sql_queries["create_index_quotes_history"])
        cursor.execute(sql_queries["create_trigger_history_quotes"])



