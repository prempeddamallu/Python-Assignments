# app/models/product_model.py
from app.models.base_model import BaseModel
from app.config import Config
from app.schemas.product_schema import ProductSchema

class ProductModel(BaseModel):
    csv_file = Config.PRODUCTS_CSV
    schema = ProductSchema()
