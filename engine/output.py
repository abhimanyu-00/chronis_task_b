# Component 4 — Safe Output
# PDF requirement: "medical, diagnostic, or characterological
# statements must be impossible by construction"
# The schema has no free text field about the person
# so harmful output is structurally impossible


def make_result(domain, divergence_type, gap,
                behavioral_score, narrative_score,
                behavioral_summary, narrative_summary,
                evidence_note):
    """
    Build the output dictionary.
    Fixed schema only — no free text about the person.
    No field exists for diagnosis, personality, or character.
    """
    return {
        "domain": domain,
        "status": "classified",
        "divergence_type": divergence_type,
        "gap_score": round(gap, 2),
        "behavioral_score": round(behavioral_score, 2),
        "narrative_score": round(narrative_score, 2),
        "behavioral_summary": behavioral_summary,
        "narrative_summary": narrative_summary,
        "evidence_note": evidence_note
    }


def make_abstention(domain, reason):
    """
    Build abstention output when evidence is insufficient.
    No type is assigned. No score is calculated.
    """
    return {
        "domain": domain,
        "status": "insufficient_evidence",
        "reason": reason
    }