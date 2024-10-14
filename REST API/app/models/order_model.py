# app/models/order_model.py
from app.models.base_model import BaseModel
from app.config import Config
from app.schemas.order_schema import OrderSchema

class OrderModel(BaseModel):
    csv_file = Config.ORDERS_CSV
    schema = OrderSchema()
