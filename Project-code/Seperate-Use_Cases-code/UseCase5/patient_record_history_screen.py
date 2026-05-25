from __future__ import annotations

import customtkinter as ctk


class PatientRecordHistoryFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.record = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Patient Medical History",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3D59AB",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text="Back",
            width=100,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=lambda: self.portal.show_sub_page("patient_record_search"),
        ).grid(row=0, column=1, sticky="e", padx=(10, 0))

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0",
        )
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Edit Medical Folder",
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.patient_record_controller.open_editor,
        ).grid(row=0, column=1, sticky="e")

    def set_record(self, record):
        self.record = record
        for widget in self.scroll.winfo_children():
            widget.destroy()

        patient = record["patient"]
        folder = record["folder"]
        self._add_section("Patient")
        self._add_row("Patient ID", patient.get("patient_id", ""))
        self._add_row("Name", f"{patient.get('first_name', '')} {patient.get('last_name', '')}")
        self._add_row("Birth Date", patient.get("date_of_birth", ""))
        self._add_row("Contact", patient.get("contact_number", ""))
        self._add_row("Insurance", f"{patient.get('insurance_provider', '')} / {patient.get('insurance_number', '')}")

        self._add_section("Hospitalization Status")
        if record["hospitalization"]:
            for hospitalization in record["hospitalization"]:
                self._add_row(
                    hospitalization.get("status", "Status"),
                    f"Ward: {hospitalization.get('ward', '')} | Admission: {hospitalization.get('admission_date', '')} | Discharge: {hospitalization.get('discharge_date', '') or '-'}",
                )
        else:
            self._add_row("Status", "No hospitalization record available.")

        self._add_section("Medical Folder")
        self._add_row("Folder ID", folder.get("folder_id", ""))
        self._add_row("Blood Type", folder.get("blood_type", ""))
        self._add_row("Allergies", folder.get("allergies", ""))
        self._add_row("Chronic Conditions", folder.get("chronic_conditions", ""))
        self._add_row("Current Medications", folder.get("current_medications", ""))
        self._add_row("Diagnosis", folder.get("diagnosis", ""))
        self._add_row("Notes", folder.get("notes", ""))
        self._add_row("Last Updated", folder.get("last_updated", ""))

        self._add_section("Lab Tests")
        self._add_records(record["lab_tests"], ["lab_test_id", "test_name", "result", "status", "test_date"])

        self._add_section("Lab Test Requests")
        self._add_records(record["lab_test_requests"], ["request_id", "test_name", "reason", "status", "request_date"])

    def _add_section(self, title):
        ctk.CTkLabel(
            self.scroll,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1E293B",
        ).pack(anchor="w", padx=24, pady=(24, 8))

    def _add_row(self, label, value):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=3)
        row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row, text=f"{label}:", width=170, anchor="w", text_color="#64748B").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row, text=str(value), anchor="w", justify="left", text_color="#1E293B", wraplength=800).grid(row=0, column=1, sticky="ew")

    def _add_records(self, records, fields):
        if not records:
            self._add_row("Records", "No records available.")
            return

        for record in records:
            value = " | ".join(str(record.get(field, "")) for field in fields)
            self._add_row(record.get(fields[0], "Record"), value)
