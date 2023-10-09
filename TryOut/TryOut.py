import os
import pandas as pd

path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\development\Quotes_parsing_SQLite"
file_name = r"src\catalog_3_68.xlsx"
file_name = os.path.join(path, file_name)
sheet_name = "catalog"


df = pd.read_excel(io=file_name, sheet_name=sheet_name, usecols=list(range(3)), dtype=pd.StringDtype())
df.info()
