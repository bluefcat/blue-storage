from typing import Any
import yaml

def load_config(config_path: str) -> Any:
    with open(config_path) as file:
        return yaml.safe_load(file)

setting: dict = load_config("./config/config.yaml")
