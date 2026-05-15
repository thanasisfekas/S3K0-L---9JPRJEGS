from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox

from MenuControllers.centralMenu import CentralMenu
from uc5_6.patient_record_pages import (
    PatientRecordEditFrame,
    PatientRecordHistoryFrame,
    PatientRecordLockedFrame,
    PatientRecordSearchFrame,
    PatientRecordSuccessFrame,
    PatientRecordValidationFailureFrame,
)
from uc5_6.prescription_pages import (
    MedicineSearchFrame,
    MedicineSelectionFrame,
    PrescriptionFormFrame,
    PrescriptionPatientDetailsFrame,
    PrescriptionPatientSearchFrame,
    PrescriptionSafetyWarningFrame,
    PrescriptionSuccessFrame,
)
from uc5_6.medical_record_repository import PatientRecordRepository
from uc5_6.prescription_repository import PrescriptionRepository


BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"


class DoctorPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.record_repository = PatientRecordRepository()
        self.prescription_repository = PrescriptionRepository()
        self.current_record = None
        self.current_prescription_patient = None
        self.selected_medicine = None
        self.blocked_medicine = None
        self.configure(fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(
            self,
            height=70,
            fg_color=CARD_WHITE,
            corner_radius=0,
            border_width=1,
            border_color="#E2E8F0",
        )
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(
            self.top_bar,
            text="✚ Vitalink | Doctor Portal",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#3D59AB",
        )
        self.lbl_title.pack(side="left", padx=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.sub_pages = {
            "menu": DoctorCentralMenu(self.container, self),
            "patient_record_search": PatientRecordSearchFrame(self.container, self),
            "patient_record_history": PatientRecordHistoryFrame(self.container, self),
            "patient_record_edit": PatientRecordEditFrame(self.container, self),
            "patient_record_success": PatientRecordSuccessFrame(self.container, self),
            "patient_record_validation_failure": PatientRecordValidationFailureFrame(self.container, self),
            "patient_record_locked": PatientRecordLockedFrame(self.container, self),
            "prescription_patient_search": PrescriptionPatientSearchFrame(self.container, self),
            "prescription_patient_details": PrescriptionPatientDetailsFrame(self.container, self),
            "medicine_search": MedicineSearchFrame(self.container, self),
            "medicine_selection": MedicineSelectionFrame(self.container, self),
            "prescription_form": PrescriptionFormFrame(self.container, self),
            "prescription_safety_warning": PrescriptionSafetyWarningFrame(self.container, self),
            "prescription_success": PrescriptionSuccessFrame(self.container, self),
        }

        for sp in self.sub_pages.values():
            sp.grid(row=0, column=0, sticky="nsew")

        self.show_sub_page("menu")

        self.btn_logout = ctk.CTkButton(
            self,
            text="\U0001F6AA Logout",
            width=100,
            fg_color="transparent",
            text_color="#800000",
            hover_color="#DC143C",
            command=self.handle_logout,
        )
        self.btn_logout.place(relx=0.02, rely=0.95, anchor="sw")
        self.btn_logout.lift()

    def show_sub_page(self, name):
        self.sub_pages[name].tkraise()

    def start_patient_record_flow(self):
        self.sub_pages["patient_record_search"].reset()
        self.show_sub_page("patient_record_search")

    def start_prescription_flow(self):
        self.current_prescription_patient = None
        self.selected_medicine = None
        self.blocked_medicine = None
        self.sub_pages["prescription_patient_search"].reset()
        self.show_sub_page("prescription_patient_search")

    def load_patient_record(self, patient_id):
        try:
            self.current_record = self.record_repository.get_record_bundle(patient_id)
        except ValueError as error:
            messagebox.showerror("Record unavailable", str(error))
            return

        self.sub_pages["patient_record_history"].set_record(self.current_record)
        self.show_sub_page("patient_record_history")

    def open_record_editor(self):
        if not self.current_record:
            messagebox.showerror("Record unavailable", "Search for a patient before editing.")
            return

        doctor_name = getattr(self.controller, "current_user_name", "Doctor")
        folder_id = self.current_record["folder"]["folder_id"]
        locked, error = self.record_repository.lock_folder(folder_id, doctor_name)
        if not locked:
            self.sub_pages["patient_record_locked"].set_message(error)
            self.show_sub_page("patient_record_locked")
            return

        patient_id = self.current_record["patient"]["patient_id"]
        self.current_record = self.record_repository.get_record_bundle(patient_id)
        self.sub_pages["patient_record_edit"].set_record(self.current_record)
        self.show_sub_page("patient_record_edit")

    def save_record_edits(self, updates):
        if not self.current_record:
            messagebox.showerror("Record unavailable", "Search for a patient before saving.")
            return

        valid, error = self.record_repository.validate_record(
            self.current_record["patient"],
            self.current_record["folder"],
            self.current_record["lab_tests"],
            self.current_record["lab_test_requests"],
            updates,
        )
        if not valid:
            self.sub_pages["patient_record_validation_failure"].set_message(error)
            self.show_sub_page("patient_record_validation_failure")
            return

        doctor_name = getattr(self.controller, "current_user_name", "Doctor")
        folder_id = self.current_record["folder"]["folder_id"]
        saved, error = self.record_repository.save_folder(folder_id, doctor_name, updates)
        if not saved:
            messagebox.showerror("Save failed", error)
            return

        patient_id = self.current_record["patient"]["patient_id"]
        self.current_record = self.record_repository.get_record_bundle(patient_id)
        self.show_sub_page("patient_record_success")

    def cancel_record_edit(self):
        if self.current_record:
            doctor_name = getattr(self.controller, "current_user_name", "Doctor")
            folder_id = self.current_record["folder"]["folder_id"]
            self.record_repository.release_folder(folder_id, doctor_name)
        self.show_sub_page("patient_record_history")

    def return_to_saved_record(self):
        if self.current_record:
            self.sub_pages["patient_record_history"].set_record(self.current_record)
        self.show_sub_page("patient_record_history")

    def confirm_validation_failure(self):
        self.show_sub_page("patient_record_edit")

    def confirm_locked_folder_notice(self):
        if self.current_record:
            self.sub_pages["patient_record_history"].set_record(self.current_record)
        self.show_sub_page("patient_record_history")

    def load_prescription_patient(self, patient_id):
        try:
            self.current_prescription_patient = self.prescription_repository.get_patient_bundle(patient_id)
        except ValueError as error:
            messagebox.showerror("Patient unavailable", str(error))
            return

        self.sub_pages["prescription_patient_details"].set_patient_bundle(self.current_prescription_patient)
        self.show_sub_page("prescription_patient_details")

    def start_medicine_search(self):
        if not self.current_prescription_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before creating a prescription.")
            return

        self.selected_medicine = None
        self.blocked_medicine = None
        self.sub_pages["medicine_search"].reset()
        self.show_sub_page("medicine_search")

    def show_medicine_results(self, medicines):
        self.sub_pages["medicine_selection"].set_medicines(medicines)
        self.show_sub_page("medicine_selection")

    def select_medicine(self, medicine):
        if not self.current_prescription_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before selecting medicine.")
            return

        self.selected_medicine = medicine
        patient_id = self.current_prescription_patient["patient"]["patient_id"]
        warnings = self.prescription_repository.check_medicine_safety(patient_id, medicine)
        if warnings:
            self.blocked_medicine = medicine
            self.selected_medicine = None
            self.sub_pages["prescription_safety_warning"].set_warning(medicine, warnings)
            self.show_sub_page("prescription_safety_warning")
            return

        self.sub_pages["prescription_form"].set_context(
            self.current_prescription_patient,
            medicine,
            [],
        )
        self.show_sub_page("prescription_form")

    def confirm_prescription_safety_warning(self):
        if not self.current_prescription_patient or not self.blocked_medicine:
            messagebox.showerror("Medicine unavailable", "Select a medicine before searching alternatives.")
            return

        patient_id = self.current_prescription_patient["patient"]["patient_id"]
        doctor_name = getattr(self.controller, "current_user_name", "Doctor")
        alternatives = self.prescription_repository.find_alternative_medicines(
            patient_id,
            self.blocked_medicine,
            doctor_name,
        )
        self.sub_pages["medicine_selection"].set_medicines(alternatives)
        self.show_sub_page("medicine_selection")

    def renew_prescription(self, prescription_log):
        if not self.current_prescription_patient:
            messagebox.showerror("Patient unavailable", "Search for a patient before renewing a prescription.")
            return

        medicine = self.prescription_repository.get_medicine_by_id(prescription_log.get("medicine_id", ""))
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
        self.sub_pages["prescription_form"].set_context(
            self.current_prescription_patient,
            medicine,
            [],
            initial_values=initial_values,
            back_page="prescription_patient_details",
        )
        self.show_sub_page("prescription_form")

    def submit_prescription(self, prescription):
        if not self.current_prescription_patient or not self.selected_medicine:
            messagebox.showerror("Prescription unavailable", "Select a patient and medicine before submitting.")
            return

        patient_id = self.current_prescription_patient["patient"]["patient_id"]
        doctor_name = getattr(self.controller, "current_user_name", "Doctor")
        saved, result = self.prescription_repository.create_prescription(
            patient_id,
            doctor_name,
            self.selected_medicine,
            prescription,
        )
        if not saved:
            messagebox.showerror("Invalid prescription", result)
            return

        self.current_prescription_patient = self.prescription_repository.get_patient_bundle(patient_id)
        self.sub_pages["prescription_success"].set_prescription_id(result)
        self.show_sub_page("prescription_success")

    def return_to_prescription_patient(self):
        if self.current_prescription_patient:
            self.sub_pages["prescription_patient_details"].set_patient_bundle(self.current_prescription_patient)
        self.show_sub_page("prescription_patient_details")

    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except Exception:
            self.controller.show_login(user_name="")


class DoctorCentralMenu(CentralMenu):
    def __init__(self, parent, portal):
        super().__init__(
            parent,
            portal,
            user_t="DOC",
            tile_commands={
                "Prescription Issuance": portal.start_prescription_flow,
                "Patient Record Processing": portal.start_patient_record_flow,
            },
        )
