# https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook
# https://stackoverflow.com/questions/26521266/using-pandas-to-pd-read-excel-for-multiple-worksheets-of-the-same-workbook
# https://stackoverflow.com/questions/17439885/export-data-from-excel-to-sqlite-database

# https://www.youtube.com/watch?v=r0EQkjcZtqM

# https://www.ch-werner.de/sqliteodbc/

# https://learn.microsoft.com/ru-ru/sql/integration-services/import-export-data/connect-to-an-odbc-data-source-sql-server-import-and-export-wizard?view=sql-server-ver16


import pandas as pd
excel_file_name = r"C:\Users\kazak.ke\Documents\Задачи\Парсинг_параметризация\SRC\Статистика_20.xlsx"
parquet_file = r"C:\Users\kazak.ke\Documents\Задачи\Парсинг_параметризация\SRC\Статистика_20.gzip"
sheet_name = "Export Worksheet"
use_columns = [1, 2, 3, 4, 5, 10]
#
# df = pd.read_excel(io=excel_file_name, sheet_name=sheet_name, usecols=use_columns, dtype=pd.StringDtype())
# print(df.info(verbose=False, show_counts=True, memory_usage='deep'))
# print(f"использовано памяти: {df.memory_usage(index=True, deep=True).sum():_} bytes")
# print(f"размерность: {df.shape}")
# print(f"индексы: {df.index}")
# print(f"названия столбцов: {list(df.columns)}")
# print(f"типы данных столбцов: '{df.dtypes.values.tolist()}'")
# print(f"{df.head(5)}")
#

# xls = pd.ExcelFile(excel_file_name)
#
# # list all sheets in the file
# sheet_names = xls.sheet_names
# print(sheet_names)
#
# df = pd.concat([pd.read_excel(excel_file_name, sheet_name=name) for name in sheet_names], axis=0)
# df = df[df.columns].astype(pd.StringDtype())
# df.to_parquet(parquet_file, engine='fastparquet', compression='gzip')

df = pd.read_parquet(parquet_file)
print(df.info(verbose=False, show_counts=True, memory_usage='deep'))
print(f"использовано памяти: {df.memory_usage(index=True, deep=True).sum():_} bytes")
print(f"размерность: {df.shape}")
print(f"индексы: {df.index}")




#
#
# # to read all sheets to a map
# sheet_to_df_map = {}
# for sheet_name in sn:
#     sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
#     # you can also use sheet_index [0,1,2..] instead of sheet name.
#
#
#


# возникает исключение 'parquet error Can't infer object conversion type: 0'
            # надо явно преобразовывать типы с десятичной точкой или string

# df = df[df.columns].astype(pd.StringDtype())
# df.to_parquet(parquet_file, engine='fastparquet', compression='gzip')