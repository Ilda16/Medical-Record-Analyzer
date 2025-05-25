from transformers import pipeline

# Try a general biomedical model
model_name = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract"

classifier = pipeline("text-classification", model=model_name)

def classify_specialties(text, threshold=0.5):
    """Classify medical notes using a general biomedical classifier (placeholder behavior)."""
    result = classifier(text)
    return [
        {
            "label": result[0]["label"],
            "score": round(result[0]["score"], 3)
        }
    ]
