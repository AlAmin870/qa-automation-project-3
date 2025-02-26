import pandas as pd
import json
import logging
import re
import yaml
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
CONFIG_DIR = BASE_DIR / "config"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load config
with open(CONFIG_DIR / "validation_rules.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

# Setup logging
logging.basicConfig(
    filename=REPORT_DIR / "test_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

def test_csv_required_fields(csv_data):
    missing = [col for col in CONFIG["csv"]["required_fields"] if col not in csv_data.columns]
    assert not missing, f"Missing columns: {missing}"
    logging.info("CSV required fields validated")

def test_csv_valid_emails(csv_data):
    pattern = re.compile(CONFIG["csv"]["email_pattern"])
    invalid = csv_data[~csv_data["email"].str.match(pattern, na=False)]["email"].tolist()
    assert not invalid, f"Invalid emails: {invalid}"
    logging.info("CSV emails validated")

def test_csv_positive_salary(csv_data):
    invalid = csv_data[csv_data["salary"] <= 0]["salary"].tolist()
    assert not invalid, f"Negative or zero salaries: {invalid}"
    logging.info("CSV salaries validated")
def test_csv_valid_dates(csv_data):
    invalid = []
    future = []
    for date in csv_data["hire_date"]:
        try:
            parsed = datetime.strptime(str(date), CONFIG["csv"]["date_format"])
            if parsed > datetime.now():
                future.append(date)
        except ValueError:
            invalid.append(date)
    assert not (invalid or future), f"Invalid dates: {invalid}, Future dates: {future}"
    logging.info("CSV dates validated")

def test_json_employee_id_exists(csv_data, json_data):
    employee_ids = set(csv_data["id"])
    invalid = [item["transaction_id"] for item in json_data if item["employee_id"] not in employee_ids]
    assert not invalid, f"Transactions with unknown employee IDs: {invalid}"
    logging.info("JSON employee IDs validated")

def test_json_positive_quantity(json_data):
    invalid = [item["transaction_id"] for item in json_data if item["quantity"] <= 0]
    assert not invalid, f"Negative or zero quantities: {invalid}"
    logging.info("JSON quantities validated")

def test_json_no_empty_products(json_data):
    empty = [item["transaction_id"] for item in json_data if not item["product"]]
    assert not empty, f"Empty product names: {empty}"
    logging.info("JSON products validated")

def test_json_valid_dates(json_data):
    invalid = []
    future = []
    for item in json_data:
        try:
            parsed = datetime.strptime(item["date"], CONFIG["csv"]["date_format"])
            if parsed > datetime.now():
                future.append(item["date"])
        except ValueError:
            invalid.append(item["transaction_id"])
    assert not (invalid or future), f"Invalid dates: {invalid}, Future dates: {future}"
    logging.info("JSON dates validated")

def test_generate_excel_report(csv_data, json_data):
    summary = {
        "Total Employees": len(csv_data),
        "Average Salary": csv_data["salary"].mean(),
        "Total Transactions": len(json_data),
        "Total Revenue": sum(item["quantity"] * item["price"] for item in json_data)
    }
    issues = {
        "Invalid Emails": len(csv_data[~csv_data["email"].str.match(CONFIG["csv"]["email_pattern"], na=False)]),
        "Negative Salaries": len(csv_data[csv_data["salary"] <= 0]),
        "Negative Quantities": len([item for item in json_data if item["quantity"] <= 0])
    }
    df_summary = pd.DataFrame([summary | issues])
    output_file = REPORT_DIR / "validation_summary.xlsx"
    df_summary.to_excel(output_file, index=False)
    # Add chart
    fig, ax = plt.subplots()
    df_summary[["Total Employees", "Total Transactions"]].plot(kind="bar", ax=ax)
    plt.savefig(REPORT_DIR / "summary_chart.png")
    plt.close()
    assert output_file.exists(), "Excel report not generated!"
    logging.info("Excel report with chart generated")

def test_performance_metrics():
    start = datetime.now()
    pd.read_csv(DATA_DIR / "employees.csv")
    with open(DATA_DIR / "sales.json", "r") as f:
        json.load(f)
    duration = (datetime.now() - start).total_seconds()
    assert duration < 2, f"Data loading too slow: {duration}s"
    logging.info(f"Performance test passed in {duration}s")