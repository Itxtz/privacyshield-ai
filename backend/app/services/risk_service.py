RISK_WEIGHTS = {

    "EMAIL": 10,

    "PHONE": 10,

    "AADHAAR": 40,

    "PERSON": 5,

    "GPE": 5,

    "ORG": 5,

    "CREDIT_CARD": 50,

    "PAN": 30
}


def calculate_risk(findings):

    score = 0

    reasons = []

    for finding in findings:

        pii_type = finding["type"]

        weight = RISK_WEIGHTS.get(
            pii_type,
            0
        )

        score += weight

        if weight > 0:

            reasons.append(
                f"{pii_type} detected"
            )

    if score < 20:

        level = "LOW"

    elif score < 50:

        level = "MEDIUM"

    else:

        level = "HIGH"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }