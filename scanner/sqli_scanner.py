import re

SQLI_PATTERNS = [
    r"execute\(.+\+.+\)",
    r"SELECT .+\+",
    r"INSERT .+\+",
    r"cursor\.execute\(.+%s.+\)"
]


def scan(file_path):
    findings = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        for i, line in enumerate(content.split("\n"), 1):
            for pattern in SQLI_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        "type": "SQL Injection",
                        "severity": "CRITICAL",
                        "file": file_path,
                        "line": i
                    })

    except:
        pass

    return findings