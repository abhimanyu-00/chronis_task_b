# Component 3 — Evidence Sufficiency Check

MIN_DAYS = 3       # minimum days of behavioral data needed
MIN_SNIPPETS = 1   # minimum self-talk snippets needed


def check_evidence(domain, behavioral_days, matching_snippets):
    """
    Check if we have enough data to classify this domain.
    Returns a result dict with status ok or insufficient_evidence.
    """
    issues = []

    # Check 1 — enough days of behavioral data?
    if len(behavioral_days) < MIN_DAYS:
        issues.append(
            f"only {len(behavioral_days)} day(s) of data, "
            f"need at least {MIN_DAYS}"
        )

    # Check 2 — at least one matching self-talk snippet?
    if len(matching_snippets) < MIN_SNIPPETS:
        issues.append(
            "no self-talk snippets found for this domain"
        )

    # If any issues found — abstain immediately
    if issues:
        return {
            "domain": domain,
            "status": "insufficient_evidence",
            "reason": "; ".join(issues)
        }

    # All checks passed
    return {
        "domain": domain,
        "status": "ok"
    }