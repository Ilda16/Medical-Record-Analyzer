import json
from pathlib import Path

class ClinicalDataLoader:
    def __init__(self, input_path="data/sample_input.json"):
        self.input_path = Path(input_path)

    def load_data(self) -> list[dict]:
        """Load and validate clinical notes from JSON"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file {self.input_path} not found.")
        with open(self.input_path) as f:
            records = json.load(f)
        self._validate(records)
        return records

    def _validate(self, records: list):
        """Check for required fields"""
        required_fields = {"patient_id", "clinical_note"}
        for record in records:
            if not all(field in record for field in required_fields):
                raise ValueError(f"Invalid record: Missing fields in {record}")