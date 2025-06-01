import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json

from models.summarizer import summarize
from models.ner import extract_entities
from models.classifier import classify_specialties
from analyzers.audit import run_audit

st.set_page_config(page_title="RxGPT Medical Note Analyzer", layout="wide")

st.title("RxGPT - Medical Record Analyzer")
st.write("Upload a patient JSON file to generate summaries, extract entities, classify specialties, and check for compliance risks.")

uploaded_file = st.file_uploader(" Upload a single patient .json file", type=["json"])

if uploaded_file:
    data = json.load(uploaded_file)
    note = data.get("clinical_note", "")
    patient_id = data.get("patient_id", "Unknown")

    st.subheader(f"Patient ID: {patient_id}")
    st.text_area("📜 Clinical Note", note, height=150)

    if st.button("🔍 Analyze Note"):
        if not note.strip():
            st.error("Note is empty. Please provide a valid clinical note.")
        else:
            with st.spinner("Analyzing..."):
                summary = summarize(note)
                entities = extract_entities(note)
                specialties = classify_specialties(note)
                alerts = run_audit(summary, entities, specialties)

            st.markdown("### Summary")
            st.write(summary)

            st.markdown("###  Extracted Entities")
            for e in entities:
                st.markdown(f"- **{e['entity']}**: {e['word']} _(score: {round(e['score'], 2)})_")

            st.markdown("###  Medical Specialties")
            for s in specialties:
                st.markdown(f"- **{s['label']}** (confidence: {round(s['score'], 2)})")

            st.markdown("###  Audit Alerts")
            if alerts:
                for alert in alerts:
                    st.warning(f" {alert}")
            else:
                st.success(" No issues detected.")
