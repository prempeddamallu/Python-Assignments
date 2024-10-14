import pytest
import pandas as pd
from flask import Flask
from app.controllers.customer_controller import CustomerController

@pytest.fixture
def client():
    app = Flask(__name__)
    app.add_url_rule("/customers", view_func=CustomerController.get_all_customers)
    app.add_url_rule(
        "/customers/<customer_id>", view_func=CustomerController.get_customer
    )
    app.add_url_rule(
        "/customers", methods=["POST"], view_func=CustomerController.add_customer
    )
    app.add_url_rule(
        "/customers/<customer_id>",
        methods=["PUT"],
        view_func=CustomerController.update_customer,
    )
    app.add_url_rule(
        "/customers/<customer_id>/orders",
        view_func=CustomerController.get_customer_orders,
    )
    return app.test_client()

def test_get_all_customers(client):
    response = client.get("/customers")
    assert response.status_code == 200
    assert "application/json" in response.content_type

def test_get_customer(client):
    response = client.get("/customers/BONAP")
    assert response.status_code == 200
    assert "application/json" in response.content_type


def test_add_customer(client):
    data = {
        "Address": "Obere Str. 5",
        "City": "Berlin",
        "CompanyName": "Alfreds Futterkiste",
        "ContactName": "Maria Sanders",
        "ContactTitle": "Sales Executive",
        "Country": "Germany",
        "CustomerID": "XUID",
        "Fax": "030-0076545",
        "Phone": "030-0074321",
        "PostalCode": "12209",
        "Region": "NaN"
    }
    response = client.post("/customers", json=data)
    assert response.status_code == 201
    assert response.json["CustomerID"] == "XUID"

    # Clean up the test data by removing the newly added customer
    df = pd.read_csv('Northwind_database_csv/customers.csv')
    df = df[df['CustomerID'] != "XUID"]
    df.to_csv('Northwind_database_csv/customers.csv', index=False)

def test_update_customer(client):
    data = {"CompanyName": "Updated "}
    response = client.put("/customers/BONAP", json=data)
    assert response.status_code == 200
    assert response.json['CompanyName'] == 'Updated '

def test_get_customer_orders(client):
    response = client.get("/customers/ALFKI/orders")
    assert response.status_code == 200
    assert "application/json" in response.content_type
