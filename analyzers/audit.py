def run_audit(summary, entities, specialties):
    alerts = []

    # No allergy info in NER or summary
    has_allergy = any("allergy" in e["word"].lower() for e in entities) or "allergy" in summary.lower()
    if not has_allergy:
        alerts.append("No allergy information mentioned.")

    # Psych risk with no referral
    if "suicidal" in summary.lower():
        if not any("psych" in e["word"].lower() for e in entities):
            alerts.append("Psychiatric symptom noted (e.g. suicidal), but no referral detected.")

    # SSN-like pattern
    if any(e["word"].replace("-", "").isdigit() and len(e["word"].replace("-", "")) == 9 for e in entities):
        alerts.append("Possible SSN or sensitive ID detected in note.")

    # No medications detected
    if not any(e["entity"].lower() == "medication" for e in entities):
        alerts.append("No medications mentioned in the record.")

    # Classified as psychiatric, but no psych-related entity found
    specialty_labels = [s["label"].lower() for s in specialties]
    if "psychiatry" in specialty_labels and not any("psych" in e["word"].lower() for e in entities):
        alerts.append("Classified as psychiatric, but no psychiatric-related terms found.")

    # No diagnosis or condition mention (basic check)
    if not any(e["entity"].lower() in ["condition", "diagnosis"] for e in entities):
        alerts.append("No diagnosed condition or disease mentioned.")

    return alerts


