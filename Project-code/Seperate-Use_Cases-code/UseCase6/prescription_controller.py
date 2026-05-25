from __future__ import annotations

from tkinter import messagebox


class PrescriptionController:
    def __init__(self, portal, repository):
        self.portal = portal
        self.repository = repository
        self.current_patient = None
        self.selected_medicine = None
        self.blocked_medicine = None

    @property
    def doctor_name(self):
        return getattr(self.portal.controller, "current_user_name", "Doctor")

    def start_flow(self):
        self.current_patient = None
        self.selected_medicine = None
        self.blocked_medicine = None
        self.portal.sub_pages["prescription_patient_search"].reset()
        self.portal.show_sub_page("prescription_patient_search")

    def search_patient(self, query):
        patient = self.repository.search_patient(query)
        if not patient:
            messagebox.showerror("Patient not found", "No patient matched the search criteria.")
            return
        self.load_patient(patient["patient_id"])

    def load_patient(self, patient_id):
        try:
            self.current_patient = self.repository.get_patient_bundle(patient_id)
        except ValueError as error:
            messagebox.showerror("Patient unavailable", str(error))
            return

        self.portal.sub_pages["prescription_patient_details"].set_patient_bundle(self.current_patient)
        self.portal.show_sub_page("prescription_patient_details")

    def start_medicine_search(self):
        if not self.current_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before creating a prescription.")
            return

        self.selected_medicine = None
        self.blocked_medicine = None
        self.portal.sub_pages["medicine_search"].reset()
        self.portal.show_sub_page("medicine_search")

    def search_medicines(self, query):
        medicines = self.repository.search_medicines(query, self.doctor_name)
        if not medicines:
            messagebox.showinfo("No medicines", "No allowed medicines matched the search criteria.")
            return
        self.show_medicine_results(medicines)

    def show_medicine_results(self, medicines):
        self.portal.sub_pages["medicine_selection"].set_medicines(medicines)
        self.portal.show_sub_page("medicine_selection")

    def select_medicine(self, medicine):
        if not self.current_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before selecting medicine.")
            return

        self.selected_medicine = medicine
        patient_id = self.current_patient["patient"]["patient_id"]
        warnings = self.repository.check_medicine_safety(patient_id, medicine)
        if warnings:
            self.blocked_medicine = medicine
            self.selected_medicine = None
            self.portal.sub_pages["prescription_safety_warning"].set_warning(medicine, warnings)
            self.portal.show_sub_page("prescription_safety_warning")
            return

        self.portal.sub_pages["prescription_form"].set_context(
            self.current_patient,
            medicine,
            [],
        )
        self.portal.show_sub_page("prescription_form")

    def confirm_safety_warning(self):
        if not self.current_patient or not self.blocked_medicine:
            messagebox.showerror("Medicine unavailable", "Select a medicine before searching alternatives.")
            return

        patient_id = self.current_patient["patient"]["patient_id"]
        alternatives = self.repository.find_alternative_medicines(
            patient_id,
            self.blocked_medicine,
            self.doctor_name,
        )
        self.portal.sub_pages["medicine_selection"].set_medicines(alternatives)
        self.portal.show_sub_page("medicine_selection")

    def renew_prescription(self, prescription_log):
        if not self.current_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before renewing a prescription.")
            return

        medicine = self.repository.get_medicine_by_id(prescription_log.get("medicine_id", ""))
        if not medicine:
            messagebox.showerror("Medicine unavailable", "The medicine from the previous prescription was not found.")
            return

        self.selected_medicine = medicine
        initial_values = {
            "dosage": prescription_log.get("dosage", ""),
            "frequency": prescription_log.get("frequency", ""),
            "duration": prescription_log.get("duration", ""),
            "instructions": prescription_log.get("instructions", ""),
        }
        self.portal.sub_pages["prescription_form"].set_context(
            self.current_patient,
            medicine,
            [],
            initial_values=initial_values,
            back_page="prescription_patient_details",
        )
        self.portal.show_sub_page("prescription_form")

    def submit_prescription(self, prescription):
        if not self.current_patient or not self.selected_medicine:
            messagebox.showerror("Prescription unavailable", "Select a patient and medicine before submitting.")
            return

        patient_id = self.current_patient["patient"]["patient_id"]
        saved, result = self.repository.create_prescription(
            patient_id,
            self.doctor_name,
            self.selected_medicine,
            prescription,
        )
        if not saved:
            messagebox.showerror("Invalid prescription", result)
            return

        self.current_patient = self.repository.get_patient_bundle(patient_id)
        self.portal.sub_pages["prescription_success"].set_prescription_id(result)
        self.portal.show_sub_page("prescription_success")

    def return_to_patient(self):
        if self.current_patient:
            self.portal.sub_pages["prescription_patient_details"].set_patient_bundle(self.current_patient)
        self.portal.show_sub_page("prescription_patient_details")
