# Python + Pytest + Playwright Automation Framework

A UI test automation framework built with **Python**, **Pytest** and **Playwright**, using the **Page Object Model (POM)** pattern. The tests run against the [SauceDemo](https://www.saucedemo.com) e-commerce demo website.

## Features

- Page Object Model for clean, reusable code
- Cross-browser testing (Chromium, Firefox, WebKit)
- Headless and headed execution
- Parallel test execution with `pytest-xdist`
- Automatic retry of failed tests with `pytest-rerunfailures`
- Separate test data files
- GitHub Actions workflow for CI

## Project Structure

```
.
├── .github/workflows/   # CI pipeline (GitHub Actions)
├── data/                # Test data
├── pages/               # Page Object classes
├── tests/               # Test cases
├── utils/               # Helper functions
├── conftest.py          # Shared fixtures
├── pytest.ini           # Pytest configuration
├── requirements.txt     # Python dependencies
├── commands.txt         # Handy run commands
└── setup.txt            # Setup notes
```

## Prerequisites

- Python 3.8 or newer
- Git
- Internet connection (tests run against the live SauceDemo site)

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright browsers
playwright install
```

## Running the Tests

```bash
# Run all tests (headless by default)
pytest tests/

# Run with the browser visible
pytest tests/ --headed

# Choose a browser, show the window and slow things down
pytest tests/ --browser=firefox --headed --slowmo=250

# Run tests in parallel
pytest -n auto

# Retry failed tests
pytest --reruns 3 --reruns-delay 2

# Verbose output
pytest tests/ -v
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `pytest: command not found` | Activate the virtual environment first |
| Browser not found | Run `playwright install` |
| `-n` option not recognized | `pip install pytest-xdist` |
| `--reruns` option not recognized | `pip install pytest-rerunfailures` |

## Credits

Based on the original project by [Pranjal](https://github.com/Pranjal-singh0/Ecommerce_Playwright-Automation-Python).

## License
MIT
