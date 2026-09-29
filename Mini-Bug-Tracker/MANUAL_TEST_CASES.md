# Manual Test Cases - Mini Bug Tracker

**Application URL:** http://127.0.0.1:5000
**Test data:** Username `tester` / Password `tester123`
**Browser:** Google Chrome

> Re-execute each case yourself and update the Actual Result / Status columns with your own observations.

| Test Case ID | Test Scenario | Precondition | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC_MAN_01 | Valid Login | Flask app is running; user is logged out | 1. Open `/login`<br>2. Enter username `tester`<br>3. Enter password `tester123`<br>4. Click **Login** | User is redirected to `/dashboard` and the "Bug Dashboard" heading is shown | Dashboard opened with the heading "Bug Dashboard" | Pass |
| TC_MAN_02 | Invalid Login | Flask app is running | 1. Open `/login`<br>2. Enter username `tester`<br>3. Enter password `wrong123`<br>4. Click **Login** | Error "Invalid username or password" is shown; user stays on the login page | Error message shown; login page remained | Pass |
| TC_MAN_03 | Empty Username | Flask app is running | 1. Open `/login`<br>2. Leave username empty<br>3. Enter password `tester123`<br>4. Click **Login** | Error "Username and password are required" is shown | Error message shown | Pass |
| TC_MAN_04 | Empty Password | Flask app is running | 1. Open `/login`<br>2. Enter username `tester`<br>3. Leave password empty<br>4. Click **Login** | Error "Username and password are required" is shown | Error message shown | Pass |
| TC_MAN_05 | Create Bug | User is logged in | 1. Click **Create Bug**<br>2. Fill Title, Description, Severity, Priority, Status, Tester Name<br>3. Click **Submit Bug** | Message "Bug created successfully" is shown and the bug appears at the top of the Bugs list | Success message shown; new bug listed in the table | Pass |
| TC_MAN_06 | Required Field Validation | User is logged in | 1. Open **Create Bug**<br>2. Leave the Title empty and fill the other fields<br>3. Click **Submit Bug** | Error "All fields are required" is shown and no bug is saved | Error shown; bug count did not change | Pass |
| TC_MAN_07 | High Severity Bug | User is logged in | 1. Open **Create Bug**<br>2. Fill all fields and select Severity = High<br>3. Submit<br>4. On the Bugs page, set the Severity filter to High and click **Search** | The new bug is listed with Severity "High" | Bug listed with Severity "High" | Pass |
| TC_MAN_08 | Search Bug | At least one bug exists | 1. Open **View Bugs**<br>2. Type part of a bug title in the search box<br>3. Click **Search** | Only bugs whose title contains the text are listed | Only matching bugs were listed | Pass |
| TC_MAN_09 | Update Bug Status | A bug with status "Open" exists | 1. Open **View Bugs**<br>2. Click **Update** on the bug<br>3. Select "In Progress"<br>4. Click **Update Status** | Message "Bug status updated successfully"; status shows "In Progress" in the list | Message shown; status changed to "In Progress" | Pass |
| TC_MAN_10 | Close Bug | A bug with status "In Progress" exists | 1. Open **View Bugs**<br>2. Click **Update** on the bug<br>3. Select "Closed"<br>4. Click **Update Status**<br>5. Open the Dashboard | Status shows "Closed" in the list and the Dashboard "Closed" count increases by 1 | Status changed to "Closed"; Dashboard count increased | Pass |
