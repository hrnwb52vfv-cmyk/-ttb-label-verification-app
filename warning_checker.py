import re

STANDARD_WARNING_KEY_PHRASES = [
    "GOVERNMENT WARNING",
    "according to the surgeon general",
    "women should not drink alcoholic beverages during pregnancy",
    "impairs your ability to drive a car or operate machinery",
    "may cause health problems",
]


def normalize_text(text):
    text = text or ""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def check_warning(text):
    """Check for the required government health warning statement.

    The heading is intentionally checked strictly in uppercase because stakeholders
    identified this as a common rejection issue.
    """
    normalized = normalize_text(text)
    lower_text = normalized.lower()

    has_uppercase_heading = "GOVERNMENT WARNING" in normalized
    phrase_matches = sum(1 for phrase in STANDARD_WARNING_KEY_PHRASES if phrase.lower() in lower_text)

    return {
        "passed": has_uppercase_heading and phrase_matches >= 4,
        "has_uppercase_heading": has_uppercase_heading,
        "matched_warning_phrases": phrase_matches,
        "required_warning_phrase_count": len(STANDARD_WARNING_KEY_PHRASES),
        "message": "Government warning appears compliant." if has_uppercase_heading and phrase_matches >= 4 else "Government warning may be missing, incomplete, or incorrectly formatted.",
    }
