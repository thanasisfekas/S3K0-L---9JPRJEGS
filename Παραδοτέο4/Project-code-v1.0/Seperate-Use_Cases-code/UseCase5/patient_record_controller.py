from __future__ import annotations

from tkinter import messagebox


class PatientRecordController:
    def __init__(self, portal, repository):
        self.portal = portal
        self.repository = repository
        self.current_record = None

    @property
    def doctor_name(self):
        return getattr(self.portal.controller, "current_user_name", "Doctor")

    def start_flow(self):
        self.portal.sub_pages["patient_record_search"].reset()
        self.portal.show_sub_page("patient_record_search")

    def search_patient(self, query):
        patient = self.repository.search_patient(query)
        if not patient:
            messagebox.showerror("Patient not found", "No patient matched the search criteria.")
            return
        self.load_patient_record(patient["patient_id"])

    def load_patient_record(self, patient_id):
        try:
            self.current_record = self.repository.get_record_bundle(patient_id)
        except ValueError as error:
            messagebox.showerror("Record unavailable", str(error))
            return

        self.portal.sub_pages["patient_record_history"].set_record(self.current_record)
        self.portal.show_sub_page("patient_record_history")

    def open_editor(self):
        if not self.current_record:
            messagebox.showerror("Record unavailable", "Search for a patient before editing.")
            return

        folder_id = self.current_record["folder"]["folder_id"]
        locked, error = self.repository.lock_folder(folder_id, self.doctor_name)
        if not locked:
            self.portal.sub_pages["patient_record_locked"].set_message(error)
            self.portal.show_sub_page("patient_record_locked")
            return

        patient_id = self.current_record["patient"]["patient_id"]
        self.current_record = self.repository.get_record_bundle(patient_id)
        self.portal.sub_pages["patient_record_edit"].set_record(self.current_record)
        self.portal.show_sub_page("patient_record_edit")

    def save_edits(self, updates):
        if not self.current_record:
            messagebox.showerror("Record unavailable", "Search for a patient before saving.")
            return

        valid, error = self.repository.validate_record(
            self.current_record["patient"],
            self.current_record["folder"],
            self.current_record["lab_tests"],
            self.current_record["lab_test_requests"],
            updates,
        )
        if not valid:
            self.portal.sub_pages["patient_record_validation_failure"].set_message(error)
            self.portal.show_sub_page("patient_record_validation_failure")
            return

        folder_id = self.current_record["folder"]["folder_id"]
        saved, error = self.repository.save_folder(folder_id, self.doctor_name, updates)
        if not saved:
            messagebox.showerror("Save failed", error)
            return

        patient_id = self.current_record["patient"]["patient_id"]
        self.current_record = self.repository.get_record_bundle(patient_id)
        self.portal.show_sub_page("patient_record_success")

    def cancel_edit(self):
        if self.current_record:
            folder_id = self.current_record["folder"]["folder_id"]
            self.repository.release_folder(folder_id, self.doctor_name)
        self.portal.show_sub_page("patient_record_history")

    def return_to_saved_record(self):
        if self.current_record:
            self.portal.sub_pages["patient_record_history"].set_record(self.current_record)
        self.portal.show_sub_page("patient_record_history")

    def confirm_validation_failure(self):
        self.portal.show_sub_page("patient_record_edit")

    def confirm_locked_folder_notice(self):
        if self.current_record:
            self.portal.sub_pages["patient_record_history"].set_record(self.current_record)
        self.portal.show_sub_page("patient_record_history")

