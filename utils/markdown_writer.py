from datetime import datetime

def save_markdown(summary, entities, specialties, audit_alerts, out_path="output/report.md"):
    with open(out_path, "w") as f:
        f.write(f"# Patient Summary Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        f.write("## Summary\n")
        f.write(f"> {summary}\n\n")

        f.write("## Extracted Medical Entities\n")
        for e in entities:
            f.write(f"- {e['entity']}: {e['word']} ({e['score']})\n")
        f.write("\n")

        f.write("## Medical Specialties\n")
        for s in specialties:
            f.write(f"- {s['label']} (Score: {s['score']})\n")
        f.write("\n")

        f.write("## Audit Alerts\n")
        if audit_alerts:
            for alert in audit_alerts:
                f.write(f"{alert}\n")
        else:
            f.write("No risk or compliance flags found.\n")

    print(f"Markdown report saved to {out_path}")
