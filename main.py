from models.summarizer import summarize
from models.ner import extract_entities
from models.classifier import classify_specialties

if __name__ == "__main__":
    clinical_note = """
    Patient presents with shortness of breath, mild fever, and persistent cough.
    History of asthma. Prescribed Albuterol and advised follow-up in 1 week.
    """

    print("\n--- Summary ---")
    print(summarize(clinical_note))

    print("\n--- Extracted Medical Entities ---")
    entities = extract_entities(clinical_note)
    for e in entities:
        print(f"{e['entity']}: {e['word']} ({e['score']})")

    print("\n--- Medical Specialties ---")
    specialties = classify_specialties(clinical_note)
    for s in specialties:
        print(f"{s['label']}: {s['score']}")



