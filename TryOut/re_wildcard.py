import re

from data_storage.re_patterns import compiled_item_patterns, extract_code, remove_wildcard

s = "генератор синхронный\t(компенсатор)           напряжением  свыше\n 1кВ, мощностью до 2,5 мВт (МВАр)  "
# s2 = "Генератор синхронный (компенсатор) напряжением до 1 кВ, мощностью до 100 кВт"
# s3 = "Генератор синхронный (компенсатор) напряжением свыше 1кВ, мощностью до 2,5 мВт (МВАр)"
#
# # r = re.sub('([.-])\1+', '\1', s)
#
#
# p = re.compile(r"[\t\n\r\f\v\s+]+")
# r = re.sub(p, r' ', s)
#
# first_word = re.compile(r"^\w+")
# fw = first_word.match(s)
# print(fw.group(0))
# print(first_word.sub(first_word.match(s).group(0).capitalize(), s))
#
#
# (firstWord, rest) = s.split(maxsplit=1)
# print(firstWord.capitalize(), rest)
#
#
# print(f"{s!r}")
# print(f"{r!r}")
# print(f"{remove_wildcard(s)!r}")

s = remove_wildcard(s)

(first_word, rest) = s.split(maxsplit=1)
s = " ".join([first_word.capitalize(), rest])
print(s)
