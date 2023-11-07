import duckdb
from icecream import ic

url = "https://huggingface.co/datasets/blog_authorship_corpus/resolve/refs%2Fconvert%2Fparquet/blog_authorship_corpus/train/0000.parquet"

con = duckdb.connect()
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")
r = con.sql(f"SELECT horoscope, count(*), AVG(LENGTH(text)) AS avg_blog_length FROM '{url}' GROUP BY horoscope ORDER BY avg_blog_length DESC LIMIT(5)")
ic(r)

# con.sql(f"SELECT horoscope, count(*), AVG(LENGTH(text)) AS avg_blog_length FROM read_parquet({urls[:2]}) GROUP BY horoscope ORDER BY avg_blog_length DESC LIMIT(5)")