import pandas as pd
from flask import jsonify,request
from app.models.product_model import ProductModel
from marshmallow import ValidationError
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class ProductController:
    @staticmethod
    def get_all_products():
        df = ProductModel.load_data()
        data = df.to_dict(orient='records')
        return jsonify(data), 200

    @staticmethod
    def get_product_by_id(product_id):
        df = ProductModel.load_data()
        product = df[df['ProductID'] == int(product_id)]
        if product.empty:
            return jsonify({'error': 'Product not found'}), 404
        data = product.to_dict(orient='records')[0]
        return jsonify(data), 200

    @staticmethod
    def create_product():
        json_data=request.get_json()
        try:
            data = ProductModel.schema.load(json_data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

        df = ProductModel.load_data()
        if not df[df['ProductID'] == data['ProductID']].empty:
            return jsonify({'error': 'Product already exists'}), 400

        df = df._append(pd.DataFrame([data]), ignore_index=True)
        ProductModel.save_data(df)
        return jsonify(data), 201

    

    def update_product(product_id):
        json_data=request.get_json()
        # Load the data
        df = ProductModel.load_data()
        logging.debug(f"Loaded data: {df}")
    
        # Check if the product exists
        if df[df['ProductID'] == int(product_id)].empty:
            return jsonify({'error': 'Product not found'}), 404
    
        # Validate and process the input data
        try:
            data = ProductModel.schema.load(json_data, partial=True)
            logging.debug(f"Validated data: {data}")
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
    
        # Update the DataFrame
        df.loc[df['ProductID'] == int(product_id), list(data.keys())] = list(data.values())
        logging.debug(f"Update  d DataFrame: {df}")
    
        # Save the updated data
        ProductModel.save_data(df)
    
        # Retrieve the updated product
        updated_product = df[df['ProductID'] == int(product_id)].to_dict(orient='records')[0]
        logging.debug(f"Updated product: {updated_product}")
    
        return jsonify(updated_product), 200
    
    

    @staticmethod
    def delete_product(product_id):
        df = ProductModel.load_data()
        if df[df['ProductID'] == int(product_id)].empty:
            return jsonify({'error': 'Product not found'}), 404

        df = df[df['ProductID'] != int(product_id)]
        ProductModel.save_data(df)
        return jsonify({'message': 'Product deleted successfully'}), 200
