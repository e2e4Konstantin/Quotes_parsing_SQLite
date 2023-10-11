import re
from dataclasses import dataclass

items_eng = ['chapter', 'collection', 'section', 'subsection', 'table', 'quote']

item_patterns: dict[str:str] = {
    'chapter': r"^\s*(\d+)\s*$",
    'collection': r"^\s*((\d+)\.(\d+))\s*$",
    'section': r"^\s*((\d+)\.(\d+)-(\d+))\s*$",
    'subsection': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
    'table': r"^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$",
    'quote': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
}

compiled_item_patterns = {
    'chapter': re.compile(item_patterns['chapter']),
    'collection': re.compile(item_patterns['collection']),
    'section': re.compile(item_patterns['section']),
    'subsection': re.compile(item_patterns['subsection']),
    'table': re.compile(item_patterns['table']),
    'quote': re.compile(item_patterns['quote']),

    'subsection_groups': re.compile(r"(^\d+\.\d+-\d+-)(\d+)\s*"),
    'wildcard': re.compile(r"[\t\n\r\f\v\s+]+"),
}

@dataclass
class ItemCatalog:
    rating: int
    name: str
    pattern: str
    compiled: re.Pattern


items_data = {
    'chapter': ItemCatalog(1, 'глава', item_patterns['chapter'], compiled_item_patterns['chapter']),
    'collection': r"^\s*((\d+)\.(\d+))\s*$",
    'section': r"^\s*((\d+)\.(\d+)-(\d+))\s*$",
    'subsection': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
    'table': r"^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$",
    'quote': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
}



items_rus = ['глава', 'сборник', 'отдел', 'раздел', 'таблица', 'расценка']
items_eng = ['chapter', 'collection', 'section', 'subsection', 'table', 'quote']

title_prefix: dict[str:re.Pattern] = {
    'table': re.compile(r"^\s*Таблица\s*((\d+)\.(\d+)-(\d+)\.)*"),  # Таблица 3.1-4.
    'subsection': re.compile(r"^\s*Раздел\s*((\d+)\.)*"),  # Раздел 7.
}


def remove_wildcard(source: str = None) -> str | None:
    """ Удаляет из строки спецсимволы """
    return re.sub(compiled_item_patterns['wildcard'], r" ", source.strip()) if source else None


def extract_code(source: str, item_name: str) -> str:
    """ Выделяет из входной строки шифр объекта в соответствии с названием объекта"""
    bid_quote = compiled_item_patterns[item_name].match(source)
    return bid_quote.group(0) if bid_quote else ""


def title_extraction(title: str, item_name: str) -> str | None:
    """ Удаляет из заголовка префикс, в первом слове делает первую букву заглавной, удаляет лишние пробелы. """
    if title:
        clean_title = title_prefix[item_name].sub('', title).strip()
        by_word = clean_title.split(" ")
        by_word[0] = by_word[0].strip().capitalize()
        return " ".join(by_word)
    return None


# def get_quote_code(code: str = None) -> tuple | None:
#     """ Выделяет из шифра расценки числа и возвращает кортеж.
#         '4.1-2-10' -> (4, 1, 2, 10)"""
#     if code:
#         return re.match(item_patterns['quote'], code) is not None
#     return None

def code_split(src_code: str) -> tuple:
    """ Разбивает шифр на части.
     '4.1-2-10' -> (4, 1, 2, 10)"""
    return tuple(re.split('[.-]', src_code)) if src_code else tuple()


def identify_item_type(src_code: str) -> str | None:
    test = ['5', '5.1', '5.1-1', '5.1-1-1', '5.1-1-1-0-1', '5.1-1-1-0-2']
    return None
