import pandas as pd
import sqlite3
from utils import config
import pickle

def retrieve_training_dataset(path):
    with sqlite3.connect(path) as connection:
        df = pd.read_sql(f"SELECT * FROM {config.TABLE_NAME}", connection)
    return df

def load(file_name=config.SERIALIZED_MODEL):
     return pickle.load(open(f"{config.MODELS_PATH}/{file_name}", "rb"))
