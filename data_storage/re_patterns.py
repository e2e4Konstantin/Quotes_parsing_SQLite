import re
from dataclasses import dataclass

#
# _items_eng =    ['chapter', 'collection', 'section', 'subsection', 'table',   'quote']
# _items_parent = [ 1,         2,            3,         4,            5,         6]
# _items_rus =    ['глава',   'сборник',    'отдел',   'раздел',     'таблица', 'расценка']

_item_patterns: dict[str:str] = {
    'directory': r"^\s*0000\s*$",
    'chapter': r"^\s*(\d+)\s*$",
    'collection': r"^\s*((\d+)\.(\d+))\s*$",
    'section': r"^\s*((\d+)\.(\d+)-(\d+))\s*$",
    'subsection': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
    'table': r"^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$",
    'quote': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
}

_compiled_item_patterns = {
    'directory': re.compile(_item_patterns['directory']),
    'chapter': re.compile(_item_patterns['chapter']),
    'collection': re.compile(_item_patterns['collection']),
    'section': re.compile(_item_patterns['section']),
    'subsection': re.compile(_item_patterns['subsection']),
    'table': re.compile(_item_patterns['table']),
    'quote': re.compile(_item_patterns['quote']),

    'subsection_groups': re.compile(r"(^\d+\.\d+-\d+-)(\d+)\s*"),
    'wildcard': re.compile(r"[\t\n\r\f\v\s+]+"),
    'code_valid_chars': re.compile(r"[^\d+.-]+"),

    'table_prefix': re.compile(r"^\s*Таблица\s*((\d+)\.(\d+)-(\d+)\.)*"),  # Таблица 3.1-4.
    'subsection_prefix': re.compile(r"^\s*Раздел\s*((\d+)\.)*"),  # Раздел 7.
    'section_prefix': re.compile(r"^\s*Отдел\s*((\d+)\.)*"),  # Отдел 7.
    'collection_prefix': re.compile(r"^\s*Сборник\s*((\d+)\.)*"),  # Сборник 7.
    'chapter_prefix': re.compile(r"^\s*Глава\s*((\d+)\.)*"),  # Глава 7.
}


@dataclass
class ItemCatalog:
    rank: int
    parent: int
    name: str
    pattern: str | None
    compiled: re.Pattern | None
    prefix: re.Pattern | None


items_data: dict[str: ItemCatalog] = {
    'directory': ItemCatalog(
        100, 1, 'справочник', _item_patterns['directory'], _compiled_item_patterns['directory'], None
    ),
    'chapter': ItemCatalog(
        90, 1, 'глава', _item_patterns['chapter'], _compiled_item_patterns['chapter'],
        _compiled_item_patterns['chapter_prefix']
    ),
    'collection': ItemCatalog(
        80, 2, 'сборник', _item_patterns['collection'], _compiled_item_patterns['collection'],
        _compiled_item_patterns['collection_prefix']
    ),
    'section': ItemCatalog(
        70, 3, 'отдел', _item_patterns['section'], _compiled_item_patterns['section'],
        _compiled_item_patterns['section_prefix']
    ),
    'subsection': ItemCatalog(
        60, 4, 'раздел', _item_patterns['subsection'], _compiled_item_patterns['subsection'],
        _compiled_item_patterns['subsection_prefix']
    ),
    'table': ItemCatalog(
        50, 5, 'таблица', _item_patterns['table'], _compiled_item_patterns['table'],
        _compiled_item_patterns['table_prefix']
    ),
    'quote': ItemCatalog(
        40, 6, 'расценка', _item_patterns['quote'], _compiled_item_patterns['quote'], None
    ),
}


def remove_wildcard(source: str = None) -> str | None:
    """ Удаляет из строки спецсимволы, одиночные пробелы оставляет """
    return re.sub(_compiled_item_patterns['wildcard'], r" ", source.strip()) if source else None


def clear_code(source: str = None) -> str | None:
    """ Удаляет из строки все символы кроме (чисел . -) """
    return re.sub(_compiled_item_patterns['code_valid_chars'], r"", source)


def extract_code(source: str, item_name: str) -> str:
    """ Выделяет из входной строки шифр объекта в соответствии с названием объекта"""
    bid_quote = items_data[item_name].compiled.match(source)
    return bid_quote.group(0) if bid_quote else ""


def title_extraction(title: str, item_name: str) -> str | None:
    """ Удаляет из заголовка префикс, в первом слове делает первую букву заглавной,
        удаляет лишние пробелы. """
    title = remove_wildcard(title)
    if title:
        clean_title = items_data[item_name].prefix.sub('', title).strip()
        by_word = clean_title.split(" ")
        by_word[0] = by_word[0].strip().capitalize()
        return " ".join(by_word)
    return None


def split_code(src_code: str) -> tuple:
    """ Разбивает шифр на части. '4.1-2-10' -> ('4', '1', '2', '10')"""
    return tuple(re.split('[.-]', src_code)) if src_code else tuple()


def split_code_int(src_code: str):
    """ Разбивает шифр на части из чисел. '4.1-2-10' -> (4, 1, 2, 10)"""
    return tuple(map(int, re.split('[.-]', src_code))) if src_code else tuple()


def identify_item(src_code: str) -> tuple:
    # ['5',       '5.1',          '5.1-1',    '5.1-1-1',      '5.1-1-1-0-1',  '5.1-1-1']
    # ['chapter', 'collection',   'section',  'subsection',   'table',        'quote']
    code = remove_wildcard(src_code)
    if code:
        length = len(split_code(code))
        match length:
            case 6:  # таблица
                extract = ('table',)
            case 4:  # раздел, расценка
                extract = ('subsection', 'quote')
            case 3:  # отдел
                extract = ('section',)
            case 2:  # сборник
                extract = ('collection',)
            case 1:  # глава
                extract = ('chapter',)
            case _:  # непонятно
                extract = tuple()
        return extract
    return tuple()


if __name__ == "__main__":
    s = '5  . 1-1-1-0-   1   '
    s2 = remove_wildcard(s)
    print(f"{s2!r}")
    s3 = split_code(s2)
    print(f"{s3}")

    sx = clear_code(s)
    print(sx)

    print(items_data.keys())
    print([x for x in items_data.keys()])
    print(items_data['table'].prefix)
    test = ['5', '5.1', '5.1-1', '5.1-1-1', '5.1-1-1-0-1', '5.1-1-1']
    for x in test:
        print(identify_item(x))
