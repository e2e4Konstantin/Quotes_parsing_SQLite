from icecream import ic

from config import DataFile, SrcMachinesData
from file_features import file_extract_period_path
from data_extraction import read_data_frame
from data_storage.db_settings import dbControl
from data_storage.machines.sql_machines import sql_creates_machines


def read_raw_machines_structure(raw_file_db: str, structure_data_file: DataFile):
    """ Читает данные о структуре 'Машин' из файла. Добавляет столбец 'PERIOD'. Записывает в 'сырую' БД.  """
    structure_df = read_data_frame(excel_file_name=structure_data_file.name,
                                   sheet_name='Export Worksheet', use_columns=[0, 1, 2])
    structure_df['PERIOD'] = structure_data_file.period
    with dbControl(raw_file_db) as db:
        structure_df.to_sql(name=sql_creates_machines["table_name_raw_machines_catalog"],
                            con=db.connection, if_exists='append', index=False)
    del structure_df


def read_raw_machines_data(raw_file_db: str, machines_data_file: DataFile):
    """ Читает данные о 'Машинах' из файла. Добавляет столбец 'PERIOD'. Записывает в 'сырую' БД.  """
    machines_df = read_data_frame(excel_file_name=machines_data_file.name,
                                  sheet_name='Sheet', use_columns=[0, 1, 2, 3, 4, 5, 6, 7])
    machines_df['PERIOD'] = machines_data_file.period
    with dbControl(raw_file_db) as db:
        machines_df.to_sql(name=sql_creates_machines["table_name_raw_machines"],
                           con=db.connection, if_exists='append', index=False)
    del machines_df


def read_machines(raw_file_db: str, data: SrcMachinesData):
    """ Читает данные о машинах из файлов. Добавляет столбец 'PERIOD'. Записывает в 'сырую' БД.  """
    # выделить период из имени файла
    structure_data_file: DataFile = file_extract_period_path(data.path, data.structure)
    ic(structure_data_file)
    read_raw_machines_structure(raw_file_db, structure_data_file)

    machine_data_file: DataFile = file_extract_period_path(data.path, data.machines)
    ic(machine_data_file)
    read_raw_machines_data(raw_file_db, machine_data_file)

    with dbControl(raw_file_db) as db:
        db.inform()


# def write_raw_machines_to_operate_db(raw_file_db: str, operating_file_db: str):
#     # в рабочей базе создать таблицы и индексы для 'Машин' если они есть удалить их
#     create_machine_tables(operating_file_db)


if __name__ == "__main__":
    data_path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\АИС"
    machines_data = SrcMachinesData(data_path, "STRUCTURE_MACHINES_2_68.xlsx", "MACHINES_2_68.xlsx")
    read_machines(raw_file_db=r'../../output/raw_test.sqlite', data=machines_data)
