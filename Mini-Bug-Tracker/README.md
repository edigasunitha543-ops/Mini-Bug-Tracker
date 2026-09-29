# Mini Bug Tracking & Test Case Management System

A small Flask web application built as a **QA / Automation Testing portfolio project**. It is used to practise manual testing, Selenium automation with PyTest, and database validation with SQL.

## Project Overview
The app is a simple bug tracker. A tester logs in, creates bugs, searches them and updates their status. The application is intentionally small so that the focus stays on **testing**, not on building a production system.

## Objective
Demonstrate the following fresher-level skills:
- Manual test case design and bug reporting
- Selenium WebDriver automation with Python and PyTest
- Database validation using SQL and SQLite
- Git/GitHub for version control

## Features
- Demo login (`tester` / `tester123`)
- Dashboard with bug counts by status
- Create bug (title, description, severity, priority, status, tester name)
- View, search and filter bugs (by title, status and severity)
- Update bug status
- Simple validation and success/error messages

## Technologies
Python 3, Flask, Selenium WebDriver, PyTest, SQLite, SQL, HTML/CSS, Git/GitHub

## Application Flow
```
Login -> Dashboard -> Create Bug -> Bugs list (success message)
                                         |
                              Search / Filter -> Update Bug Status -> Bugs list
```

| URL | Purpose |
|---|---|
| `/login` | Demo login |
| `/dashboard` | Bug counts and shortcuts |
| `/create-bug` | Create a new bug |
| `/bugs` | View, search and filter bugs |
| `/update-bug/<id>` | Update the status of one bug |

## Manual Testing
- `MANUAL_TEST_CASES.md` - 10 manual test cases (login, validation, create, search, update, close)
- `BUG_REPORT.md` - 3 sample bug reports

## Automation Testing
Selenium + PyTest tests in `tests/`:

| Test | Scenario |
|---|---|
| TC01 | Valid login |
| TC02 | Invalid login |
| TC03 | Create new bug |
| TC04 | Validate success message |
| TC05 | Search / view created bug (plus a severity filter test) |
| TC06 | Update bug status |
| TC07 | Validate updated bug (UI + database) |
| TC08 | Database validation |

Key points: explicit waits (`WebDriverWait`), `assert` statements, a browser fixture in `conftest.py`, and automatic screenshots on failure in `screenshots/`.

## Database Testing
After a bug is created or updated through the browser, the tests query SQLite directly (with parameterized SQL) and check that the record exists and has the correct values.
The tests use a temporary database, so your real `database/bug_tracker.db` is never changed by test runs.

## Project Structure
```
Mini-Bug-Tracker/
├── app.py                  # Flask routes
├── database.py             # SQLite helper functions (SQL)
├── requirements.txt
├── pytest.ini
├── conftest.py             # Fixtures: Flask server, browser, DB helper, screenshots
├── templates/              # HTML pages
├── static/style.css
├── tests/
│   ├── test_login.py
│   ├── test_bug_creation.py
│   └── test_bug_update.py
├── database/               # bug_tracker.db is created here automatically
├── screenshots/            # failure screenshots
├── MANUAL_TEST_CASES.md
├── BUG_REPORT.md
├── INTERVIEW_GUIDE.md
└── README.md
```

## Installation
Requirements: Python 3.9+ and Google Chrome (Selenium 4 downloads the matching driver automatically).

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## How to Start the Flask Application
```bash
python app.py
```
Open http://127.0.0.1:5000 and log in with `tester` / `tester123`.
The database file `database/bug_tracker.db` is created automatically.

## How to Run Selenium Tests
You do **not** need to start Flask first. The tests start their own Flask server on port 5001.

```bash
pytest -v              # headless Chrome
pytest -v --headed     # watch the browser
pytest tests/test_login.py -v
```

## SQL Validation
Open the database with the SQLite shell or DB Browser for SQLite:

```sql
SELECT * FROM bugs;
SELECT * FROM bugs WHERE status = 'Open';
SELECT * FROM bugs WHERE severity = 'High';
SELECT COUNT(*) FROM bugs;
UPDATE bugs SET status = 'Closed' WHERE id = 1;
```
The application code uses the parameterized form, for example `UPDATE bugs SET status = ? WHERE id = ?`.

## Sample Output (expected result of `pytest -v`)
```
tests/test_bug_creation.py::test_tc03_create_new_bug PASSED
tests/test_bug_creation.py::test_tc04_validate_success_message PASSED
tests/test_bug_creation.py::test_tc05_search_and_view_created_bug PASSED
tests/test_bug_creation.py::test_tc05b_filter_by_severity PASSED
tests/test_bug_creation.py::test_tc08_database_validation PASSED
tests/test_bug_update.py::test_tc06_update_bug_status PASSED
tests/test_bug_update.py::test_tc07_validate_updated_bug PASSED
tests/test_login.py::test_tc01_valid_login PASSED
tests/test_login.py::test_tc02_invalid_login PASSED

9 passed
```

## Future Enhancements
- Page Object Model for the Selenium tests
- HTML test report (pytest-html)
- Edit and delete bug features
- Run tests in GitHub Actions
- API tests for the Flask routes
