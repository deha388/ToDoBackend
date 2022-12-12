import sqlalchemy
from datetime import datetime
from config import load_config_yaml

cfg = load_config_yaml()

def load_sqlite():
    try:
        engine = sqlalchemy.create_engine(cfg["sqlite"]["path"])
        return engine
    except Exception as e:
        raise e
