import os
from dotenv import load_dotenv

load_dotenv()
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# MODEL = "google/gemma-4-31b-it:free"
MODEL = "google/gemma-4-26b-a4b-it:free"


def build_prompt(findings):
    if not findings:
        return (
            "The scan found no security vulnerabilities. "
            "Reply with a short positive confirmation that the code passed the security scan. "
            "Use a friendly one-sentence response."
        )

    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for finding in findings:
        counts[finding.get("severity", "LOW").upper()] += 1

    example_lines = []
    for finding in findings[:10]:
        example_lines.append(
            f"- {finding.get('type')} in {finding.get('file')} at line {finding.get('line')} "
            f"(severity: {finding.get('severity')})"
        )

    details = "\n".join(example_lines)
    return (
        "You are a security assistant that reads static scan findings and returns a short remediation summary. "
        "Explain how to fix the detected issues in two or three sentences. "
        "If the scan results are clean, return a brief positive confirmation. "
        "Use simple language and avoid long explanations.\n\n"
        f"Summary:\n"
        f"Critical: {counts['CRITICAL']}, High: {counts['HIGH']}, Medium: {counts['MEDIUM']}, Low: {counts['LOW']}\n"
        f"Findings:\n{details}"
    )


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_ai_recommendation(findings):
    api_key = OPENROUTER_API_KEY
    if not api_key:
        return (
            "AI recommendation unavailable. Please set OPENROUTER_API_KEY in the environment or create a .env file with OPENROUTER_API_KEY=."
        )

    prompt = build_prompt(findings)
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "reasoning": {"enabled": True}
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        message = data.get("choices", [{}])[0].get("message", {}).get("content")
        if not message:
            return "AI recommendation returned no content."
        return message.strip()
    except Exception as exc:
        return f"AI recommendation unavailable: {exc}"
