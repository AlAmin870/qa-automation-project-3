import pytest
import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

@pytest.fixture(scope="module")
def csv_data():
    return pd.read_csv(DATA_DIR / "employees.csv")

@pytest.fixture(scope="module")
def json_data():
    with open(DATA_DIR / "sales.json", "r") as f:
        return json.load(f)