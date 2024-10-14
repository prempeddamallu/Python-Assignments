# app/config.py
import os

class Config:
    # print(os.path.abspath(__file__)) # c:\Users\premk\Documents\PythonAssignments\REST API\app\config.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(BASE_DIR) #c:\Users\premk\Documents\PythonAssignments\REST API\app
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'Northwind_database_csv')
    # print(DATA_DIR) # c:\Users\premk\Documents\PythonAssignments\REST API\Northwind_database_csv
    CUSTOMERS_CSV = os.path.join(DATA_DIR, 'customers.csv')
    # print(CUSTOMERS_CSV) # c:\Users\premk\Documents\PythonAssignments\REST API\Northwind_database_csv\customers.csv
    PRODUCTS_CSV = os.path.join(DATA_DIR, 'products.csv')
    ORDERS_CSV = os.path.join(DATA_DIR, 'orders.csv')
