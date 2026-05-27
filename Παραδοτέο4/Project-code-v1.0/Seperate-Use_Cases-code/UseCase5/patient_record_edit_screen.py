from __future__ import annotations

import customtkinter as ctk


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

        self.form = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0",
        )
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
            command=self.portal.patient_record_controller.cancel_edit,
        ).grid(row=0, column=1, padx=(0, 12))

        ctk.CTkButton(
            actions,
            text="Submit Changes",
            width=160,
            height=42,
            fg_color="#2563EB",
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
            text_color="#1E293B",
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
        ctk.CTkLabel(self.form, text=label, text_color="#64748B", anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        entry = ctk.CTkEntry(self.form, height=40)
        entry.insert(0, value)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.entries[key] = entry

    def _add_textbox(self, row, key, label, value):
        ctk.CTkLabel(self.form, text=label, text_color="#64748B", anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        textbox = ctk.CTkTextbox(self.form, height=110)
        textbox.insert("1.0", value)
        textbox.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.text_fields[key] = textbox

    def handle_submit(self):
        updates = {key: entry.get() for key, entry in self.entries.items()}
        updates.update({key: textbox.get("1.0", "end").strip() for key, textbox in self.text_fields.items()})
        self.portal.patient_record_controller.save_edits(updates)
