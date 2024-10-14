# app/models/customer_model.py
from app.models.base_model import BaseModel
from app.config import Config
from app.schemas.customer_schema import CustomerSchema

class CustomerModel(BaseModel):
    csv_file = Config.CUSTOMERS_CSV
    schema = CustomerSchema()
