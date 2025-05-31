import json
import os
from models.summarizer import summarize
from models.ner import extract_entities
from models.classifier import classify_specialties
from analyzers.audit import run_audit
from utils.output_writer import save_output
from utils.markdown_writer import save_markdown
from utils.csv_exporter import export_summary_to_csv
from utils.loader import load_patient_note 
from utils.loader import load_patients

patients = load_patients()
for patient in patients:
    pid = patient["patient_id"]
    note = patient["note"]
    name = patient.get("name", "Unknown")
    date = patient.get("date", "Unknown")

    if not note.strip():
        print(f"[SKIP] Empty note for patient ID {pid}")
        continue

    print(f"\n--- Processing Patient: {name} (ID: {pid}) ---")

    summary = summarize(note)
    entities = extract_entities(note)
    specialties = classify_specialties(note)

    print(f"Summary: {summary}")
    print("Entities:", [e["word"] for e in entities])
    print("Specialties:", [s["label"] for s in specialties])


def load_patients(file_path="data/patients.json"):
    with open(file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
     # Load from file
    note, patient_id = load_patient_note("data/sample_input.json")

    print(f"\n--- Patient ID: {patient_id} ---")
    print("\n--- Summary ---")
    print(summarize(note))

    print("\n--- Extracted Medical Entities ---")
    for e in extract_entities(note):
        print(f"{e['entity']}: {e['word']} ({e['score']})")

    print("\n--- Medical Specialties ---")
    for s in classify_specialties(note):
        print(f"{s['label']}: {s['score']}")

    for patient in patients:
        pid = patient["patient_id"]
        note = patient["note"]
        name = patient.get("name", "Unknown")
        date = patient.get("date", "Unknown")

        metadata = {
            "patient_id": pid,
            "name": name,
            "date": date
        }
        with open(f"output/{pid}/metadata.json", "w") as meta_file:
            json.dump(metadata, meta_file)

        print(f"\n Processing Patient ID: {pid}")
        summary = summarize(note)
        entities_raw = extract_entities(note)
        entities = [
            {"entity": e["entity"], "word": e["word"], "score": float(e["score"])}
            for e in entities_raw
        ]
        specialties_raw = classify_specialties(note)
        specialties = [
            {"label": s["label"], "score": float(s["score"])}
            for s in specialties_raw
        ]
        alerts = run_audit(summary, entities, specialties)

        # Make output dir if needed
        os.makedirs(f"output/{pid}", exist_ok=True)

        # Save result.json and report.md inside patient folder
        save_output(summary, entities, specialties, alerts, out_path=f"output/{pid}/result.json")
        save_markdown(summary, entities, specialties, alerts, out_path=f"output/{pid}/report.md")

    print("\n All patients processed.")

    export_summary_to_csv()





