from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd


class PatientRecordRepository:
    def __init__(self):
        self.shared_data_dir = Path("./Data")
        self.uc_data_dir = Path("./Seperate-Use_Cases-code") / "uc5"
        self.patients_file = self.shared_data_dir / "patients.csv"
        self.hospitalizations_file = self.uc_data_dir / "hospitalizations.csv"
        self.folders_file = self.uc_data_dir / "patient_medical_folders.csv"
        self.lab_tests_file = self.uc_data_dir / "lab_tests.csv"
        self.lab_test_requests_file = self.uc_data_dir / "lab_test_requests.csv"

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

    def get_record_bundle(self, patient_id):
        patients = self._read_csv(self.patients_file)
        hospitalizations = self._read_csv(self.hospitalizations_file)
        folders = self._read_csv(self.folders_file)
        lab_tests = self._read_csv(self.lab_tests_file)
        lab_test_requests = self._read_csv(self.lab_test_requests_file)

        patient_match = patients[patients["patient_id"].astype(str) == patient_id]
        folder_match = folders[folders["patient_id"].astype(str) == patient_id]

        if patient_match.empty:
            raise ValueError("Patient was not found.")
        if folder_match.empty:
            raise ValueError("Medical folder was not found for this patient.")

        return {
            "patient": patient_match.iloc[0].to_dict(),
            "hospitalization": hospitalizations[
                hospitalizations["patient_id"].astype(str) == patient_id
            ].to_dict("records"),
            "folder": folder_match.iloc[0].to_dict(),
            "lab_tests": lab_tests[
                lab_tests["patient_id"].astype(str) == patient_id
            ].to_dict("records"),
            "lab_test_requests": lab_test_requests[
                lab_test_requests["patient_id"].astype(str) == patient_id
            ].to_dict("records"),
        }

    def lock_folder(self, folder_id, doctor_name):
        folders = self._read_csv(self.folders_file)
        folder_index = folders.index[folders["folder_id"].astype(str) == str(folder_id)]
        if folder_index.empty:
            return False, "Medical folder was not found."

        row_index = folder_index[0]
        locked_by = str(folders.at[row_index, "locked_by"]).strip()
        if locked_by and locked_by != doctor_name:
            return False, f"Medical folder is currently being edited by {locked_by}."

        folders.at[row_index, "locked_by"] = doctor_name
        self._write_csv(self.folders_file, folders)
        return True, ""

    def release_folder(self, folder_id, doctor_name):
        folders = self._read_csv(self.folders_file)
        folder_index = folders.index[folders["folder_id"].astype(str) == str(folder_id)]
        if folder_index.empty:
            return

        row_index = folder_index[0]
        if str(folders.at[row_index, "locked_by"]).strip() == doctor_name:
            folders.at[row_index, "locked_by"] = ""
            self._write_csv(self.folders_file, folders)

    def validate_record(self, patient, folder, lab_tests, lab_test_requests, updates):
        required_folder_fields = ["blood_type", "diagnosis", "notes"]
        missing = [field for field in required_folder_fields if not updates.get(field, "").strip()]
        if missing:
            return False, "Please complete blood type, diagnosis, and notes before saving."

        if folder.get("patient_id") != patient.get("patient_id"):
            return False, "Medical folder does not belong to the selected patient."

        for lab_test in lab_tests:
            if lab_test.get("patient_id") != patient.get("patient_id"):
                return False, "A lab test is connected to a different patient."
            if lab_test.get("folder_id") != folder.get("folder_id"):
                return False, "A lab test is connected to a different medical folder."

        for request in lab_test_requests:
            if request.get("patient_id") != patient.get("patient_id"):
                return False, "A lab test request is connected to a different patient."
            if request.get("folder_id") != folder.get("folder_id"):
                return False, "A lab test request is connected to a different medical folder."

        return True, ""

    def save_folder(self, folder_id, doctor_name, updates):
        folders = self._read_csv(self.folders_file)
        folder_index = folders.index[folders["folder_id"].astype(str) == str(folder_id)]
        if folder_index.empty:
            return False, "Medical folder was not found."

        row_index = folder_index[0]
        if str(folders.at[row_index, "locked_by"]).strip() != doctor_name:
            return False, "Medical folder is not locked for the current doctor."

        for field, value in updates.items():
            folders.at[row_index, field] = value.strip()

        folders.at[row_index, "last_updated"] = date.today().isoformat()
        folders.at[row_index, "locked_by"] = ""
        self._write_csv(self.folders_file, folders)
        return True, ""
