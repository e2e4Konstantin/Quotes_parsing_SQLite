from pandas import DataFrame


def target_count(target: str, column_name: str, df: DataFrame) -> int:
    """ Считает количество значений target в столбце column_name. """
    return df[column_name].value_counts().get(target, 0)
