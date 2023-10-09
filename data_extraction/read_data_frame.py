import os
import pandas as pd
from pandas import DataFrame

from file_features.message import output_message_exit


def read_data_frame(excel_file_name: str, sheet_name: str, use_columns: list[int]) -> DataFrame | None:
    """
    Читает данные из Excel файла в pandas.DataFrame().
    Строки и столбцы нумеруем с 1.
    Для отладки создает из DF файл формата parquet с расширением gzip. Если уже есть такой файл, то DF читает из него.
    :param excel_file_name: Файл с данными.
    :param sheet_name: Имя таблицы.
    :param use_columns список индексов столбцов которые надо прочитать
    :return: Экземпляр класса pandas.DataFrame()
    """

    file_path, file_name = os.path.split(excel_file_name)
    parquet_file = os.path.join(file_path, f"{file_name.split('.')[0]}_{sheet_name}.gzip")
    df = DataFrame()
    if os.path.exists(parquet_file):
        try:
            df = pd.read_parquet(parquet_file)
        except IOError as err:
            output_message_exit(str(err), parquet_file)
    else:
        try:
            df = pd.read_excel(io=excel_file_name, sheet_name=sheet_name, usecols=use_columns, dtype=pd.StringDtype())
            # возникает исключение 'parquet error Can't infer object conversion type: 0'
            # надо явно преобразовывать типы с десятичной точкой или string
            # df = df[df.columns].astype(pd.StringDtype())
            df.to_parquet(parquet_file, engine='fastparquet', compression='gzip')
        except IOError as err:
            output_message_exit(str(err), excel_file_name)
    if not df.empty:
        df = df[df.columns].astype(pd.StringDtype())
        return df
    return None
