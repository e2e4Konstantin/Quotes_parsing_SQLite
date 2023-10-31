import re
from dataclasses import dataclass
from icecream import ic

from data_storage.re_patterns import clear_code, split_code, remove_wildcard

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


    'chapter_prefix': re.compile(r"^\s*Глава\s*((\d+)\.)*"),  # Глава 2.
    'subsection_prefix': re.compile(r"^\s*Раздел\s*((\d+)\.)*"),  # Раздел 3.
    'group_prefix': re.compile(r"^\s*((\d+)\.)*"),  # 3.

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
        prefix=_compiled_machine_code_patterns['chapter_prefix']
    ),
    'subsection': ItemCatalog(
        'раздел', 'глава', 80, _machine_code_patterns['subsection'], _compiled_machine_code_patterns['subsection'],
        _compiled_machine_code_patterns['subsection_prefix']
    ),

    'group': ItemCatalog(
        'группа', 'раздел', 70, _machine_code_patterns['group'], _compiled_machine_code_patterns['group'],
        _compiled_machine_code_patterns['group_prefix']
    ),

    'machine': ItemCatalog(
        'машина', 'группа', 60, _machine_code_patterns['machine'], _compiled_machine_code_patterns['machine'], None
    ),

}


def machines_title_extraction(title: str, item_name: str) -> str | None:
    """ Удаляет из заголовка префикс, в первом слове делает первую букву заглавной,
        удаляет лишние пробелы. """
    title = remove_wildcard(title)
    if title:
        prefix_pattern = machine_items[item_name].prefix
        if prefix_pattern:
            clean_title = prefix_pattern.sub('', title).strip()
            by_word = clean_title.split(" ")
            by_word[0] = by_word[0].strip().capitalize()
            return " ".join(by_word)
        else:
            return title
    return None



def identify_item_by_code(src_code: str) -> str:
    """ По коду определяет тип объекта. """
    # ['5',     '5.1',      '5.1-1',   '5.1-1-1']
    # ['глава', 'раздел',   'группа',  'машина']
    code = clear_code(src_code)
    if code:
        match len(split_code(code)):
            case l if l == 4 and machine_items['machine'].compiled.fullmatch(code):
                code_type = 'machine'
            case l if l == 3 and machine_items['group'].compiled.fullmatch(code):
                code_type = 'group'
            case l if l == 2 and machine_items['subsection'].compiled.fullmatch(code):
                code_type = 'subsection'
            case l if l == 1 and machine_items['chapter'].compiled.fullmatch(code):
                code_type = 'chapter'
            case _:  # непонятно
                code_type = ""
        return code_type
    return ""


def extract_parent_code(child_code: str) -> str:
    """ Выделяет из входного шифра родительский шифр.
        Если это глава, то вернет '0'.
    """
    if child_code:
        stripped_code = split_code(child_code)
        short_code = stripped_code[:-1]
        match len(short_code):
            case 0:
                return "0"
            case 1:
                return stripped_code[0]
            case code_len:
                for part in range(code_len - 1, 1, -1):
                    if int(stripped_code[part]) != 0:
                        return stripped_code[:part + 1]

    return "0"



if __name__ == "__main__":
    ic(identify_item_by_code('5'))
    ic(identify_item_by_code('5.1'))
    ic(identify_item_by_code('5.1-1'))
    ic(identify_item_by_code('5.1-1-55'))
    ic(identify_item_by_code('5.1-1-55-88'))
    ic(identify_item_by_code('5.1-1-5f5'))
    ic(identify_item_by_code('   5 .1- 1 -5  5'))

    ic(extract_parent_code('5.1-1-55-88'))
    ic(extract_parent_code('5.1-1-0-88'))
    ic(extract_parent_code('5.2'))
    ic(extract_parent_code('5.'))
    ic(extract_parent_code(''))
