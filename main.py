import sys

from scanner.secret_scanner import scan as secret_scan
from scanner.sqli_scanner import scan as sqli_scan
from scanner.command_scanner import scan as command_scan
from scanner.crypto_scanner import scan as crypto_scan

from scanner.repo_scanner import (
    clone_repository,
    get_python_files
)

from report_generator import (
    save_json_report,
    generate_html_report
)

from ai_recommender import get_ai_recommendation


def main():

    if len(sys.argv) != 2:

        print(
            "Usage: python main.py <github_repo_url>"
        )

        return

    repo_url = sys.argv[1]

    repo_path = clone_repository(
        repo_url
    )

    python_files = get_python_files(
        repo_path
    )

    print(
        f"[+] Found {len(python_files)} Python files"
    )

    results = []

    for file in python_files:

        results.extend(
            secret_scan(file)
        )

        results.extend(
            sqli_scan(file)
        )

        results.extend(
            command_scan(file)
        )

        results.extend(
            crypto_scan(file)
        )

    save_json_report(results)

    generate_html_report(results)

    recommendation = get_ai_recommendation(results)
    print("[+] AI recommendation:")
    print(recommendation)

    print(
        f"[+] Findings: {len(results)}"
    )

    print(
        "[+] Report Generated"
    )


if __name__ == "__main__":
    main()