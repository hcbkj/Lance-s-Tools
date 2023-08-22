import pandas as pd

excel_path = r"D:\工作相关\需求\公司内部需求\根据立案表从nas下载数据\1687138806783全国保全网_诉讼保全(1).xlsx"
df = pd.read_excel(excel_path, index_col=None, dtype=str)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

print(df)
