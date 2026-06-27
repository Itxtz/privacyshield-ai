import re

import spacy

nlp = spacy.load(
    "en_core_web_sm"
)


EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"\b\d{10}\b"

AADHAAR_PATTERN = r"\b\d{4}\s?\d{4}\s?\d{4}\b"


def detect_pii(text: str):

    findings = []

    # Email Detection
    emails = re.findall(
        EMAIL_PATTERN,
        text
    )

    for email in emails:

        findings.append({
            "type": "EMAIL",
            "value": email
        })

    # Phone Detection
    phones = re.findall(
        PHONE_PATTERN,
        text
    )

    for phone in phones:

        findings.append({
            "type": "PHONE",
            "value": phone
        })

    # Aadhaar Detection
    aadhaar_numbers = re.findall(
        AADHAAR_PATTERN,
        text
    )

    for aadhaar in aadhaar_numbers:

        findings.append({
            "type": "AADHAAR",
            "value": aadhaar
        })

    # Named Entity Recognition

    doc = nlp(text)

    for ent in doc.ents:

        findings.append({
            "type": ent.label_,
            "value": ent.text
        })

    return findings