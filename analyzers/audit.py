def run_audit(summary, entities, specialties):

    alerts = []

    # No allergy info
    if not any("allergy" in e["word"].lower() for e in entities):
        alerts.append(" No allergy information mentioned.")

    # Psych risk with no referral
    if "suicidal" in summary.lower():
        if not any("psych" in e["word"].lower() for e in entities):
            alerts.append(" Psychiatric symptom noted, but no referral detected.")

    # SSN-like numbers detected
    if any(e["word"].replace("-", "").isdigit() and len(e["word"].replace("-", "")) == 9 for e in entities):
        alerts.append("Possible SSN detected in note.")

    # No medications
    if not any(e["entity"].lower() == "medication" for e in entities):
        alerts.append("No medications mentioned.")

    # Specialty: if Psychiatry is high but no psych entity found
    specialty_labels = [s["label"].lower() for s in specialties]
    if "psychiatry" in specialty_labels and not any("psych" in e["word"].lower() for e in entities):
        alerts.append(" Classified as psychiatric, but no psych-related terms found.")

    return alerts

