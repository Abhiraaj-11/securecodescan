from scanner.repo_scanner import (
    clone_repository,
    get_all_files
)

from scanner.engines.python_ast_engine import scan_python_file
from scanner.secret_scanner import scan as secret_scan
from scanner.sqli_scanner import scan as sqli_scan
from scanner.command_scanner import scan as command_scan
from scanner.crypto_scanner import scan as crypto_scan

import os
import json

from ai_recommender import get_ai_recommendation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def save_json_report(results, recommendation=None):

    report_path = os.path.join(BASE_DIR, "reports", "report.json")

    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    payload = {
        "findings": results
    }

    if recommendation is not None:
        payload["ai_recommendation"] = recommendation

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)


# -------------------------
# CORE ENGINE
# -------------------------
def run(repo_url):

    print("[+] Cloning repository...")

    repo_path = clone_repository(repo_url)

    print("[+] Scanning files...")

    files = get_all_files(repo_path)

    print(f"[+] Total files: {len(files)}")

    results = []

    for file in files:
        ext = file.split(".")[-1].lower()

        if ext == "py":
            results.extend(scan_python_file(file))
        else:
            results.extend(secret_scan(file))
            results.extend(sqli_scan(file))
            results.extend(command_scan(file))
            results.extend(crypto_scan(file))

    print(f"[+] Total findings: {len(results)}")

    recommendation = get_ai_recommendation(results)
    print("[+] AI recommendation generated")

    save_json_report(results, recommendation)

    return results, recommendation