"""Shared PyTest fixtures: Flask server, browser, database helper, and failure screenshots."""
import os
import re
import sqlite3
import tempfile
import threading
import uuid
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

PORT = 5001
BASE_URL = f"http://127.0.0.1:{PORT}"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(PROJECT_DIR, "screenshots")

VALID_USERNAME = "tester"
VALID_PASSWORD = "tester123"


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", default=False,
                     help="Run Chrome with a visible window (default is headless)")


@pytest.fixture(scope="session")
def db_path():
    """A temporary SQLite file so tests never touch the real database."""
    folder = tempfile.mkdtemp()
    return os.path.join(folder, "test_bug_tracker.db")


@pytest.fixture(scope="session")
def flask_server(db_path):
    """Start the Flask app in a background thread for the whole test session."""
    os.environ["BUG_TRACKER_DB"] = db_path
    from werkzeug.serving import make_server

    import app as app_module  # imported after the env variable is set

    server = make_server("127.0.0.1", PORT, app_module.app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield BASE_URL
    server.shutdown()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store each test result on the test item so fixtures can check if the test failed."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture
def browser(request, flask_server):
    """Start Chrome, open the app, run the test, then close Chrome."""
    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    driver.get(flask_server)
    yield driver

    # Screenshot on failure
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", request.node.name)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, f"{safe_name}_{stamp}.png"))
    driver.quit()


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)


@pytest.fixture
def login(browser, wait):
    """Return a function that logs in through the UI."""
    def _login(username=VALID_USERNAME, password=VALID_PASSWORD):
        browser.get(BASE_URL + "/login")
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(username)
        browser.find_element(By.ID, "password").send_keys(password)
        browser.find_element(By.ID, "login-button").click()
    return _login


@pytest.fixture
def logged_in_browser(browser, login, wait):
    """A browser that is already logged in and on the dashboard."""
    login()
    wait.until(EC.url_contains("/dashboard"))
    return browser


@pytest.fixture
def create_bug_via_ui(logged_in_browser, wait):
    """Return a function that fills and submits the Create Bug form through the UI."""
    def _create(title=None, severity="High", priority="High", status="Open",
                tester_name="Test Fresher"):
        title = title or f"Sample bug {uuid.uuid4().hex[:8]}"
        driver = logged_in_browser
        driver.get(BASE_URL + "/create-bug")
        wait.until(EC.visibility_of_element_located((By.ID, "title"))).send_keys(title)
        driver.find_element(By.ID, "description").send_keys("Created by Selenium test")
        Select(driver.find_element(By.ID, "severity")).select_by_visible_text(severity)
        Select(driver.find_element(By.ID, "priority")).select_by_visible_text(priority)
        Select(driver.find_element(By.ID, "status")).select_by_visible_text(status)
        driver.find_element(By.ID, "tester_name").send_keys(tester_name)
        driver.find_element(By.ID, "submit-bug").click()
        return title
    return _create


@pytest.fixture
def db_query(db_path):
    """Return a function that runs a parameterized SELECT on the test database."""
    def _query(sql, params=()):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return rows
    return _query
