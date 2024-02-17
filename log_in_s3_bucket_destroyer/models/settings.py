import os
from pyaml_env import parse_config

SETTINGS = None


def load_config(config_path: str) -> None:
    global SETTINGS

    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    SETTINGS = parse_config(config_path)
