"""Mini Bug Tracker - a small Flask app used for practising QA and Selenium automation."""
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import database

app = Flask(__name__)
app.secret_key = "demo-secret-key-for-learning-only"

DEMO_USERNAME = "tester"
DEMO_PASSWORD = "tester123"

SEVERITIES = ["Low", "Medium", "High", "Critical"]
PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

database.init_db()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Username and password are required"
        elif username == DEMO_USERNAME and password == DEMO_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    counts = {
        "total": database.count_bugs(),
        "open": database.count_bugs("Open"),
        "in_progress": database.count_bugs("In Progress"),
        "resolved": database.count_bugs("Resolved"),
        "closed": database.count_bugs("Closed"),
    }
    return render_template("dashboard.html", counts=counts)


@app.route("/create-bug", methods=["GET", "POST"])
@login_required
def create_bug():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        severity = request.form.get("severity", "")
        priority = request.form.get("priority", "")
        status = request.form.get("status", "")
        tester_name = request.form.get("tester_name", "").strip()

        if not all([title, description, severity, priority, status, tester_name]):
            error = "All fields are required"
        else:
            database.insert_bug(title, description, severity, priority, status, tester_name)
            flash("Bug created successfully", "success")
            return redirect(url_for("bugs"))
    return render_template(
        "create_bug.html", error=error, severities=SEVERITIES, priorities=PRIORITIES, statuses=STATUSES
    )


@app.route("/bugs")
@login_required
def bugs():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "")
    severity = request.args.get("severity", "")
    rows = database.get_bugs(search, status, severity)
    return render_template(
        "bugs.html", bugs=rows, search=search, selected_status=status,
        selected_severity=severity, severities=SEVERITIES, statuses=STATUSES,
    )


@app.route("/update-bug/<int:bug_id>", methods=["GET", "POST"])
@login_required
def update_bug(bug_id):
    bug = database.get_bug_by_id(bug_id)
    if bug is None:
        flash("Bug not found", "error")
        return redirect(url_for("bugs"))
    if request.method == "POST":
        new_status = request.form.get("status", "")
        if new_status not in STATUSES:
            flash("Invalid status", "error")
            return redirect(url_for("update_bug", bug_id=bug_id))
        database.update_bug_status(bug_id, new_status)
        flash("Bug status updated successfully", "success")
        return redirect(url_for("bugs"))
    return render_template("update_bug.html", bug=bug, statuses=STATUSES)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
