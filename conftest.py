# conftest.py
from dotenv import load_dotenv
import os
import pytest
from playwright.sync_api import sync_playwright
from datetime import datetime
from pytest_html import extras

load_dotenv()  # Load from .env by default

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com/")

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chromium", help="Browser: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--headless", action="store_true", help="Run tests in headless mode"
    )
    parser.addoption(
        "--slowmo", action="store", default=0, type=int, help="Delay (ms) between actions"
    )
    parser.addoption(
        "--headed", action="store_true", help="Run browser in headed mode"
    )
    parser.addoption("--env", action="store", default="staging", help="Target environment: staging, qa, prod")
    parser.addoption("--device", action="store", default="desktop", help="Device type: desktop, mobile")
    parser.addoption("--locale", action="store", default="en-US", help="Locale/language code")

@pytest.fixture(scope="function")
def page(request):
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")
    slowmo = int(request.config.getoption("--slowmo"))

    trace_dir = os.path.join("reports", "traces")
    os.makedirs(trace_dir, exist_ok=True)

    headless_mode = not headed

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=headless_mode, slow_mo=slowmo)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True)
        page = context.new_page()
        console_logs = []

        # Capture console messages
        page.on("console", lambda msg: console_logs.append(f"[{msg.type.upper()}] {msg.text}"))

        yield page

        # After test: if failed, attach logs
        if request.node.rep_call.failed and console_logs:
            log_dir = os.path.join("reports", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"{request.node.name}.log")

            with open(log_file, "w") as f:
                f.write("\n".join(console_logs))

            request.node.extra.append(extras.text("\n".join(console_logs), name="Browser Console Logs"))

        trace_name = f"trace_{browser_name}_{request.node.name}.zip"
        context.tracing.stop(path=os.path.join(trace_dir, trace_name))

        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Trigger only on test failures during call phase
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page:
            # Create directories if needed
            screenshot_dir = os.path.join("reports", "screenshots")
            logs_dir = os.path.join("reports", "logs")
            os.makedirs(screenshot_dir, exist_ok=True)
            os.makedirs(logs_dir, exist_ok=True)

            # Generate unique file names
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/", "_").replace(" ", "_")
            screenshot_file = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            log_file = os.path.join(logs_dir, f"{test_name}_{timestamp}.log")

            # Capture screenshot
            page.screenshot(path=screenshot_file, full_page=True)
            if hasattr(report, "extra"):
                report.extra.append(extras.image(screenshot_file, mime_type="image/png"))

            # Capture browser console logs
            console_msgs = page.context.pages[0].evaluate("""
                () => {
                    return window._console_logs || []
                }
            """)
            if console_msgs:
                with open(log_file, "w") as f:
                    f.write("\n".join(console_msgs))
                report.extra.append(extras.text("\n".join(console_msgs), name="Browser Console Logs"))

def pytest_configure(config):
    if not config.option.htmlpath:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("reports", "html")
        os.makedirs(output_dir, exist_ok=True)
        config.option.htmlpath = os.path.join(output_dir, f"report_{ts}.html")

@pytest.fixture(scope="session")
def cli_context(request):
    return {
        "env": request.config.getoption("--env"),
        "device": request.config.getoption("--device"),
        "locale": request.config.getoption("--locale"),
    }