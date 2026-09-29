from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_tc01_valid_login(browser, login, wait):
    """TC01 - Valid login opens the dashboard."""
    login("tester", "tester123")
    wait.until(EC.url_contains("/dashboard"))
    heading = wait.until(EC.visibility_of_element_located((By.ID, "dashboard-heading")))
    assert "/dashboard" in browser.current_url
    assert heading.text == "Bug Dashboard"


def test_tc02_invalid_login(browser, login, wait):
    """TC02 - Invalid login shows an error and stays on the login page."""
    login("tester", "wrong-password")
    error = wait.until(EC.visibility_of_element_located((By.ID, "error-message")))
    assert error.text == "Invalid username or password"
    assert "/login" in browser.current_url
