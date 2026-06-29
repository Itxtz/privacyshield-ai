import re


EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"\b\d{10}\b"

AADHAAR_PATTERN = r"\b\d{4}\s?\d{4}\s?\d{4}\b"



def mask_email(email):

    parts = email.split("@")

    username = parts[0]
    domain = parts[1]

    if len(username) <= 2:
        masked_username = "*" * len(username)

    else:
        masked_username = (
            username[:2]
            + "*" * (len(username) - 2)
        )

    return f"{masked_username}@{domain}"


def mask_phone(phone):

    if len(phone) < 4:
        return "*" * len(phone)

    return (
        phone[:2]
        + "*" * (len(phone) - 4)
        + phone[-2:]
    )


def mask_aadhaar(aadhaar):

    digits = aadhaar.replace(" ", "")

    return (
        digits[:2]
        + "*" * 8
        + digits[-2:]
    )

def redact_text(text: str):

    redaction_summary = []

    # Email
    emails = re.findall(
        EMAIL_PATTERN,
        text
    )

    for email in emails:

        masked_email = mask_email(email)
        text = text.replace(
            email,
            masked_email
        )

        redaction_summary.append(
            f"EMAIL redacted: {email}"
        )

    # Phone
    phones = re.findall(
        PHONE_PATTERN,
        text
    )

    for phone in phones:

        masked_phone = mask_phone(phone)
        text = text.replace(
            phone,
            masked_phone
        )

        redaction_summary.append(
            f"PHONE redacted: {phone}"
        )

    # Aadhaar
    aadhaars = re.findall(
        AADHAAR_PATTERN,
        text
    )

    for aadhaar in aadhaars:

        masked_aadhaar = mask_aadhaar(aadhaar)
        text = text.replace(
            aadhaar,
            masked_aadhaar
        )

        redaction_summary.append(
            f"AADHAAR redacted: {aadhaar}"
        )

    return {
        "redacted_text": text,
        "summary": redaction_summary
    }