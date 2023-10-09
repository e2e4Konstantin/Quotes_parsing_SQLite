import re

item_patterns: dict[str:str] = {
    'chapter': r"^\s*(\d+)\s*$",
    'collection': r"^\s*((\d+)\.(\d+))\s*$",
    'section': r"^\s*((\d+)\.(\d+)-(\d+))\s*$",
    'subsection': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
    'table': r"^\s*((\d+)\.(\d+)(-(\d+)){4})\s*$",

    'quote': r"^\s*((\d+)\.(\d+)(-(\d+)){2})\s*$",
}

title_prefix: dict[str:re.Pattern] = {
    'table': re.compile(r"^\s*Таблица\s((\d+)\.(\d+)-(\d+)\.)*"),
}

compiled_item_patterns = {
    'table': re.compile(item_patterns['table']),
    'quote': re.compile(item_patterns['quote']),

    'wildcard': re.compile(r"[\t\n\r\f\v\s+]+"),

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



def get_quote_code(code: str = None) -> tuple | None:
    """ Выделяет из шифра расценки числа и возвращает кортеж.
        '4.1-2-10' -> (4, 1, 2, 10)"""
    if code:
        return re.match(item_patterns['quote'], code) is not None
    return None
