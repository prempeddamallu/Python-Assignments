# app/schemas/customer_schema.py
from marshmallow import Schema, fields, validates, ValidationError

class CustomerSchema(Schema):
    CustomerID = fields.String(required=True, validate=lambda x: len(x) <= 5)
    CompanyName = fields.String(required=True)
    ContactName = fields.String()
    ContactTitle = fields.String()
    Address = fields.String()
    City = fields.String()
    Region = fields.String()
    PostalCode = fields.String()
    Country = fields.String()
    Phone = fields.String()
    Fax = fields.String()
    
    @validates('CustomerID')
    def validate_customer_id(self, value):
        if not value.isalnum():
            raise ValidationError('CustomerID must be alphanumeric.')
