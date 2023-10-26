from data_extraction import read_data_frame
from data_storage.db_settings import dbControl
from data_storage.sql_creates import sql_creates
from config import DataFile


def write_raw_catalog_file_to_db(db_name: str, data_file: DataFile):
    """ Читает данные 'Каталога' из файла в DF. Добавляет столбец 'PERIOD'. Записывает DF в базу данных. """
    # 'PARENT_PRESSMARK', 'PRESSMARK', 'TITLE'
    catalog_data = read_data_frame(excel_file_name=data_file.name,
                                   sheet_name='Export Worksheet', use_columns=[0, 1, 2])
    catalog_data['PERIOD'] = data_file.period
    with dbControl(db_name) as db:
        catalog_data.to_sql(name=sql_creates["table_name_raw_catalog"], con=db.connection, if_exists='append',
                            index=False)
    del catalog_data


def write_raw_quotes_file_to_db(db_name: str, data_file: DataFile):
    """ Читает данные 'Расценки' из файла в DF. Добавляет столбец 'PERIOD'. Записывает DF в базу данных. """
    # 'GROUP_WORK_PROCESS'	'PRESSMARK'	'TITLE'	'UNIT_OF_MEASURE'
    quotes_data = read_data_frame(excel_file_name=data_file.name,
                                  sheet_name='Export Worksheet', use_columns=[0, 1, 2, 3])
    quotes_data['PERIOD'] = data_file.period
    with dbControl(db_name) as db:
        quotes_data.to_sql(name=sql_creates["table_name_raw_quotes"], con=db.connection, if_exists='append',
                           index=False)
    del quotes_data



def read_raw_statistics_data_to_db(db_name: str, statistics_file: DataFile):
    """ Читает статистику по расценкам из файла в DF. DF записывает в raw базу данных. """
    # читаем статистику в DataFrame
    statistics_data = read_data_frame(excel_file_name=statistics_file.name, sheet_name='statistics', use_columns=[0, 1])
    statistics_data['PERIOD'] = statistics_file.period
    with dbControl(db_name) as db:
        # создаем новую таблицу и записываем туда данные статистики
        statistics_data.to_sql(name=sql_creates["table_name_raw_statistics"], con=db.connection, if_exists='append',
                               index=False)
    del statistics_data
