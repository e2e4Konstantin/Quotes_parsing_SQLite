from icecream import ic

from data_storage.db_settings import dbControl
from data_storage.machines.sql_machines import sql_tools_machines, sql_update_machines
from data_storage.sql_creates import sql_creates


def update_machines_statistics_from_raw_db(operating_db_file: str, raw_db_file: str):
    """ Обновляет статистику для каждой машины из raw таблицы статистики """
    with dbControl(raw_db_file) as raw_db, dbControl(operating_db_file) as operate_db:
        result = operate_db.connection.execute(sql_tools_machines["select_machines_all"])
        if result:
            machines = result.fetchall()
            success = []
            for machine in machines:
                # ic(tuple(quote))
                code = machine['code']
                period = machine['period']
                result = raw_db.connection.execute(sql_creates["select_raw_statistics_code"], (period, code))
                if result:
                    raw_statistics = result.fetchall()
                    if raw_statistics:
                        statistics_data = raw_statistics[0]
                        # ic(tuple(statistics_data))
                        stat_value = int(statistics_data['POSITION'])
                        update = operate_db.connection.execute(
                            sql_update_machines["update_machine_statistics_by_id"],
                            (stat_value, machine['ID_tblMachine'])
                        )
                        success.append(tuple(statistics_data))
                    else:
                        message = f"в raw db не найдена статистика для {code} {period}"
                        ic(message)
            log = f"обновили статистику у {len(success)} расценок."
            ic(log)

        raw_2 = raw_db.connection.execute("""SELECT * FROM tblRawStatistics WHERE PRESSMARK REGEXP "^2\.\d+";""")
        raw_stat_chapter_2 = raw_2.fetchall()
        raw_list = [x['PRESSMARK'] for x in raw_stat_chapter_2]
        r_all = len(raw_list)
        print(f"2 глава, статистика, исходных записей: {r_all}, дублей: {r_all - len(set(raw_list))}")
