# iBinder Automation Tests

This repository contains automated tests for the iBinder application using Playwright.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

To run the tests:
```bash
pytest test_ibinder_login_playwright.py -v
```

## Test Structure

- `test_ibinder_login_playwright.py`: Contains the Playwright test for login functionality
- `conftest.py`: Contains pytest fixtures and configuration
- `requirements.txt`: Lists all Python dependencies

## Features

- Automated login testing
- Browser automation using Playwright
- Detailed logging and error reporting
- Configurable test parameters

## Notes

- The tests are configured to run in headed mode by default for better visibility
- For CI/CD environments, set `headless=True` in `conftest.py`
- Test credentials are currently hardcoded and should be moved to environment variables in production 