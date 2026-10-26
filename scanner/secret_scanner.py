import re

SECRET_PATTERNS = [
    r"api[_-]?key\s*=\s*['\"]\w+['\"]",
    r"secret\s*=\s*['\"]\w+['\"]",
    r"password\s*=\s*['\"]\w+['\"]",
    r"token\s*=\s*['\"]\w+['\"]"
]


def scan(file_path):
    findings = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        for i, line in enumerate(content.split("\n"), 1):
            for pattern in SECRET_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        "type": "Hardcoded Secret",
                        "severity": "HIGH",
                        "file": file_path,
                        "line": i
                    })

    except:
        pass

    return findings