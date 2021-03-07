

INPUT_USER = {"name": "Jane Doe", "email": "jane@email.com", "age": 23}

INPUT_ONE_TRANSACTION = {"reference": "000001", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1}

INPUT_MANY_TRANSACTIONS_1 = [
    {"reference": "000001", "account": "C00001", "date": "2021-01-01", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1},
    {"reference": "000002", "account": "C00001", "date": "2021-01-10", "amount": "2500.72", "type": "inflow", "category": "salary", "user_id": 1},
    {"reference": "000003", "account": "C00001", "date": "2021-03-05", "amount": "-150.72", "type": "outflow", "category": "transfer", "user_id": 1},
    {"reference": "000004", "account": "C00001", "date": "2021-03-07", "amount": "1500.50", "type": "inflow", "category": "salary", "user_id": 1},
    {"reference": "000005", "account": "C00002", "date": "2021-02-12", "amount": "-560.00", "type": "outflow", "category": "rent", "user_id": 1},
    {"reference": "000006", "account": "C00002", "date": "2021-02-22", "amount": "-51.13", "type": "outflow", "category": "other", "user_id": 1},
    {"reference": "000007", "account": "C00002", "date": "2021-03-01", "amount": "3000.82", "type": "inflow", "category": "savings" ,"user_id": 1},
    {"reference": "000008", "account": "C00002", "date": "2021-03-02", "amount": "3250.88", "type": "inflow", "category": "savings" ,"user_id": 1}
]

INPUT_MANY_TRANSACTIONS_2_FAIL = [
    {"reference": "000009", "account": "C00001", "date": "2021-01-01", "amount": "51.13", "type": "outflow", "category": "groceries", "user_id": 1},
    {"reference": "000010", "account": "C00001", "date": "2021-01-10", "amount": "2500.72", "type": "inflow", "category": "salary", "user_id": 1}
]

INPUT_MANY_TRANSACTIONS_3_FAIL = [
    {"reference": "000011", "account": "C00001", "date": "2021-01-01", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1},
    {"reference": "000011", "account": "C00001", "date": "2021-01-10", "amount": "2500.72", "type": "inflow", "category": "salary", "user_id": 1}
]

INPUT_MANY_TRANSACTIONS_4_FAIL = [
    {"reference": "000012", "account": "C00001", "date": "2021-01-01", "amount": "51.13", "type": "outflow", "category": "groceries", "user_id": 1},
    {"reference": "000013", "account": "C00001", "date": "2021-01-10", "amount": "-2500.72", "type": "inflow", "category": "salary", "user_id": 1}
]

INPUT_MANY_TRANSACTIONS_5_FAIL = [
    {"reference": "000014", "account": "C00001", "date": "2021-01-01", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1},
    {"reference": "000015", "account": "C00001", "date": "2021-01-10", "amount": "-2500.72", "type": "inflow", "category": "salary", "user_id": 1}
]

OUTPUT_SUMMARY_ACCOUNT = [
    {"account": "C00099", "balance": "1738.87", "total_inflow": "2500.72", "total_outflow": "-761.85"},
    {"account": "S00012", "balance": "150.72", "total_inflow": "150.72", "total_outflow": "0.00"},
]

OUTPUT_SUMMARY_CATEGORIES = {"inflow": {"salary": "2500.72", "savings": "150.72"}, "outflow": {"groceries": "-51.13", "rent": "-560.00", "transfer": "-150.72"}}
