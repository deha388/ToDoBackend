import yaml
from importlib import resources


def load_config_yaml():
    with open("src\collection\config.yaml", "r") as file:
        cfg = yaml.safe_load(file)
    return cfg