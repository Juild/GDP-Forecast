import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

DATABASE_PATH = os.path.join(BASE_DIR, "db.sqlite3")

MODELS_PATH = os.path.join(BASE_DIR, "models")

LOGS_PATH = os.path.join(BASE_DIR, "logs")

GDP = "NY.GDP.MKTP.KD.ZG"
