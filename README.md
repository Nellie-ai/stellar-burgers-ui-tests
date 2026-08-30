# Stellar Burgers UI Tests

[![CI](https://github.com/Nellie-ai/stellar-burgers-ui-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/Nellie-ai/stellar-burgers-ui-tests/actions/workflows/ci.yml)

English | [Русский](README_RU.md)

## Overview

An end-to-end UI test suite for the educational [Stellar Burgers](https://stellarburgers.education-services.ru/) web application. The project uses Selenium, pytest, Page Object Model, API-based test-data preparation, and Allure reporting.

## Tech stack

| Area | Tools |
| --- | --- |
| Language | Python 3.10+ (CI runs Python 3.12) |
| Test runner | pytest |
| Browser automation | Selenium WebDriver |
| Test-data setup | requests-based API client |
| Reporting | Allure Pytest |
| Design pattern | Page Object Model |
| CI | GitHub Actions |

## What is tested / Coverage

The suite contains 8 logical scenarios. Each scenario is parameterized for Google Chrome and Mozilla Firefox, producing 16 collected test cases.

### Constructor and navigation

- navigation from the order feed to the constructor;
- navigation from the constructor to the order feed;
- opening ingredient details in a modal window;
- closing the ingredient-details modal;
- increasing the ingredient counter after adding an ingredient.

### Order feed

- increasing the all-time completed-order counter;
- increasing the today completed-order counter;
- showing the new order number in the “In progress” section.

## Project structure

```text
.
├── .github/workflows/
│   ├── ci.yml                    # constructor checks on PR, push, and manual run
│   └── e2e.yml                   # full E2E run manually and weekly
├── locators/                     # Selenium locators
├── pages/                        # Page Objects and shared WebDriver actions
├── tests/
│   ├── test_constructor.py       # constructor and navigation scenarios
│   └── test_order_feed.py        # order creation and feed scenarios
├── utils/
│   ├── api_client.py             # user setup and cleanup through the API
│   ├── constants.py              # URLs and configurable timeouts
│   └── data.py                   # test-user model and data generation
├── conftest.py                   # browser, auth, and screenshot fixtures
├── pytest.ini                    # pytest configuration and browser markers
└── requirements.txt
```

Authentication is prepared through the API. The user-facing ingredient and order flows are exercised through the browser UI.

## Local setup

Requirements:

- Python 3.10 or newer;
- Google Chrome and Mozilla Firefox;
- network access to the educational Stellar Burgers web application and API;
- Allure CLI only if a local HTML report is needed.

Selenium Manager resolves compatible browser drivers automatically.

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Activate the virtual environment using the command appropriate for your operating system.

### Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `STELLAR_BURGERS_URL` | `https://stellarburgers.education-services.ru` | Web application URL |
| `STELLAR_BURGERS_API_URL` | value of `STELLAR_BURGERS_URL` | API base URL |
| `SELENIUM_TIMEOUT` | `15` | Default request timeout in seconds |
| `ORDER_TIMEOUT` | `180` | Maximum wait for order creation and display in seconds |

Example:

```bash
ORDER_TIMEOUT=240 python -m pytest -m chrome -v
```

PowerShell:

```powershell
$env:ORDER_TIMEOUT = "240"
python -m pytest -m chrome -v
```

### Test commands

```bash
python -m pytest -v
python -m pytest -m chrome -v
python -m pytest -m firefox -v
python -m pytest tests/test_constructor.py -v
```

### Allure

```bash
python -m pytest --alluredir=allure_results --clean-alluredir
allure serve allure_results
```

On setup or test failure, the suite attaches a browser screenshot when a WebDriver is available.

## CI

- `.github/workflows/ci.yml` runs the constructor scenarios in Chrome and Firefox for pull requests, pushes to `main`, and manual dispatch; Allure results are uploaded per browser.
- `.github/workflows/e2e.yml` runs the full suite in both browsers manually and every Monday at 03:00 UTC; Allure results are uploaded per browser.

## Notes / Limitations

- The tests depend on the availability and behavior of the public educational web application and API.
- Order-feed scenarios create real orders, so global order counters change on the test stand.
- Counter checks can take up to three minutes; parallel execution of feed scenarios is not recommended because they share global counters.
- Browsers run in headless mode in the test fixtures.
- `allure_results/` is generated locally or in CI and is not tracked by Git.

## License / Provenance

The repository includes an MIT LICENSE for the original test code and PROVENANCE.md describing the educational origin of the scenarios and the boundary with the external application. The MIT License applies only to original test code in this repository and does not grant rights to the external application or third-party assets.
