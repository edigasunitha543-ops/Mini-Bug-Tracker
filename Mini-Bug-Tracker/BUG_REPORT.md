# Bug Report - Mini Bug Tracker

These are sample bugs/observations found while testing the demo application.

**Environment (all bugs):** Windows 11, Google Chrome, Flask app at http://127.0.0.1:5000, SQLite database

---

## BUG-001

| Field | Details |
|---|---|
| **Bug ID** | BUG-001 |
| **Title** | Username on the login page is case-sensitive |
| **Environment** | Windows 11, Chrome, local Flask app |
| **Steps to Reproduce** | 1. Open `/login`<br>2. Enter username `Tester` (capital T)<br>3. Enter password `tester123`<br>4. Click **Login** |
| **Expected Result** | Login succeeds because the username is the same apart from letter case (or the case rule is clearly shown to the user) |
| **Actual Result** | "Invalid username or password" is shown |
| **Severity** | Low |
| **Priority** | Low |
| **Status** | Open |

---

## BUG-002

| Field | Details |
|---|---|
| **Bug ID** | BUG-002 |
| **Title** | A very long bug title without spaces stretches the Bugs table |
| **Environment** | Windows 11, Chrome, local Flask app |
| **Steps to Reproduce** | 1. Log in<br>2. Open **Create Bug**<br>3. Enter a title of about 150 characters with no spaces (for example `AAAA...`)<br>4. Fill the other fields and click **Submit Bug**<br>5. Look at the Bugs table |
| **Expected Result** | Long text wraps or is shortened so the table stays inside the page |
| **Actual Result** | The Title column becomes very wide and the table goes beyond the page width |
| **Severity** | Low |
| **Priority** | Medium |
| **Status** | Open |

---

## BUG-003

| Field | Details |
|---|---|
| **Bug ID** | BUG-003 |
| **Title** | A Closed bug can be changed back to another status without any warning |
| **Environment** | Windows 11, Chrome, local Flask app |
| **Steps to Reproduce** | 1. Log in<br>2. Open **View Bugs**<br>3. Click **Update** on a bug whose status is "Closed"<br>4. Select "Open"<br>5. Click **Update Status** |
| **Expected Result** | The user sees a confirmation or a clear reopen rule before a closed bug is changed |
| **Actual Result** | The status changes to "Open" immediately with only the normal success message |
| **Severity** | Medium |
| **Priority** | Medium |
| **Status** | Open |
