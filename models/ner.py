from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load model and tokenizer from Hugging Face
model_name = "d4data/biomedical-ner-all"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_entities(text):
    """Extract medical entities from clinical text."""
    entities = ner_pipeline(text)
    return [
        {
            "entity": item["entity_group"],
            "word": item["word"],
            "score": round(item["score"], 3)
        }
        for item in entities
    ]
