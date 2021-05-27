# Assignment - API Enhancement

## Target
1. Import csv file into sqlite3 ```import_data.py```

```sql
.schema bills
CREATE TABLE "bills" (
  "bill/PayerAccountId" INTEGER,
  "lineItem/UsageAccountId" INTEGER,
  "lineItem/UsageStartDate" TEXT,
  "lineItem/UsageEndDate" TEXT,
  "lineItem/UsageAmount" REAL,
  "lineItem/UnblendedRate" REAL,
  "lineItem/UnblendedCost" REAL,
  "product/ProductName" TEXT
);
CREATE INDEX idx_aid ON bills ([lineItem/UsageAccountId]);
CREATE INDEX idx_prodName ON bills ([product/ProductName]);
```

2. create DB index at lineItem/UsageAccountId, product/ProductName ```index_data.py```
3. APIs
    ```sh
    cd api;
    pip install -r requirements.txt
    python app.py
    ```
    1. Get __lineItem/UnblendedCost__ grouping by __product/productname__
        - Input
          | Column | Required |
          | ------ | -------- |
          | lineitem/usageaccountid | true |
        - Output 
        ```JSON
            {
                "{product/productname_A}": "sum(lineitem/unblendedcost)",
                "{product/productname_B}": "sum(lineitem/unblendedcost)",
                ...
            }
        ```
        1. __API URLs__ /api/aid/`<aid>`/unblended_cost
        2. __API sample__   curl http://localhost:5000/api/aid/27404931260/unblended_cost


    2. Get daily __lineItem/UsageAmount__ grouping by __product/productname__
        - Input
          | Column | Required |
          | ------ | -------- |
          | lineitem/usageaccountid | true |
        - Output
        ```JSON
            {
                "{product/productname_A}": {
                    "YYYY/MM/01": "sum(lineItem/UsageAmount)",
                    "YYYY/MM/02": "sum(lineItem/UsageAmount)",
                    "YYYY/MM/03": "sum(lineItem/UsageAmount)",
                    ...
                },
                "{product/productname_B}": {
                    "YYYY/MM/01": "sum(lineItem/UsageAmount)",
                    "YYYY/MM/02": "sum(lineItem/UsageAmount)",
                    "YYYY/MM/03": "sum(lineItem/UsageAmount)",
                    ...
                },
            }
        ```
        1. __API URLs__ /api/aid/`<aid>`/usage_amount
        2. __API sample__   curl -X GET http://localhost:5000/api/aid/27404931260/usage_amount

4. I use python implement APIs.

## Deliverable
1. git repo [https://github.com/liyuqi/hw-backend-api-enhancement]
2. __README.md__ here
3. API description as above
4. Flask framwork
5. local sqlite
6. performance
    1. create index: every query filter UsageAccountId, then group by ProductName
    2. unblendedcost: first use sum() function at query, then render out
    3. UsageAmount: first filter at query, map daily amount from start to end, then render out