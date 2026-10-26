SEVERITY_SCORE = {

    "CRITICAL": 10,

    "HIGH": 7,

    "MEDIUM": 4,

    "LOW": 1
}


def calculate_metrics(results):

    metrics = {

        "CRITICAL": 0,

        "HIGH": 0,

        "MEDIUM": 0,

        "LOW": 0
    }

    for finding in results:

        metrics[
            finding["severity"]
        ] += 1

    return metrics


def calculate_risk_score(results):

    score = 0

    for finding in results:

        score += SEVERITY_SCORE[
            finding["severity"]
        ]

    return score