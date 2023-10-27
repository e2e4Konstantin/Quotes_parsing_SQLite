import re
from dataclasses import dataclass

#
# _items_eng =    ['chapter', 'subsection', 'group', 'machine']
# _items_parent = [ 1,         2,            3,       4]
# _items_rus =    ['глава',   'раздел',    'группа',  'машина']

_machine_code_patterns: dict[str:str] = {
    'directory': r"^\s*0000\s*$",
    'chapter': r"^\s*(\d+)\s*$",
    'subsection': r"^\s*((\d+)\.(\d+))\s*$",
    'group': r"^\s*((\d+)\.(\d+)-(\d+))\s*$",
    'machine': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
}

_compiled_machine_code_patterns = {
    'directory': re.compile(_machine_code_patterns['directory']),
    'chapter': re.compile(_machine_code_patterns['chapter']),
    'subsection': re.compile(_machine_code_patterns['subsection']),
    'group': re.compile(_machine_code_patterns['group']),
    'machine': re.compile(_machine_code_patterns['machine']),

    'subsection_groups': re.compile(r"(^\d+\.\d+-\d+-)(\d+)\s*"),
    'wildcard': re.compile(r"[\t\n\r\f\v\s+]+"),
    'code_valid_chars': re.compile(r"[^\d+.-]+"),

    'subsection_prefix': re.compile(r"^\s*Раздел\s*((\d+)\.)*"),    # Раздел 3.
    'chapter_prefix': re.compile(r"^\s*Глава\s*((\d+)\.)*"),        # Глава 2.
}


@dataclass
class ItemCatalog:
    name: str
    parent_item: str
    rating: int
    pattern: str | None
    compiled: re.Pattern | None
    prefix: re.Pattern | None


machine_items: dict[str: ItemCatalog] = {
    'directory': ItemCatalog(
        name='справочник', parent_item='справочник', rating=100, pattern=_machine_code_patterns['directory'],
        compiled=_compiled_machine_code_patterns['directory'], prefix=None
        ),
    'chapter': ItemCatalog(
        'глава', 'справочник', 90, _machine_code_patterns['chapter'], _compiled_machine_code_patterns['chapter'],
        _compiled_machine_code_patterns['chapter_prefix']
        ),
    'subsection': ItemCatalog(
        'раздел', 'глава', 80, _machine_code_patterns['subsection'], _compiled_machine_code_patterns['subsection'],
        _compiled_machine_code_patterns['subsection_prefix']
        ),

    'group': ItemCatalog(
        'группа', 'раздел', 70, _machine_code_patterns['group'], _compiled_machine_code_patterns['group'], None
        ),

    'machine': ItemCatalog(
        'машина', 'группа', 60, _machine_code_patterns['machine'], _compiled_machine_code_patterns['machine'], None
        ),

}


def remove_wildcard(source: str = None) -> str | None:
    """ Удаляет из строки спецсимволы, одиночные пробелы оставляет """
    return re.sub(_compiled_machine_code_patterns['wildcard'], r" ", source.strip()) if source else None


def clear_code(source: str = None) -> str | None:
    """ Удаляет из строки все символы кроме (чисел . -) """
    return re.sub(_compiled_machine_code_patterns['code_valid_chars'], r"", source)

#
# def extract_code(source: str, item_name: str) -> str:
#     """ Выделяет из входной строки шифр объекта в соответствии с названием объекта"""
#     bid_quote = items_data[item_name].compiled.match(source)
#     return bid_quote.group(0) if bid_quote else ""
#
#
# def title_extraction(title: str, item_name: str) -> str | None:
#     """ Удаляет из заголовка префикс, в первом слове делает первую букву заглавной,
#         удаляет лишние пробелы. """
#     title = remove_wildcard(title)
#     if title:
#         clean_title = items_data[item_name].prefix.sub('', title).strip()
#         by_word = clean_title.split(" ")
#         by_word[0] = by_word[0].strip().capitalize()
#         return " ".join(by_word)
#     return None
#
#
# def split_code(src_code: str) -> tuple:
#     """ Разбивает шифр на части. '4.1-2-10' -> ('4', '1', '2', '10')"""
#     return tuple(re.split('[.-]', src_code)) if src_code else tuple()
#
#
# def split_code_int(src_code: str):
#     """ Разбивает шифр на части из чисел. '4.1-2-10' -> (4, 1, 2, 10)"""
#     return tuple(map(int, re.split('[.-]', src_code))) if src_code else tuple()
#
#
# def identify_item(src_code: str) -> tuple:
#     # ['5',       '5.1',          '5.1-1',    '5.1-1-1',      '5.1-1-1-0-1',  '5.1-1-1']
#     # ['chapter', 'collection',   'section',  'subsection',   'table',        'quote']
#     code = remove_wildcard(src_code)
#     if code:
#         length = len(split_code(code))
#         match length:
#             case 6:  # таблица
#                 extract = ('table',)
#             case 4:  # раздел, расценка
#                 extract = ('subsection', 'quote')
#             case 3:  # отдел
#                 extract = ('section',)
#             case 2:  # сборник
#                 extract = ('collection',)
#             case 1:  # глава
#                 extract = ('chapter',)
#             case _:  # непонятно
#                 extract = tuple()
#         return extract
#     return tuple()
#
#
# def check_code_item(src_code: str, item_name) -> bool:
#     """ Проверяет, соответствует ли код указаному типц"""
#     check_types = identify_item(src_code)
#     if len(check_types) > 0 and check_types[0] == item_name:
#         return True
#     return False


if __name__ == "__main__":
    print(machine_items)