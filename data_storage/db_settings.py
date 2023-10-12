import sqlite3
import re

from file_features import output_message_exit


def regex(expression, item):
    reg = re.compile(expression)
    return reg.search(item) is not None


# def regex_pattern(pattern: re.Pattern, item):
#     return pattern.search(item) is not None


class dbControl:
    """ Для управления ресурсами БД. """

    def __init__(self, db_file_name: str = None):
        self.__db_path = db_file_name
        self.__db_connection = None
        self.cursor = None
        self.connect_db()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exception_type, exception_value, traceback):
        self.close_db(exception_value)

    def __str__(self):
        return f"db name: {self.__db_path}, connect: {self.__db_connection}, cursor: {self.cursor}"

    def __del__(self):
        self.__db_connection.close() if self.__db_connection is not None else self.__db_connection

    def connect_db(self):
        try:
            self.__db_connection = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.__db_connection.cursor()
            self.__db_connection.row_factory = sqlite3.Row
            self.__db_connection.create_function("REGEXP", 2, regex)
        except sqlite3.Error as err:
            self.close_db(err)
            output_message_exit(f"ошибка открытия БД Sqlite3: {err}", f"{self.__db_path}")


    def close_db(self, exception_value=None):
        if self.__db_connection is not None:
            self.cursor.close() if self.cursor is not None else self.cursor
            if isinstance(exception_value, Exception):
                self.__db_connection.rollback()
            else:
                self.__db_connection.commit()
            self.__db_connection.close()

    def run_execute(self, *args, **kwargs):
        try:
            self.cursor.execute(*args, **kwargs)
        except sqlite3.Error as error:
            print(f"SQLite error: {' '.join(error.args)}")
            # print(f"Exception class is: {error.__class__}")
            # print('SQLite traceback: ')
            # exc_type, exc_value, exc_tb = sys.exc_info()
            # print(traceback.format_exception(exc_type, exc_value, exc_tb))
            # print(error)

    def inform_db(self, all_details: bool = False):
        """  Выводи в консоль информацию о таблицах БД
        :param all_details: выводить все записи
        """
        with self.__db_connection as db:
            self.cursor.execute('SELECT SQLITE_VERSION()')
            print(f"SQLite version: {self.cursor.fetchone()[0]}")
            print(f"connect.total_changes: {db.total_changes}")
            # print(self.cursor.connection)

            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            for index, table_i in enumerate(tables):
                table_name = table_i[0]
                count = self.cursor.execute(f"SELECT COUNT(1) from {table_name}")
                print(f"\n{index + 1}. таблица: {table_name}, записей: {count.fetchone()[0]}")
                table_info = self.cursor.execute(f"PRAGMA table_info({table_name})")
                data = table_info.fetchall()

                print(f"поля таблицы: ")
                print([d for d in data])
                if all_details:
                    print(f"данные таблицы:")
                    self.cursor.execute(f"SELECT * from {table_name}")
                    print([row_i for row_i in self.cursor])
