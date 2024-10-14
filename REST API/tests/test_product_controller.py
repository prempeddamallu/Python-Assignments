import pytest
from flask import Flask
from app.controllers.product_controller import ProductController
import pandas as pd

@pytest.fixture
def client():
    app = Flask(__name__)
    app.add_url_rule("/products", view_func=ProductController.get_all_products)
    app.add_url_rule(
        "/products/<product_id>", view_func=ProductController.get_product_by_id
    )
    app.add_url_rule(
        "/products", methods=["POST"], view_func=ProductController.create_product
    )
    app.add_url_rule(
        "/products/<product_id>",
        methods=["PUT"],
        view_func=ProductController.update_product,
    )
    app.add_url_rule(
        "/products/<product_id>",
        methods=["DELETE"],
        view_func=ProductController.delete_product,
    )
    return app.test_client()


def test_get_all_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert "application/json" in response.content_type


def test_get_product_by_id(client):
    response = client.get("/products/1")
    assert response.status_code == 200
    assert "application/json" in response.content_type


def test_create_product(client):
    data = {
        "ProductID": 100,
        "ProductName": "Chai",
        "SupplierID": 5,
        "CategoryID": 2,
        "QuantityPerUnit": "10 boxes x 20 bags",
        "UnitPrice": 18.0,
        "UnitsInStock": 39,
        "UnitsOnOrder": 0,
        "ReorderLevel": 10,
        "Discontinued": False,
    }

    response = client.post("/products", json=data)
    print(response.status_code)
    assert response.status_code == 201

    


def test_update_product(client):
    data = {"ProductName": "Updated Product"}

    # # Perform the PUT request to update the product
    response = client.put("/products/100", json=data)

    # # Verify the response
    assert response.status_code == 200


def test_delete_product(client):
    response = client.delete("/products/100")
    assert response.status_code == 200
