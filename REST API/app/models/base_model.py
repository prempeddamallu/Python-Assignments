# app/models/base_model.py
import pandas as pd
from app.config import Config
import os

class BaseModel:
    csv_file = ''
    schema = None  # Should be set in child classes

    @classmethod
    def load_data(cls):
        if not os.path.exists(cls.csv_file):
            # Create CSV with appropriate columns if it doesn't exist
            df = pd.DataFrame(columns=cls.schema.fields.keys())
            df.to_csv(cls.csv_file, index=False)
            return df
        return pd.read_csv(cls.csv_file)

    @classmethod
    def save_data(cls, df):
        df.to_csv(cls.csv_file, index=False)
