# customer_controller.py

import pandas as pd
from flask import jsonify,request
from app.models.customer_model import CustomerModel
from marshmallow import ValidationError
import logging

class CustomerController:

    @staticmethod
    def get_all_customers():
        # Logic to load all customers from CSV
        df = pd.read_csv('Northwind_database_csv/customers.csv')
        return jsonify(df.to_dict(orient='records'))

    @staticmethod
    def get_customer(customer_id):
        # Logic to load a specific customer from CSV
        df = pd.read_csv('Northwind_database_csv/customers.csv')
        customer = df[df['CustomerID'] == customer_id]
        if customer.empty:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer.to_dict(orient='records'))
        # return jsonify(customer.to_dict(orient='records')[0])

    @staticmethod        
    def add_customer():
        json_data=request.get_json()
        try:
            data = CustomerModel.schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        df = CustomerModel.load_data()
        if not df[df['CustomerID'] == data['CustomerID']].empty:
            return jsonify({'error': 'Customer already exists'}), 400

        df = df._append(pd.DataFrame([data]), ignore_index=True)
        CustomerModel.save_data(df)
        return jsonify(data), 201


    @staticmethod
    def update_customer(customer_id):
        json_data=request.get_json()
        # Load the data
        df = CustomerModel.load_data()
        logging.debug(f"Loaded data: {df}")
    
        # Check if the order exists
        if df[df['CustomerID'] == (customer_id)].empty:
            return jsonify({'error': 'Customer not found'}), 404
    
        # Validate and process the input data
        try:
            data = CustomerModel.schema.load(json_data, partial=True)
            logging.debug(f"Validated data: {data}")
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
    
        # Update the DataFrame
        df.loc[df['CustomerID'] == (customer_id), list(data.keys())] = list(data.values())
        logging.debug(f"Update  d DataFrame: {df}")
    
        # Save the updated data
        CustomerModel.save_data(df)

        updated_customer = df[df['CustomerID'] == (customer_id)].to_dict(orient='records')[0]
        logging.debug(f"Updated Customer: {updated_customer}")
    
        return jsonify(updated_customer), 200

    @staticmethod
    def delete_customer(customer_id):
        df = pd.read_csv('Northwind_database_csv/customers.csv')
        
        # Check if the customer exists
        if df[df['CustomerID'] == customer_id].empty:
            return jsonify({'error': 'Customer not found'}), 404
        
        # Delete the customer record
        df = df[df['CustomerID'] != customer_id]
        
        # Save the updated DataFrame to CSV
        df.to_csv('Northwind_database_csv/customers.csv', index=False)
        
        # Optionally, perform additional actions like calling a model method
        CustomerModel.save_data(df)
        
        return jsonify({'message': 'Customer deleted successfully'}), 200
    
    @staticmethod
    def get_customer_orders(customer_id):
        # Logic to get orders for a customer
        df_orders = pd.read_csv('Northwind_database_csv/orders.csv')
        customer_orders = df_orders[df_orders['CustomerID'] == customer_id]
        if customer_orders.empty:
            return jsonify({'error': 'No orders found for this customer'}), 404
        return jsonify(customer_orders.to_dict(orient='records'))
