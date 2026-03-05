import json

CONFIG_FILE = "config.json"

def load_config() -> dict:
    """
    Loads the user config from a JSON file
    :return: dictionary of settings or empty dict if not found
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(data_dict: dict) -> None:
    """
    Saves a configuration to a local JSON file
    :param data_dict: dictionary of save data with keys being UI elements
    :return: None
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(data_dict, f, indent=4)
