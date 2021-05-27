import sqlite3
import csv
import pandas as pd
from pandas.io import sql
from datetime import datetime
# print(datetime.now())

# bills = pd.read_csv('../data/output.csv',
# usecols = ['bill/PayerAccountId'
#     ,'lineItem/UsageAccountId'
#     ,'lineItem/UsageStartDate'
#     ,'lineItem/UsageEndDate'
#     ,'lineItem/UnblendedRate'
#     ,'lineItem/UsageAmount'
#     ,'lineItem/UnblendedCost'
#     ,'product/ProductName'])

# print(bills)
db = sqlite3.connect('test.db')
# sql.to_sql(bills,name='bills',if_exists='replace',con=db) #if_exists='replace',index=False

idx_query1 = 'CREATE INDEX idx_aid ON bills ([lineItem/UsageAccountId])'
idx_query2 = 'CREATE INDEX idx_prodName ON bills ([product/ProductName])'
db.execute(idx_query1)
db.execute(idx_query2)