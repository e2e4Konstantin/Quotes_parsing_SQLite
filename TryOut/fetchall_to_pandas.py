import pandas as pd
import sqlite3
cursor = sqlite3.Cursor
df = pd.DataFrame(cursor.fetchall(), columns=['one','two'])
x = df['one'].values
f0 = pd.DataFrame.from_records(cursor.fetchall(), columns=['Time','Serie1','Serie2'],index='Time')