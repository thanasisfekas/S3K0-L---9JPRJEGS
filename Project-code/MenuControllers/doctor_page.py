from __future__ import annotations

import sys
from pathlib import Path

import customtkinter as ctk

USE_CASES_DIR = Path(__file__).resolve().parents[1] / "Seperate-Use_Cases-code"
if str(USE_CASES_DIR) not in sys.path:
    sys.path.append(str(USE_CASES_DIR))

from MenuControllers.centralMenu import CentralMenu
import uc5.patient_record_pages as patient_record_pages
import uc6.prescription_pages as prescription_pages
from uc5.medical_record_repository import PatientRecordRepository
from uc5.patient_record_controller import PatientRecordController
from uc6.prescription_controller import PrescriptionController
from uc6.prescription_repository import PrescriptionRepository

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"


class DoctorPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.record_repository = PatientRecordRepository()
        self.prescription_repository = PrescriptionRepository()
        self.patient_record_controller = PatientRecordController(self, self.record_repository)
        self.prescription_controller = PrescriptionController(self, self.prescription_repository)
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
            "patient_record_search": patient_record_pages.PatientRecordSearchFrame(self.container, self),
            "patient_record_history": patient_record_pages.PatientRecordHistoryFrame(self.container, self),
            "patient_record_edit": patient_record_pages.PatientRecordEditFrame(self.container, self),
            "patient_record_success": patient_record_pages.PatientRecordSuccessFrame(self.container, self),
            "patient_record_validation_failure": patient_record_pages.PatientRecordValidationFailureFrame(self.container, self),
            "patient_record_locked": patient_record_pages.PatientRecordLockedFrame(self.container, self),
            "prescription_patient_search": prescription_pages.PrescriptionPatientSearchFrame(self.container, self),
            "prescription_patient_details": prescription_pages.PrescriptionPatientDetailsFrame(self.container, self),
            "medicine_search": prescription_pages.MedicineSearchFrame(self.container, self),
            "medicine_selection": prescription_pages.MedicineSelectionFrame(self.container, self),
            "prescription_form": prescription_pages.PrescriptionFormFrame(self.container, self),
            "prescription_safety_warning": prescription_pages.PrescriptionSafetyWarningFrame(self.container, self),
            "prescription_success": prescription_pages.PrescriptionSuccessFrame(self.container, self),
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
                "Prescription Issuance": portal.prescription_controller.start_flow,
                "Patient Record Processing": portal.patient_record_controller.start_flow,
            },
        )
