from flask import Flask, render_template, request, redirect, url_for
import json
import os
import sys
import threading

# -------------------------
# PATH SETUP (IMPORTANT)
# -------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

from run_scan import run


app = Flask(__name__)

REPORT_PATH = os.path.join(
    BASE_DIR,
    "reports",
    "report.json"
)


# -------------------------
# SCORING SYSTEM
# -------------------------
SEVERITY_SCORE = {
    "CRITICAL": 10,
    "HIGH": 7,
    "MEDIUM": 4,
    "LOW": 1
}


# -------------------------
# LOAD REPORT
# -------------------------
def load_report_data():

    if not os.path.exists(REPORT_PATH):
        return {
            "findings": [],
            "ai_recommendation": None
        }

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return {
            "findings": data.get("findings", []),
            "ai_recommendation": data.get("ai_recommendation")
        }

    return {
        "findings": data,
        "ai_recommendation": None
    }


# -------------------------
# METRICS
# -------------------------
def get_metrics(findings):

    metrics = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for f in findings:
        metrics[f.get("severity", "LOW")] += 1

    return metrics


def calculate_risk_score(findings):

    score = 0

    for f in findings:
        score += SEVERITY_SCORE.get(
            f.get("severity", "LOW"),
            0
        )

    return score


# -------------------------
# DASHBOARD ROUTE
# -------------------------
@app.route("/")
def dashboard():

    report_data = load_report_data()
    findings = report_data["findings"]
    recommendation = report_data["ai_recommendation"]

    return render_template(
        "dashboard.html",
        findings=findings,
        metrics=get_metrics(findings),
        risk_score=calculate_risk_score(findings),
        ai_recommendation=recommendation
    )


# -------------------------
# SCAN STATE
# -------------------------
scan_status = {"running": False, "done": False}


def _run_scan(repo_url):
    scan_status["running"] = True
    scan_status["done"] = False
    try:
        run(repo_url)
    finally:
        scan_status["running"] = False
        scan_status["done"] = True


# -------------------------
# RUN SCAN ROUTE
# -------------------------
@app.route("/scan", methods=["POST"])
def scan_repo():

    repo_url = request.form.get("repo_url")

    if not repo_url:
        return redirect(url_for("dashboard"))

    if scan_status["running"]:
        # Don't launch a second scan while one is already running
        return redirect(url_for("dashboard"))

    print(f"[+] Scanning: {repo_url}")

    # Run scan in a background thread so Flask doesn't time out and
    # so a watchdog reload can't kill the scan mid-way.
    t = threading.Thread(target=_run_scan, args=(repo_url,), daemon=True)
    t.start()
    t.join()  # wait for completion before redirecting

    return redirect(url_for("dashboard"))


# -------------------------
# START APP
# -------------------------
if __name__ == "__main__":

    # Exclude cloned_repos from the watchdog file watcher so that
    # newly cloned .py files don't trigger a mid-scan server reload.
    cloned_repos_dir = os.path.join(BASE_DIR, "cloned_repos")

    app.run(
        debug=True,
        port=5000,
        exclude_patterns=[
            os.path.join(cloned_repos_dir, "*"),
            os.path.join(cloned_repos_dir, "**", "*"),
        ]
    )