import pytest
import pandas as pd
from flask import Flask
from app.controllers.order_controller import OrderController


@pytest.fixture
def client():
    app = Flask(__name__)
    app.add_url_rule("/orders", view_func=OrderController.get_all_orders)
    app.add_url_rule("/orders/<order_id>", view_func=OrderController.get_order_by_id)
    app.add_url_rule(
        "/orders", methods=["POST"], view_func=OrderController.create_order
    )
    app.add_url_rule(
        "/orders/<order_id>", methods=["PUT"], view_func=OrderController.update_order
    )
    app.add_url_rule(
        "/orders/<order_id>", methods=["DELETE"], view_func=OrderController.delete_order
    )
    app.add_url_rule(
        "/customers/<customer_id>/orders",
        view_func=OrderController.get_orders_by_customer,
    )
    return app.test_client()


def test_get_all_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert "application/json" in response.content_type


def test_get_order_by_id(client):
    response = client.get("/orders/10248")
    assert response.status_code == 200
    assert "application/json" in response.content_type


def test_create_order(client):
    data = {
        "CustomerID": "TOMSP",
        "EmployeeID": 6,
        "Freight": 11.61,
        "OrderDate": "1996-07-05",
        "OrderID": 11111,
        "RequiredDate": "1996-08-16",
        "ShipAddress": "Luisenstr. 48",
        "ShipCity": "M\u00fcnster",
        "ShipCountry": "Germany",
        "ShipName": "Toms Spezialit\u00e4ten",
        "ShipPostalCode": "44087",
        "ShipRegion": "NaN",
        "ShipVia": 1,
        "ShippedDate": "1996-07-10"
    }
    response = client.post("/orders", json=data)
    assert response.status_code == 201
    assert response.json["OrderID"] == 11111




def test_update_order(client):
    data = {"ShipName": "Bahamas"}
    response = client.put("/orders/10248", json=data)
    assert response.status_code == 200


def test_delete_order(client):
    response = client.delete("/orders/11111")
    assert response.status_code == 200
