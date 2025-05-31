import json

def load_patient_note(filepath):
    """
    Load a patient note from a JSON file.

    Args:
        filepath (str): Path to the JSON file containing the patient note.

    Returns:
        tuple: clinical_note (str), patient_id (str)
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get("clinical_note", ""), data.get("patient_id", "unknown")

def load_patients(file_path="data/patients.json"):
    """
    Load multiple patient records from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing a list of patients.

    Returns:
        list[dict]: A list of patient record dictionaries.
    """
    with open(file_path, "r") as f:
        return json.load(f)
