import logging as log

# curl http://192.168.43.175:5000/api/aid/484234319610/cost
# curl http://192.168.43.175:5000/api/aid/484234319610/amount


from flask import g, Flask, request, jsonify, render_template, Response
import pandas as pd
import sqlite3
import sys
import os
import json
from datetime import datetime, timedelta
app = Flask(__name__)

DATABASE = "../data/test.db"
TABLE = ' bills '

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.test = sqlite3.connect(DATABASE)
        # db.row_factory = sqlite3.Row
        # db.row_factory = dict_factory
    return db

@app.errorhandler(400)
def bad_request(error):
    return json.dumps({'status':400,'error': 'Bad request'})

@app.errorhandler(404)
def not_found(e):
    return json.dumps({'status': 404, 'error': 'Not found'})

@app.route('/',methods=['GET'])
def home():
    return 'api demo'

@app.route('/api/aid/<aid>/unblended_cost',methods=['GET'])
def cost(aid):
    # Get lineItem/UnblendedCost grouping by product/productname
    # input : {col:'lineitem/usageaccountid'}
    # output: {
    #     "{product/productname_A}": "sum(lineitem/unblendedcost)",
    #     "{product/productname_B}": "sum(lineitem/unblendedcost)",
    #     ...
    # }
    # aid = list(filter(lambda t: t['aid']==aid))
    db = get_db()
    c = db.cursor()
    query = ' SELECT [product/ProductName], sum([lineItem/UnblendedCost]) as cost FROM '+TABLE
    query+= ' WHERE [lineItem/UsageAccountId]='+aid
    query+= ' GROUP BY [product/ProductName]'
    # print('query',query)
    datas = db.execute(query).fetchall()
    # ddf = pd.read_sql_query(query,db)
    # return ddf.to_json(orient = "records")
    cost_dict = dict()
    for data in datas:
        productName,cost=data[0],data[1]
        cost_dict[productName] = cost
    return json.dumps(cost_dict)
    

@app.route('/api/aid/<aid>/usage_amount',methods=['GET'])
def amount(aid):
    # Get daily lineItem/UsageAmount grouping by product/productname
    # input : {col:'lineitem/usageaccountid'}
    # Output: {
    #     "{product/productname_A}": {
    #         "YYYY/MM/01": "sum(lineItem/UsageAmount)",
    #         "YYYY/MM/02": "sum(lineItem/UsageAmount)",
    #         "YYYY/MM/03": "sum(lineItem/UsageAmount)",
    #         ...
    #     },
    # }
    db = get_db()
    c = db.cursor()
    query = ' SELECT [product/ProductName], [lineItem/UsageStartDate], [lineItem/UsageEndDate], [lineItem/UsageAmount] FROM ' + TABLE
    query+= ' WHERE [lineItem/UsageAccountId]='+aid
    datas = db.execute(query).fetchall()

    use_amount = dict()
    day_amount = dict()
    for data in datas:
        productName,startDate,endDate,usageAmount = data[0],data[1],data[2],data[3]
        if data[0] not in use_amount:
            use_amount[data[0]] = {}

        day_amount = use_amount[productName]
        shift_day = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%SZ') # startDate[0:10]
        end_day     = datetime.strptime(endDate, '%Y-%m-%dT%H:%M:%SZ') # endDate[0:10]
        day_str = shift_day.strftime('%Y/%m/%d')
        same_day = (startDate[0:10] == endDate[0:10])
        while (shift_day < end_day or same_day):
            if day_str in day_amount:
                day_amount[day_str] += usageAmount
            else:
                day_amount[day_str] = usageAmount
            shift_day += timedelta(days=1) 
            day_str = shift_day.strftime('%Y/%m/%d')
            same_day = False
    return json.dumps(use_amount)
    # return json.dumps(result)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
