import sqlite3
import re

from file_features import output_message_exit, output_message


class dbControl:
    """ Для управления соединением БД. """

    def __init__(self, db_file_name: str = None):
        self.path = db_file_name
        self.connection = None
        self.cursor = None
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close(exception_value)

    def __str__(self):
        return f"db name: {self.path}, connect: {self.connection}, cursor: {self.cursor}"

    def __del__(self):
        self.connection.close() if self.connection is not None else self.connection

    @staticmethod
    def regex(expression, item):
        reg = re.compile(expression)
        return reg.search(item) is not None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()

            self.connection.create_function("REGEXP", 2, self.regex)
        except sqlite3.Error as err:
            self.close(err)
            output_message_exit(f"ошибка открытия БД Sqlite3: {err}", f"{self.path}")

    def close(self, exception_value=None):
        if self.connection is not None:
            self.cursor.close() if self.cursor is not None else self.cursor
            if isinstance(exception_value, Exception):
                self.connection.rollback()
            else:
                self.connection.commit()
            self.connection.close()

    def get_id(self, query: str, *args) -> int | None:
        """ Выбрать id записи по запросу """
        try:
            result = self.cursor.execute(query, args)
            if result:
                row = self.cursor.fetchone()
                return row[0] if row else None
        except sqlite3.Error as error:
            output_message(f"ошибка. поиск в БД Sqlite3: {' '.join(error.args)}",
                           f"получить id записи {args}")
        return None

    def try_insert(self, query: str, src_data: tuple, message: str) -> int | None:
        """ Пытается выполнить запрос на вставку записи в БД. Возвращает rowid """
        try:
            result = self.cursor.execute(query, src_data)
            if result:
                return result.lastrowid
        except sqlite3.Error as error:
            output_message(f"ошибка INSERT запроса БД Sqlite3: {' '.join(error.args)}", f"{message}")
        return None

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

    def inform(self, all_details: bool = False):
        """  Выводи в консоль информацию о таблицах БД
        :param all_details: выводить все записи
        """
        if self.connection:
            with self.connection as db:
                self.cursor.execute('SELECT SQLITE_VERSION()')
                print(f"SQLite version: {self.cursor.fetchone()[0]}")
                print(f"connect.total_changes: {db.total_changes}")

                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = self.cursor.fetchall()
                for index, table_i in enumerate(tables):
                    table_name = table_i[0]
                    count = self.cursor.execute(f"SELECT COUNT(1) from {table_name}")
                    print(f"\n{index + 1}. таблица: {table_name}, записей: {count.fetchone()[0]}")
                    table_info = self.cursor.execute(f"PRAGMA table_info({table_name})")
                    data = table_info.fetchall()

                    print(f"поля таблицы: ")
                    print([tuple(d) for d in data])
                    if all_details:
                        print(f"данные таблицы:")
                        self.cursor.execute(f"SELECT * from {table_name}")
                        print([row_i for row_i in self.cursor])
