# QA Automation Project 3: Enterprise Data Validation Suite

A professional-grade automation suite for validating large-scale employee (CSV) and sales (JSON) data, with advanced reporting.

## Setup
1. Install: `pip install pandas pytest openpyxl matplotlib requests pyyaml`.
2. Run: `pytest tests/test_data_validation.py -v`.

## Features
- **Advanced Validation:** Regex for emails, date parsing, cross-file ID checks.
- **Realistic Data:** 50 employees (CSV), 30 sales transactions (JSON) with intentional errors.
- **Reporting:** Logs (`test_log.log`), Excel summary with issues (`validation_summary.xlsx`), bar chart (`summary_chart.png`).
- **Configurable:** Rules in `validation_rules.yaml`.
- **Performance:** Data loading validated under 2 seconds.

## Tests
1. **CSV Required Fields:** Ensures all columns exist.
2. **CSV Valid Emails:** Checks email format (regex).
3. **CSV Positive Salary:** Detects negative/zero salaries.
4. **CSV Valid Dates:** Flags invalid/future dates.
5. **JSON Employee ID Exists:** Verifies IDs match CSV.
6. **JSON Positive Quantity:** Ensures quantities > 0.
7. **JSON No Empty Products:** Validates product names.
8. **JSON Valid Dates:** Checks transaction dates.
9. **Generate Excel Report:** Produces summary with chart.
10. **Performance Metrics:** Confirms fast data loading.

## Results
- **Dataset:** 50 employees, 30 transactions with errors (e.g., invalid emails, negative salaries, future dates).
- **Outcome:** 3 tests pass, 7 fail as expected—see `reports/test_output.txt`.
- **Outputs:** Excel report with stats/issues and a bar chart showcase enterprise-level QA.

## Impact
Built for scale and precision, this suite demonstrates real-world data validation and reporting—ready for enterprise challenges.
