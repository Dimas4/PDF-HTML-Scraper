import os

import yaml


def get_config() -> dict:
    """
    Loads the config file
    :return: dict
    """
    with open(os.path.join('config', 'config.yaml'), 'r') as file:
        config = yaml.load(file)
    return config
