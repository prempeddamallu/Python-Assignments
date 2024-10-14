from app.controllers.customer_controller import CustomerController
from app.controllers.product_controller import ProductController
from app.controllers.order_controller import OrderController
from flask import request, render_template

def register_routes(app):

    def home_page():
        return render_template('index.html')
    
    app.add_url_rule('/', view_func=home_page, methods=['GET'])

    # Customer Routes
    def get_customers():
        return CustomerController.get_all_customers()

    def get_customer(customer_id):
        return CustomerController.get_customer(customer_id)

    def add_customer():
        return CustomerController.add_customer()

    def update_customer(customer_id):
        return CustomerController.update_customer(customer_id)
    
    def delete_customer(customer_id):
        return CustomerController.delete_customer(customer_id)

    def get_customer_orders(customer_id):
        return CustomerController.get_customer_orders(customer_id)

    app.add_url_rule('/customers', view_func=get_customers, methods=['GET']) 
    app.add_url_rule('/customers/<string:customer_id>', view_func=get_customer, methods=['GET']) 
    app.add_url_rule('/customers', view_func=add_customer, methods=['POST']) 
    app.add_url_rule('/customers/<string:customer_id>', view_func=update_customer, methods=['PUT']) 
    app.add_url_rule('/customers/<string:customer_id>/orders', view_func=get_customer_orders, methods=['GET']) 
    app.add_url_rule('/customers/<string:customer_id>', view_func=delete_customer, methods=['DELETE'])

    # Product Routes
    def get_products():
        return ProductController.get_all_products()

    def get_product(product_id):
        return ProductController.get_product_by_id(product_id)

    def add_product():
        return ProductController.create_product()

    def update_product(product_id):
        return ProductController.update_product(product_id)

    app.add_url_rule('/products', view_func=get_products, methods=['GET']) 
    app.add_url_rule('/products/<int:product_id>', view_func=get_product, methods=['GET']) 
    app.add_url_rule('/products', view_func=add_product, methods=['POST']) 
    app.add_url_rule('/products/<int:product_id>', view_func=update_product, methods=['PUT']) 

    # Order Routes
    def get_orders():
        return OrderController.get_all_orders()

    def get_order(order_id):
        return OrderController.get_order_by_id(order_id)

    def add_order():
        return OrderController.create_order()

    def update_order(order_id):
        return OrderController.update_order(order_id)

    app.add_url_rule('/orders', view_func=get_orders, methods=['GET']) 
    app.add_url_rule('/orders/<int:order_id>', view_func=get_order, methods=['GET']) 
    app.add_url_rule('/orders', view_func=add_order, methods=['POST']) 
    app.add_url_rule('/orders/<int:order_id>', view_func=update_order, methods=['PUT']) 
