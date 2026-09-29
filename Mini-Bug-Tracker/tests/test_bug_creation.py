from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def test_tc03_create_new_bug(logged_in_browser, create_bug_via_ui, wait):
    """TC03 - A new bug can be created and the user lands on the bugs page."""
    title = create_bug_via_ui()
    wait.until(EC.url_contains("/bugs"))
    assert "/bugs" in logged_in_browser.current_url
    assert title in logged_in_browser.page_source


def test_tc04_validate_success_message(logged_in_browser, create_bug_via_ui, wait):
    """TC04 - The success message is shown after creating a bug."""
    create_bug_via_ui()
    message = wait.until(EC.visibility_of_element_located((By.ID, "flash-message")))
    assert message.text == "Bug created successfully"


def test_tc05_search_and_view_created_bug(logged_in_browser, create_bug_via_ui, wait):
    """TC05 - The created bug can be found using the search box."""
    title = create_bug_via_ui()
    wait.until(EC.url_contains("/bugs"))

    search_box = wait.until(EC.visibility_of_element_located((By.ID, "search-input")))
    search_box.send_keys(title)
    logged_in_browser.find_element(By.ID, "search-button").click()

    first_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.bug-row .bug-title")))
    rows = logged_in_browser.find_elements(By.CSS_SELECTOR, "tr.bug-row")
    assert len(rows) == 1
    assert first_title.text == title
    assert logged_in_browser.find_element(By.CSS_SELECTOR, "tr.bug-row .bug-severity").text == "High"


def test_tc05b_filter_by_severity(logged_in_browser, create_bug_via_ui, wait):
    """Extra - Filtering by severity only shows bugs with that severity."""
    create_bug_via_ui(severity="Critical")
    wait.until(EC.url_contains("/bugs"))
    Select(wait.until(EC.visibility_of_element_located((By.ID, "filter-severity")))).select_by_visible_text("Critical")
    logged_in_browser.find_element(By.ID, "search-button").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr.bug-row")))
    severities = [e.text for e in logged_in_browser.find_elements(By.CSS_SELECTOR, "tr.bug-row .bug-severity")]
    assert severities and all(s == "Critical" for s in severities)


def test_tc08_database_validation(logged_in_browser, create_bug_via_ui, wait, db_query):
    """TC08 - The bug created in the UI exists in SQLite with the correct values."""
    title = create_bug_via_ui(severity="High", priority="Medium", status="Open", tester_name="Asha")
    wait.until(EC.url_contains("/bugs"))

    rows = db_query("SELECT * FROM bugs WHERE title = ?", (title,))
    assert len(rows) == 1
    bug = rows[0]
    assert bug["severity"] == "High"
    assert bug["priority"] == "Medium"
    assert bug["status"] == "Open"
    assert bug["tester_name"] == "Asha"
    assert bug["description"] == "Created by Selenium test"
