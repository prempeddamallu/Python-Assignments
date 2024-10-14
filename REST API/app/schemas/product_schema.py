# app/schemas/product_schema.py
from marshmallow import Schema, fields, validates, ValidationError

class ProductSchema(Schema):
    ProductID = fields.Integer(required=True)
    ProductName = fields.String(required=True)
    SupplierID = fields.Integer()
    CategoryID = fields.Integer()
    QuantityPerUnit = fields.String()
    UnitPrice = fields.Float()
    UnitsInStock = fields.Integer()
    UnitsOnOrder = fields.Integer()
    ReorderLevel = fields.Integer()
    Discontinued = fields.Boolean()
    
    @validates('UnitPrice')
    def validate_unit_price(self, value):
        if value is not None and value < 0:
            raise ValidationError('UnitPrice cannot be negative.')
