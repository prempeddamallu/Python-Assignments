# app/schemas/order_schema.py
from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class OrderSchema(Schema):
    OrderID = fields.Integer(required=True)
    CustomerID = fields.String(required=True)
    EmployeeID = fields.Integer()
    OrderDate = fields.Date()
    RequiredDate = fields.Date()
    ShippedDate = fields.Date()
    ShipVia = fields.Integer()
    Freight = fields.Float()
    ShipName = fields.String()
    ShipAddress = fields.String()
    ShipCity = fields.String()
    ShipRegion = fields.String()
    ShipPostalCode = fields.String()
    ShipCountry = fields.String()
    
    @validates('OrderDate')
    def validate_order_date(self, value):
        if value and value > datetime.today().date():
            raise ValidationError('OrderDate cannot be in the future.')
