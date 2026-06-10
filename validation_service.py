import re
from rapidfuzz import fuzz
from services.warning_checker import check_warning


def normalize_text(value):
    value = value or ""
    value = value.upper()
    value = re.sub(r"[^A-Z0-9.%/ ]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def fuzzy_field_check(label_text, expected_value, threshold=85):
    if not expected_value:
        return {
            "status": "not_provided",
            "passed": False,
            "score": 0,
            "message": "No application value was provided.",
        }

    normalized_label = normalize_text(label_text)
    normalized_expected = normalize_text(expected_value)

    if normalized_expected in normalized_label:
        return {
            "status": "match",
            "passed": True,
            "score": 100,
            "message": "Exact or normalized match found on label.",
        }

    score = fuzz.partial_ratio(normalized_expected, normalized_label)
    return {
        "status": "match" if score >= threshold else "mismatch",
        "passed": score >= threshold,
        "score": round(score, 1),
        "message": "Likely match found with minor differences." if score >= threshold else "Expected value was not clearly found on the label.",
    }


def validate_label(extracted_text, application_data):
    brand_result = fuzzy_field_check(extracted_text, application_data.get("brand_name"), threshold=82)
    class_type_result = fuzzy_field_check(extracted_text, application_data.get("class_type"), threshold=80)
    alcohol_result = fuzzy_field_check(extracted_text, application_data.get("alcohol_content"), threshold=90)
    net_contents_result = fuzzy_field_check(extracted_text, application_data.get("net_contents"), threshold=90)
    warning_result = check_warning(extracted_text)

    checks = {
        "Brand Name": brand_result,
        "Class/Type": class_type_result,
        "Alcohol Content": alcohol_result,
        "Net Contents": net_contents_result,
        "Government Warning": warning_result,
    }

    passed_count = sum(1 for result in checks.values() if result.get("passed"))
    total_count = len(checks)

    if passed_count == total_count:
        overall_status = "PASS"
    elif passed_count >= 3:
        overall_status = "REVIEW"
    else:
        overall_status = "FAIL"

    return {
        "overall_status": overall_status,
        "passed_count": passed_count,
        "total_count": total_count,
        "checks": checks,
    }
