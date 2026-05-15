from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


class PrescriptionRepository:
    def __init__(self):
        self.shared_data_dir = Path("./Data")
        self.uc_data_dir = Path("./uc5_6")
        self.patients_file = self.shared_data_dir / "patients.csv"
        self.doctors_file = self.shared_data_dir / "doctors.csv"
        self.folders_file = self.uc_data_dir / "patient_medical_folders.csv"
        self.medicines_file = self.uc_data_dir / "medicines.csv"
        self.prescription_logs_file = self.uc_data_dir / "prescription_logs.csv"

    def _read_csv(self, path):
        if not path.exists():
            return pd.DataFrame()
        return pd.read_csv(path, keep_default_na=False)

    def _write_csv(self, path, data_frame):
        data_frame.to_csv(path, index=False)

    def search_patient(self, query):
        query = query.strip().lower()
        if not query:
            return None

        patients = self._read_csv(self.patients_file)
        if patients.empty:
            return None

        full_name = (
            patients["first_name"].astype(str).str.lower()
            + " "
            + patients["last_name"].astype(str).str.lower()
        )
        matches = patients[
            patients["patient_id"].astype(str).str.lower().eq(query)
            | patients["email"].astype(str).str.lower().str.contains(query, regex=False)
            | patients["contact_number"].astype(str).str.lower().str.contains(query, regex=False)
            | patients["first_name"].astype(str).str.lower().str.contains(query, regex=False)
            | patients["last_name"].astype(str).str.lower().str.contains(query, regex=False)
            | full_name.str.contains(query, regex=False)
        ]

        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def get_patient_bundle(self, patient_id):
        patients = self._read_csv(self.patients_file)
        folders = self._read_csv(self.folders_file)
        logs = self._read_csv(self.prescription_logs_file)

        patient_match = patients[patients["patient_id"].astype(str) == str(patient_id)]
        if patient_match.empty:
            raise ValueError("Patient was not found.")

        folder_match = folders[folders["patient_id"].astype(str) == str(patient_id)]
        folder = folder_match.iloc[0].to_dict() if not folder_match.empty else {}

        patient_logs = logs[logs["patient_id"].astype(str) == str(patient_id)]
        return {
            "patient": patient_match.iloc[0].to_dict(),
            "folder": folder,
            "prescription_logs": patient_logs.to_dict("records"),
        }

    def get_doctor(self, doctor_name):
        doctors = self._read_csv(self.doctors_file)
        if doctors.empty:
            return {}

        full_name = (
            doctors["first_name"].astype(str).str.strip()
            + " "
            + doctors["last_name"].astype(str).str.strip()
        )
        matches = doctors[full_name.str.lower() == doctor_name.strip().lower()]
        if matches.empty:
            return {}
        return matches.iloc[0].to_dict()

    def search_medicines(self, query, doctor_name):
        query = query.strip().lower()
        if not query:
            return []

        doctor = self.get_doctor(doctor_name)
        doctor_specialty = str(doctor.get("specialization", "")).strip().lower()
        medicines = self._read_csv(self.medicines_file)
        if medicines.empty:
            return []

        text_matches = medicines[
            medicines["name"].astype(str).str.lower().str.contains(query, regex=False)
            | medicines["category"].astype(str).str.lower().str.contains(query, regex=False)
            | medicines["active_substance"].astype(str).str.lower().str.contains(query, regex=False)
        ]

        allowed_rows = []
        for _, medicine in text_matches.iterrows():
            allowed_specialties = [
                specialty.strip().lower()
                for specialty in str(medicine.get("allowed_specialties", "")).split(";")
            ]
            if "all" in allowed_specialties or doctor_specialty in allowed_specialties:
                allowed_rows.append(medicine.to_dict())

        return allowed_rows

    def get_medicine_by_id(self, medicine_id):
        medicines = self._read_csv(self.medicines_file)
        if medicines.empty:
            return {}

        matches = medicines[medicines["medicine_id"].astype(str) == str(medicine_id)]
        if matches.empty:
            return {}
        return matches.iloc[0].to_dict()

    def _doctor_can_prescribe(self, medicine, doctor_name):
        doctor = self.get_doctor(doctor_name)
        doctor_specialty = str(doctor.get("specialization", "")).strip().lower()
        allowed_specialties = [
            specialty.strip().lower()
            for specialty in str(medicine.get("allowed_specialties", "")).split(";")
        ]
        return "all" in allowed_specialties or doctor_specialty in allowed_specialties

    def check_medicine_safety(self, patient_id, medicine):
        bundle = self.get_patient_bundle(patient_id)
        folder = bundle["folder"]
        warnings = []

        allergies = str(folder.get("allergies", "")).lower()
        allergy_terms = [
            term.strip().lower()
            for term in str(medicine.get("allergy_substances", "")).split(";")
            if term.strip()
        ]
        for term in allergy_terms:
            if term in allergies:
                warnings.append(f"Patient allergy matches {term}.")

        patient_conditions = " ".join(
            [
                str(folder.get("chronic_conditions", "")),
                str(folder.get("diagnosis", "")),
                str(folder.get("notes", "")),
            ]
        ).lower()
        contraindications = [
            term.strip().lower()
            for term in str(medicine.get("contraindications", "")).split(";")
            if term.strip()
        ]
        for term in contraindications:
            if term in patient_conditions:
                warnings.append(f"Contraindication found for {term}.")

        return warnings

    def find_alternative_medicines(self, patient_id, medicine, doctor_name):
        medicines = self._read_csv(self.medicines_file)
        if medicines.empty:
            return []

        category = str(medicine.get("category", "")).strip().lower()
        selected_id = str(medicine.get("medicine_id", "")).strip()
        alternatives = []

        for _, alternative in medicines.iterrows():
            alternative = alternative.to_dict()
            same_category = str(alternative.get("category", "")).strip().lower() == category
            different_medicine = str(alternative.get("medicine_id", "")).strip() != selected_id
            if not same_category or not different_medicine:
                continue
            if not self._doctor_can_prescribe(alternative, doctor_name):
                continue
            if self.check_medicine_safety(patient_id, alternative):
                continue
            alternatives.append(alternative)

        return alternatives

    def validate_prescription(self, prescription):
        required_fields = ["dosage", "frequency", "duration", "instructions"]
        missing = [field for field in required_fields if not prescription.get(field, "").strip()]
        if missing:
            return False, "Please complete dosage, frequency, duration, and instructions."
        return True, ""

    def create_prescription(self, patient_id, doctor_name, medicine, prescription):
        valid, error = self.validate_prescription(prescription)
        if not valid:
            return False, error

        logs = self._read_csv(self.prescription_logs_file)
        next_number = len(logs.index) + 1
        prescription_id = f"PR{next_number:03d}"
        log_id = f"PL{next_number:03d}"
        doctor = self.get_doctor(doctor_name)

        new_row = {
            "log_id": log_id,
            "prescription_id": prescription_id,
            "patient_id": patient_id,
            "doctor_id": doctor.get("doctor_id", ""),
            "doctor_name": doctor_name,
            "medicine_id": medicine.get("medicine_id", ""),
            "medicine_name": medicine.get("name", ""),
            "dosage": prescription.get("dosage", "").strip(),
            "frequency": prescription.get("frequency", "").strip(),
            "duration": prescription.get("duration", "").strip(),
            "instructions": prescription.get("instructions", "").strip(),
            "created_at": date.today().isoformat(),
            "status": "Issued",
        }

        logs = pd.concat([logs, pd.DataFrame([new_row])], ignore_index=True)
        self._write_csv(self.prescription_logs_file, logs)
        return True, prescription_id
