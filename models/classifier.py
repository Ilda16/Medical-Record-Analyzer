from transformers import pipeline

#zero-shot classifier model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_specialties(text):
    # Define your medical specialty labels
    labels = [
        "Pulmonology",
        "Cardiology",
        "Psychiatry",
        "Neurology",
        "Oncology",
        "Endocrinology",
        "Infectious Disease",
        "Primary Care"
    ]

    result = classifier(text, candidate_labels=labels, multi_label=True)

    # Return labels and scores as a list of dicts
    return [
        {"label": label, "score": round(score, 3)}
        for label, score in zip(result["labels"], result["scores"])
        if score >= 0.3  # Optional threshold
    ]
