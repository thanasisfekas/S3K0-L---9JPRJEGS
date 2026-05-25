from __future__ import annotations

import customtkinter as ctk


class PrescriptionPatientDetailsFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Patient Prescription History",
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
            command=lambda: self.portal.show_sub_page("prescription_patient_search"),
        ).grid(row=0, column=1, sticky="e")

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
            text="Create New Prescription",
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.prescription_controller.start_medicine_search,
        ).grid(row=0, column=1, sticky="e")

    def set_patient_bundle(self, bundle):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        patient = bundle["patient"]
        self._add_section("Patient")
        self._add_row("Patient ID", patient.get("patient_id", ""))
        self._add_row("Name", f"{patient.get('first_name', '')} {patient.get('last_name', '')}")
        self._add_row("Birth Date", patient.get("date_of_birth", ""))
        self._add_row("Contact", patient.get("contact_number", ""))

        self._add_section("Prescription Log")
        logs = bundle["prescription_logs"]
        if not logs:
            self._add_row("History", "No prescriptions have been issued for this patient.")
            return

        for log in logs:
            self._add_prescription_log_row(log)

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

    def _add_prescription_log_row(self, log):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=6)
        row.grid_columnconfigure(1, weight=1)

        value = (
            f"{log.get('medicine_name', '')} | {log.get('dosage', '')} | "
            f"{log.get('frequency', '')} | {log.get('duration', '')} | "
            f"{log.get('created_at', '')}"
        )
        ctk.CTkLabel(
            row,
            text=f"{log.get('prescription_id', 'Prescription')}:",
            width=170,
            anchor="w",
            text_color="#64748B",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            row,
            text=value,
            anchor="w",
            justify="left",
            text_color="#1E293B",
            wraplength=700,
        ).grid(row=0, column=1, sticky="ew")
        ctk.CTkButton(
            row,
            text="Renew",
            width=90,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=lambda selected=log: self.portal.prescription_controller.renew_prescription(selected),
        ).grid(row=0, column=2, padx=(16, 0))
