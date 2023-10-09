from pandas import DataFrame


def info_data_frame(df: DataFrame, mode: str = 'short'):
    print(df.info(verbose=False, show_counts=True, memory_usage='deep'))
    print(f"использовано памяти: {df.memory_usage(index=True, deep=True).sum():_} bytes")
    print(f"размерность: {df.shape}")
    print(f"индексы: {df.index}")
    if mode != 'short':
        print(f"названия столбцов: {list(df.columns)}")
        print(f"типы данных столбцов: '{df.dtypes.values.tolist()}'")
        print(f"{df.head(5)}")
    print(f"<<{'-' * 20} info df {'-' * 20}>>")
