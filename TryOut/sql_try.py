#
# from data_extraction import read_data_frame, info_data_frame
# from data_storage import write_catalog_to_db, write_quotes_to_db, dbControl, create_tables
#
#
# from data_storage import sql_queries, item_patterns, title_prefix, title_extraction
#
#
#
# path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
#
# # читаем данные из исходных файлов во временную БД
# raw_db_name = r"output\RawCatalog.sqlite"
# raw_db = os.path.join(path, raw_db_name)
# # get_raw_data(path, raw_db)
# #
# operating_db_name = r"output\Quotes.sqlite"
# operating_db = os.path.join(path, operating_db_name)
#
# create_tables(operating_db)
#
#
# with dbControl(raw_db) as raw_cursor, dbControl(operating_db) as cursor:
#         # raw_cursor.execute("""select PRESSMARK, TITLE from tblRawCatalog;""")
#         # for row in raw_cursor.fetchall():
#         #     print(row)
#
#         # raw_cursor.execute("""select PRESSMARK, TITLE from tblRawCatalog where PRESSMARK REGEXP "^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$";""")
#         # for row in raw_cursor.fetchall():
#         #     print(f"{row[0]} - {row[1].split('.')[2]} {row!r} ")
#
#         raw_cursor.execute("""select count(PRESSMARK) from tblRawCatalog where PRESSMARK REGEXP "^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$";""")
#         print(f"numberOfRows = {raw_cursor.fetchone()}, {type(raw_cursor.fetchone())=}")
#
#         raw_cursor.execute("""SELECT PRESSMARK, TITLE FROM tblRawCatalog WHERE PRESSMARK REGEXP ?;""", (item_patterns['table'],))
#         for row in raw_cursor.fetchall()[:4]:
#             print(row)
#
#         print(f"numberOfRows = {raw_cursor.fetchone()}, {type(raw_cursor.fetchall())=}")
#
#     # raw_cursor.execute("""SELECT * FROM tblRawCatalog WHERE PRESSMARK REGEXP ?""", (item_patterns['table'],))
#     # raw_tables = raw_cursor.fetchall()
#     # for raw_table in raw_tables:
#     #     cursor.execute(sql_queries["insert_table_to_tblTables"], (68, raw_table[1].strip(), title_extraction(raw_table[2], 'table'), 0))
#
#
# result = operating_cursor.execute("""select ID_tblTable from tblTables where code IS ?""", (table_code,))
# print(f"{result}, {result.rowcount = } {result.fetchone()}")
# print(f"{result.description}")
#
#
#
# if cursor.description is None:
#     # No recordset for INSERT, UPDATE, CREATE, etc
#     pass
# else:
#     # Recordset for SELECT
#
#
# exist = cursor.fetchone()
# if exist is None:
#   ... # does not exist
# else:
#   ... # exists
#
#
# SELECT * FROM sqlite_master WHERE type = 'table';