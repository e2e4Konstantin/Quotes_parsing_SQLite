#
#
# CREATE TABLE test
# (
#     id INTEGER NOT NULL PRIMARY KEY,
#     prefix TEXT NOT NULL,
#     CHECK(prefix NOT LIKE '%[^a-zA-Z]%')
# )
#
#
# def regex(expr, item):
#     reg = re.compile(expr)
#     return reg.search(item) is not None
#
#
# conn = sqlite3.connect(':MEMORY:')
# conn.create_function("REGEXP", 2, regex)
#
# CHECK (prefix REGEXP '^[a-zA-Z]+$')
#
# CHECK(prefix NOT GLOB '*[^a-zA-Z]*'))
#
# CHECK(length(prefix) > 0 AND prefix NOT GLOB '*[^a-zA-Z]*'))