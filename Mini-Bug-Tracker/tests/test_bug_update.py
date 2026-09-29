from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def open_update_page_for(driver, wait, title):
    """Search for a bug by title on the bugs page and click its Update link."""
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "search-input")))
    search_box.clear()
    search_box.send_keys(title)
    driver.find_element(By.ID, "search-button").click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "tr.bug-row a.update-link"))).click()
    wait.until(EC.url_contains("/update-bug/"))


def test_tc06_update_bug_status(logged_in_browser, create_bug_via_ui, wait):
    """TC06 - Update a bug from Open to Closed."""
    title = create_bug_via_ui(status="Open")
    wait.until(EC.url_contains("/bugs"))
    open_update_page_for(logged_in_browser, wait, title)

    assert logged_in_browser.find_element(By.ID, "current-status").text == "Open"
    Select(logged_in_browser.find_element(By.ID, "status")).select_by_visible_text("Closed")
    logged_in_browser.find_element(By.ID, "update-button").click()

    message = wait.until(EC.visibility_of_element_located((By.ID, "flash-message")))
    assert message.text == "Bug status updated successfully"


def test_tc07_validate_updated_bug(logged_in_browser, create_bug_via_ui, wait, db_query):
    """TC07 - The updated status is visible in the UI and saved in the database."""
    title = create_bug_via_ui(status="Open")
    wait.until(EC.url_contains("/bugs"))
    open_update_page_for(logged_in_browser, wait, title)

    Select(logged_in_browser.find_element(By.ID, "status")).select_by_visible_text("Closed")
    logged_in_browser.find_element(By.ID, "update-button").click()
    wait.until(EC.url_contains("/bugs"))

    # UI validation
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "search-input")))
    search_box.send_keys(title)
    logged_in_browser.find_element(By.ID, "search-button").click()
    status_cell = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.bug-row .bug-status")))
    assert status_cell.text == "Closed"

    # Database validation
    rows = db_query("SELECT status FROM bugs WHERE title = ?", (title,))
    assert len(rows) == 1
    assert rows[0]["status"] == "Closed"
