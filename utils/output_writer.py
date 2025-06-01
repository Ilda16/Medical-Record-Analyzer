import json
import os
from datetime import datetime

def save_output(summary, entities, specialties, audit_alerts, out_path="output/result.json"):
    result = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "entities": entities,
        "specialties": specialties,  
        "audit_alerts": audit_alerts
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"\n Results saved to {out_path}")
