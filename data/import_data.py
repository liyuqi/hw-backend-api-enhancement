import sqlite3
import csv
import pandas as pd
from pandas.io import sql
from datetime import datetime
# print(datetime.now())
bills = pd.read_csv('../data/output.csv',
usecols = ['bill/PayerAccountId'
    ,'lineItem/UsageAccountId'
    ,'lineItem/UsageStartDate'
    ,'lineItem/UsageEndDate'
    ,'lineItem/UnblendedRate'
    ,'lineItem/UsageAmount'
    ,'lineItem/UnblendedCost'
    ,'product/ProductName'])

# print(bills)
db = sqlite3.connect('test.db')
sql.to_sql(bills,name='bills',if_exists='replace',con=db) #if_exists='replace',index=False