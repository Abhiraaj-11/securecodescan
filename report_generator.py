import json

from jinja2 import Environment
from jinja2 import FileSystemLoader

from metrics import (
    calculate_metrics,
    calculate_risk_score
)


def save_json_report(results):

    with open(
        "reports/report.json",
        "w"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


def generate_html_report(results):

    metrics = calculate_metrics(results)

    risk_score = calculate_risk_score(results)

    env = Environment(
        loader=FileSystemLoader(
            "templates"
        )
    )

    template = env.get_template(
        "report_template.html"
    )

    html = template.render(
        findings=results,
        metrics=metrics,
        risk_score=risk_score
    )

    with open(
        "reports/report.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)