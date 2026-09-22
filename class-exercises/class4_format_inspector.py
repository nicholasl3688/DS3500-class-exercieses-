import json
import logging
from pathlib import Path

import pandas as pd
import yaml
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

def inspect_csv(filepath):
    """read a csv file and display basic information"""
    df = pd.read_csv(filepath)
    logger.info(f"loading csv {filepath}...")
    print(df.head(3))

def inspect_json(filepath):
    """Read a JSON file and display basic information."""
    # TODO:
    # 1. Open the file and read it using json.load().
    # 2. Log the filepath at INFO.
    # 3. Print the contents.
    logger.info(f"reading json file: {filepath}")
    with open(filepath, "r") as f:
        data = json.load(f)

    print(data["Status"])
    print(data["Data"])


def inspect_yaml(filepath):
    """Read a YAML file and display basic information."""
    # TODO:
    # 1. Open the file and read it using yaml.safe_load().
    # 2. Log the filepath at INFO.
    # 3. Print the contents.
    logger.info(f"reading yaml file: {filepath}")
    with open(filepath, "r") as f:
        config = yaml.safe_load(f)

    print(config["cleaning"]["missing"])
    print(config["processing"]["batch_size"])
    print(config['school']['course'])



def inspect_env():
    """Read a .env file and display basic information."""
    load_dotenv()

    keys = [
        key for key in ["USERNAME", "PASSWORD"]
        if os.getenv(key) is not None
    ]

    # TODO:
    # 1. Log at INFO that .env was loaded.
    # 2. Print keys.
    # Do not print passwords, API keys, or other secret values.

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    api_key = os.getenv("API_KEY")

    print(username)


    logger.info(f"loaded file .env...")


def main():
    # TODO:
    # 1. Create a Path object for the data directory.
    # 2. Use the / operator to build the CSV, JSON, and YAML paths.
    # 3. Call each inspection function using the matching path.
    # 4. Call inspect_env() without an argument.
    file_path = Path("data")
    csv_path = Path("data") / 'sample.csv'
    json_path = Path("data") / 'sample.json'
    yaml_path = Path("data") / 'sample.yaml'

    inspect_csv(csv_path)
    inspect_json(json_path)
    inspect_yaml(yaml_path)

    inspect_env()



if __name__ == "__main__":
    main()