from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox


CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"
SUCCESS_GREEN = "#15803D"
ERROR_RED = "#B91C1C"


class PatientRecordSearchFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Patient Medical Record Management",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3D59AB",
        ).pack(pady=(20, 10))
        ctk.CTkLabel(
            self,
            text="Search by patient ID, name, email, or phone number.",
            font=ctk.CTkFont(size=15),
            text_color=TEXT_MUTE,
        ).pack(pady=(0, 30))

        card = ctk.CTkFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", padx=120, pady=20)
        card.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            card,
            placeholder_text="Example: P001 or David Williams",
            height=45,
            border_width=1,
            corner_radius=8,
        )
        self.search_entry.grid(row=0, column=0, padx=24, pady=24, sticky="ew")

        search_button = ctk.CTkButton(
            card,
            text="Search Patient",
            height=45,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.handle_search,
        )
        search_button.grid(row=0, column=1, padx=(0, 24), pady=24)

        back_button = ctk.CTkButton(
            self,
            text="Back to Doctor Menu",
            width=180,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=lambda: self.portal.show_sub_page("menu"),
        )
        back_button.pack(pady=20)

    def reset(self):
        self.search_entry.delete(0, "end")

    def handle_search(self):
        patient = self.portal.record_repository.search_patient(self.search_entry.get())
        if not patient:
            messagebox.showerror("Patient not found", "No patient matched the search criteria.")
            return
        self.portal.load_patient_record(patient["patient_id"])


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

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Edit Medical Folder",
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.open_record_editor,
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
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=24, pady=(24, 8))

    def _add_row(self, label, value):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=3)
        row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row, text=f"{label}:", width=170, anchor="w", text_color=TEXT_MUTE).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row, text=str(value), anchor="w", justify="left", text_color=TEXT_DARK, wraplength=800).grid(row=0, column=1, sticky="ew")

    def _add_records(self, records, fields):
        if not records:
            self._add_row("Records", "No records available.")
            return

        for record in records:
            value = " | ".join(str(record.get(field, "")) for field in fields)
            self._add_row(record.get(fields[0], "Record"), value)


class PatientRecordEditFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.record = None
        self.entries = {}
        self.text_fields = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Edit Medical Folder",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3D59AB",
        ).grid(row=0, column=0, sticky="w", pady=(10, 20))

        self.form = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        self.form.grid(row=1, column=0, sticky="nsew")
        self.form.grid_columnconfigure(1, weight=1)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Cancel",
            width=120,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=self.portal.cancel_record_edit,
        ).grid(row=0, column=1, padx=(0, 12))

        ctk.CTkButton(
            actions,
            text="Submit Changes",
            width=160,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.handle_submit,
        ).grid(row=0, column=2)

    def set_record(self, record):
        self.record = record
        self.entries = {}
        self.text_fields = {}

        for widget in self.form.winfo_children():
            widget.destroy()

        folder = record["folder"]
        patient = record["patient"]
        ctk.CTkLabel(
            self.form,
            text=f"{patient.get('first_name', '')} {patient.get('last_name', '')} ({patient.get('patient_id', '')})",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_DARK,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(24, 16))

        fields = [
            ("blood_type", "Blood Type"),
            ("allergies", "Allergies"),
            ("chronic_conditions", "Chronic Conditions"),
            ("current_medications", "Current Medications"),
        ]

        row_index = 1
        for key, label in fields:
            self._add_entry(row_index, key, label, folder.get(key, ""))
            row_index += 1

        self._add_textbox(row_index, "diagnosis", "Diagnosis", folder.get("diagnosis", ""))
        row_index += 1
        self._add_textbox(row_index, "notes", "Notes", folder.get("notes", ""))

    def _add_entry(self, row, key, label, value):
        ctk.CTkLabel(self.form, text=label, text_color=TEXT_MUTE, anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        entry = ctk.CTkEntry(self.form, height=40)
        entry.insert(0, value)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.entries[key] = entry

    def _add_textbox(self, row, key, label, value):
        ctk.CTkLabel(self.form, text=label, text_color=TEXT_MUTE, anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        textbox = ctk.CTkTextbox(self.form, height=110)
        textbox.insert("1.0", value)
        textbox.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.text_fields[key] = textbox

    def handle_submit(self):
        updates = {key: entry.get() for key, entry in self.entries.items()}
        updates.update({key: textbox.get("1.0", "end").strip() for key, textbox in self.text_fields.items()})
        self.portal.save_record_edits(updates)


class PatientRecordSuccessFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Medical Folder Saved",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=SUCCESS_GREEN,
        ).pack(pady=(120, 12))
        ctk.CTkLabel(
            self,
            text="The patient's medical folder was updated successfully.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_DARK,
        ).pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Medical History",
            width=220,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.return_to_saved_record,
        ).pack()


class PatientRecordValidationFailureFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Validation Failed",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=ERROR_RED,
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The edited medical folder data could not be validated.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_DARK,
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Edit Form",
            width=220,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.confirm_validation_failure,
        ).pack()

    def set_message(self, message):
        self.message_label.configure(text=message)


class PatientRecordLockedFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Medical Folder Unavailable",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=ERROR_RED,
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The medical folder is already locked by another doctor.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_DARK,
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Medical History",
            width=240,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.confirm_locked_folder_notice,
        ).pack()

    def set_message(self, message):
        self.message_label.configure(text=message)
