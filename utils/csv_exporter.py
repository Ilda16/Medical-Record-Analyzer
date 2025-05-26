import os
import json
import csv

def export_summary_to_csv(output_dir="output", csv_path="output/summary.csv"):
    rows = []

    for patient_folder in os.listdir(output_dir):
        folder_path = os.path.join(output_dir, patient_folder)
        result_path = os.path.join(folder_path, "result.json")
        metadata_path = os.path.join(folder_path, "metadata.json")

        if not os.path.isfile(result_path) or not os.path.isfile(metadata_path):
            continue

        with open(result_path, "r") as f:
            result = json.load(f)
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        summary = result.get("summary", "")
        specialties = result.get("specialties", [])
        audit_alerts = result.get("audit_alerts", [])

        top_specialties = ", ".join([s["label"] for s in specialties[:2]]) if specialties else "N/A"

        rows.append({
            "patient_id": metadata.get("patient_id", ""),
            "name": metadata.get("name", ""),
            "date": metadata.get("date", ""),
            "summary_preview": summary[:80] + "..." if len(summary) > 80 else summary,
            "top_specialties": top_specialties,
            "alert_count": len(audit_alerts),
            "alert_preview": audit_alerts[0] if audit_alerts else "None"
        })

    # Write to CSV (UTF-8, Google Sheets-friendly)
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["patient_id", "name", "date", "summary_preview", "top_specialties", "alert_count", "alert_preview"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f" CSV summary saved to {csv_path}")
