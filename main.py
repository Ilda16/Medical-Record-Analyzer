import json
import os
import argparse
from models.summarizer import summarize
from models.ner import extract_entities
from models.classifier import classify_specialties
from analyzers.audit import run_audit
from utils.output_writer import save_output
from utils.markdown_writer import save_markdown
from utils.csv_exporter import export_summary_to_csv
from utils.loader import load_patient_note, load_patients

def process_patient(patient, output_base):
    pid = patient.get("patient_id", "unknown")
    note = patient.get("note", "")
    name = patient.get("name", "Unknown")
    date = patient.get("date", "Unknown")

    if not note.strip():
        print(f"[SKIP] Empty note for patient ID {pid}")
        return

    metadata = {
        "patient_id": pid,
        "name": name,
        "date": date
    }

    print(f"\n--- Processing Patient: {name} (ID: {pid}) ---")

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

    # Make output directory
    output_dir = os.path.join(output_base, pid)
    os.makedirs(output_dir, exist_ok=True)

    # Save metadata
    with open(os.path.join(output_dir, "metadata.json"), "w") as meta_file:
        json.dump(metadata, meta_file, indent=4)

    # Save outputs
    save_output(summary, entities, specialties, alerts, out_path=os.path.join(output_dir, "result.json"))
    save_markdown(summary, entities, specialties, alerts, out_path=os.path.join(output_dir, "report.md"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process patient clinical notes with RxGPT.")
    parser.add_argument("--input", type=str, default="data/patients.json", help="Path to patients JSON file")
    parser.add_argument("--output", type=str, default="output", help="Directory to save output")
    parser.add_argument("--single", type=str, help="Optional: Path to single patient JSON file")
    args = parser.parse_args()

    if args.single:
        note, patient_id = load_patient_note(args.single)

        if not note.strip():
            print(f"[ERROR] Clinical note is empty for Patient ID: {patient_id}")
        else:
            print(f"\n--- Patient ID: {patient_id} ---")
            print("\n--- Summary ---")
            print(summarize(note))

            print("\n--- Extracted Medical Entities ---")
            for e in extract_entities(note):
                print(f"{e['entity']}: {e['word']} ({e['score']})")

            print("\n--- Medical Specialties ---")
            for s in classify_specialties(note):
                print(f"{s['label']}: {s['score']}")
    else:
        patients = load_patients(args.input)
        for patient in patients:
            process_patient(patient, args.output)

        print("\nAll patients processed.")
        export_summary_to_csv()
