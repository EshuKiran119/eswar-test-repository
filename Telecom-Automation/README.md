# Selenium and Robot Framework login examples

A small demonstration structure with a Selenium login page object, a Python unittest and a Robot Framework login scenario. The folder name reflects the original organization; the public code does not implement telecom provisioning or SIM-management workflows.

## Included files

- `pages/login_page.py`: login locators and an explicit URL wait.
- `tests/python/test_dashboard.py`: unittest browser lifecycle and login assertion.
- `tests/robot/login_tests.robot`: browser-driven login example.
- `run_tests.py`: unittest entry point.

## Execution gaps

The examples require setup before they are executable:

- The Python test does not navigate to an application URL before locating the login form.
- Application locators, test credentials and the expected redirect must match the selected test environment.
- The Robot scenario needs `robotframework-seleniumlibrary`, which is missing from the existing requirements.
- The Robot `Resource` points to an empty Python file; it needs a valid Robot resource or an implemented Python library import.
- `utils/custom_keywords.py` and `utils/helpers.py` are empty placeholders.

The redesign preserves these source files and records their limitations instead of presenting them as a completed production framework. No application tests were executed during the redesign.

[Repository overview](../README.md)
