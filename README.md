# SecureCodeScan

SecureCodeScan is a Python static-analysis tool that scans a GitHub repository for potential security issues and creates reports. It can also use OpenRouter to generate a short remediation summary from the scan findings.

> Static analysis can miss vulnerabilities and report false positives. A clean scan is not proof that a repository is secure.

## Requirements

- Python 3.10 or newer
- Git installed and available on `PATH`
- An OpenRouter API key only if you want AI-generated recommendations

## Setup

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The AI recommendation feature is optional. To enable it, copy `.env.example` to `.env` and add your OpenRouter key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key
```

Alternatively, set `OPENROUTER_API_KEY` in your shell environment. Keep the real key private: `.env` is excluded by `.gitignore`; never commit or share it. If a key has already been committed or exposed, revoke it with OpenRouter and create a new one.

## Scan a repository from the command line

Pass the URL of a repository you are authorized to scan:

```powershell
python main.py https://github.com/OWNER/REPOSITORY
```

This command scans Python files and writes `reports/report.json` and `reports/report.html`. If configured, the AI recommendation is printed in the terminal.

## Use the dashboard

Start the local Flask dashboard:

```powershell
python dashboard/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), enter an authorized GitHub repository URL, and submit the form. The dashboard scan supports Python, JavaScript/TypeScript, Java, C/C++, Go, Ruby, PHP, HTML, CSS, JSON, Markdown, and Jupyter Notebook files. Its findings and optional AI recommendation are saved in `reports/report.json`.

The dashboard is intended for local development, not production deployment.

## Checks performed

The project includes scanners for:

- Hardcoded secrets
- SQL injection patterns
- Command injection patterns
- Risky cryptographic usage

The checks are heuristic and their coverage varies by language and pattern. Review findings in context and use additional testing and security review for important systems.

## Data and privacy

Repositories supplied for scanning are cloned locally under `cloned_repos/`. When an OpenRouter key is configured, scan finding summaries are sent to OpenRouter to generate recommendations. Do not submit code or findings that you are not permitted to share with that service.

## Project layout

- `main.py` — command-line scan entry point
- `dashboard/app.py` — local web dashboard
- `scanner/` — scanner implementations
- `reports/` — generated reports (ignored by Git)
- `cloned_repos/` — repositories cloned for scanning (ignored by Git)