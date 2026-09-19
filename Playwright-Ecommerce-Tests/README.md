# Playwright login automation sample

A Python/pytest example that logs in to SauceDemo and asserts that the inventory list is visible. The current fixture launches Chromium; this sample does not yet implement a multi-browser matrix, cart or checkout tests.

## Included files

- `tests/test_login.py`: parameterized login test with Playwright assertions.
- `tests/conftest.py`: browser/context setup and cleanup.
- `pytest.ini`: Allure result directory configuration.

## Execution prerequisites

Use an isolated Python environment. Install the existing requirements, **plus `pytest-playwright`**, because `conftest.py` depends on its `playwright` fixture:

```bash
python -m pip install -r requirements.txt pytest-playwright
python -m playwright install chromium
python -m pytest
```

The fixture currently launches a headed browser, so it requires a graphical session. Allure results are written to `allure-report/`; rendering an HTML report requires the separate Allure CLI. Execution against SauceDemo was not performed as part of the portfolio redesign.

[Repository overview](../README.md)
