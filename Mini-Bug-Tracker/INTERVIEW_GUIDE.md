# Interview Guide - Mini Bug Tracker

## Resume Bullets
- Built a Flask + SQLite bug tracking web app and wrote 10 manual test cases and 3 bug reports covering login, validation, bug creation, search and status updates.
- Automated 9 UI test scenarios (login, create bug, search/filter, update status) using Python, Selenium WebDriver and PyTest with explicit waits, fixtures and failure screenshots.
- Performed database validation with parameterized SQL (SELECT, INSERT, UPDATE, COUNT) on SQLite to verify UI actions were saved correctly; managed code with Git/GitHub.

## 30-Second Explanation (HR)
"I built a small bug tracking application using Python and Flask to practise software testing. A tester can log in, create bugs, search them and update their status. I tested it manually with 10 test cases and 3 bug reports, then automated the main flows with Selenium and PyTest. I also checked the SQLite database with SQL to confirm the data saved correctly. The project is on GitHub and helped me practise the full testing process from test design to automation."

## 1-Minute Technical Explanation
"The project is a Flask app with five pages: login, dashboard, create bug, bugs list with search and filter, and update bug. Data is stored in a SQLite `bugs` table, and all SQL is parameterized. For testing, I wrote 10 manual test cases and 3 bug reports. For automation, I used Selenium WebDriver with PyTest. `conftest.py` starts the Flask app on a test port with a temporary database, opens Chrome through a fixture, and closes it after each test. Tests use element IDs, `WebDriverWait` with expected conditions, and `assert` statements. After creating or updating a bug in the UI, the tests run a SELECT query on SQLite to validate the data. If a test fails, a screenshot is saved in the `screenshots` folder. There are 9 tests in total, run with `pytest -v`."

---

## 15 Interview Questions

### 1. Explain your project.
**Simple answer:** It is a small bug tracker built with Flask. I tested it manually and automated it with Selenium and PyTest, and I validated the data in SQLite.
**Deeper explanation:** The app is only a test target. My work was designing test cases, writing automation, reporting bugs and validating the database. I can walk through login, create bug, search, update and DB checks.

### 2. Why did you use Flask?
**Simple answer:** Flask is small and easy, so I could build a working app quickly and focus on testing.
**Deeper explanation:** Flask needs very little code for routes, templates and forms. It also runs locally, so Selenium can test it without any external website.

### 3. Why did you use Selenium?
**Simple answer:** Selenium automates a real browser, so it can click, type and check the page like a user.
**Deeper explanation:** It is widely used for web UI automation and supports Python. It replaces repeated manual clicking with repeatable regression tests.

### 4. Why PyTest?
**Simple answer:** PyTest has simple syntax, plain `assert`, and fixtures for setup and cleanup.
**Deeper explanation:** Tests are ordinary functions starting with `test_`. Fixtures in `conftest.py` start the server and the browser, and PyTest shows clear failure output. `pytest -v` runs everything.

### 5. How did you automate login?
**Simple answer:** I opened `/login`, typed the username and password using their IDs, clicked the Login button, then checked the URL and dashboard heading.
**Deeper explanation:** I used `By.ID` locators and `WebDriverWait` until the elements were visible. The valid-login test asserts `/dashboard` is in the URL. The invalid-login test asserts the error message "Invalid username or password" is shown.

### 6. How did you create a bug using Selenium?
**Simple answer:** I opened the create bug page, typed into the text fields, selected dropdown values, and clicked Submit.
**Deeper explanation:** I used `send_keys()` for text fields and Selenium's `Select` class for severity, priority and status. The steps live in a reusable fixture (`create_bug_via_ui`) and use a random title so every test has unique data.

### 7. How did you validate the database?
**Simple answer:** After creating a bug in the UI, I ran a SELECT query on SQLite with the bug title and asserted the record exists.
**Deeper explanation:** The `db_query` fixture connects to the same test database file that Flask uses. I check that exactly one row exists and that severity, priority, status and tester name match. After an update I check `status` is `Closed`.

### 8. What SQL queries did you use?
**Simple answer:** SELECT, INSERT, UPDATE and COUNT.
**Deeper explanation:**
```sql
SELECT * FROM bugs;
SELECT * FROM bugs WHERE status = 'Open';
SELECT * FROM bugs WHERE severity = 'High';
SELECT COUNT(*) FROM bugs;
UPDATE bugs SET status = 'Closed' WHERE id = ?;
```
The `?` placeholders are parameterized queries. They keep user input separate from SQL and help prevent SQL injection.

### 9. What is an assertion?
**Simple answer:** An assertion checks that something is true. If it is false, the test fails.
**Deeper explanation:** Example: `assert message.text == "Bug created successfully"`. Without assertions a test only performs steps and never verifies the expected result.

### 10. What is an explicit wait?
**Simple answer:** It waits for a specific condition, such as an element being visible, up to a maximum time.
**Deeper explanation:** `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))` continues as soon as the condition is true, so it is faster and more reliable than `time.sleep()`, which always waits a fixed time.

### 11. What is manual testing?
**Simple answer:** A person tests the application by hand, following test cases, without automation scripts.
**Deeper explanation:** It is good for new features, exploratory testing and usability. I wrote 10 manual test cases with ID, scenario, precondition, steps, expected result, actual result and status.

### 12. How did you write test cases?
**Simple answer:** I looked at each feature and wrote positive and negative scenarios with clear steps and expected results.
**Deeper explanation:** For login I covered valid, invalid, empty username and empty password. For bugs I covered creation, required-field validation, search and status updates. Good test cases have specific steps, test data and one clear expected result.

### 13. What is severity?
**Simple answer:** Severity is how badly a bug affects the application.
**Deeper explanation:** It is technical impact, usually Low, Medium, High or Critical. Example: a crash on login is High or Critical. A small spelling mistake is Low. The tester usually sets severity.

### 14. What is priority?
**Simple answer:** Priority is how soon the bug should be fixed.
**Deeper explanation:** It is a business decision. A bug can be low severity but high priority, like a spelling mistake in the company name on the home page. It can also be high severity but low priority if it happens in a rarely used feature.

### 15. Explain the complete project flow.
**Simple answer:** Design test cases, run manual tests, report bugs, automate the main flows with Selenium and PyTest, and validate data in SQLite.
**Deeper explanation:** For a run: `pytest -v` starts Flask on port 5001 with a temporary DB, opens Chrome, logs in, creates a bug, searches for it, updates its status, and checks the database. Failures save a screenshot. Everything is stored in Git and pushed to GitHub.
