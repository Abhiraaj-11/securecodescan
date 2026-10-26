import re

PATTERNS = [

    r"md5\(",

    r"sha1\("
]


def scan(file_path):

    findings = []

    try:

        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            lines = file.readlines()

        for line_no, line in enumerate(lines, start=1):

            for pattern in PATTERNS:

                if re.search(
                    pattern,
                    line
                ):

                    findings.append({

                        "type": "Weak Cryptography",

                        "severity": "MEDIUM",

                        "file": file_path,

                        "line": line_no,

                        "code": line.strip()
                    })

    except Exception:

        pass

    return findings