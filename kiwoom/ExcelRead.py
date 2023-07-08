import pandas as pd

workbook = pd.read_excel("C:/pythonfiles/lims/files/interest.xlsx",index_col=None,dtype={'code':str,'종목명':str})
print(workbook.head())
