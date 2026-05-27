from __future__ import annotations

import customtkinter as ctk


class PrescriptionFormFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.entries = {}
        self.back_page = "medicine_selection"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Prescription Form",
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
            text="Back",
            width=120,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=self.handle_back,
        ).grid(row=0, column=1, padx=(0, 12))

        ctk.CTkButton(
            actions,
            text="Submit Prescription",
            width=180,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.handle_submit,
        ).grid(row=0, column=2)

    def set_context(self, patient_bundle, medicine, warnings, initial_values=None, back_page="medicine_selection"):
        self.entries = {}
        self.back_page = back_page
        initial_values = initial_values or {}
        for widget in self.form.winfo_children():
            widget.destroy()

        patient = patient_bundle["patient"]
        ctk.CTkLabel(
            self.form,
            text=f"{patient.get('first_name', '')} {patient.get('last_name', '')} ({patient.get('patient_id', '')})",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1E293B",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            self.form,
            text=f"{medicine.get('name', '')} | {medicine.get('form', '')} | {medicine.get('strength', '')}",
            text_color="#64748B",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 16))

        row_index = 2
        if warnings:
            ctk.CTkLabel(
                self.form,
                text="Safety warning: " + " ".join(warnings),
                text_color="#B91C1C",
                wraplength=850,
                justify="left",
            ).grid(row=row_index, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 16))
            row_index += 1

        for key, label, placeholder in [
            ("dosage", "Dosage", "Example: 500mg"),
            ("frequency", "Frequency", "Example: twice daily"),
            ("duration", "Duration", "Example: 7 days"),
        ]:
            self._add_entry(row_index, key, label, placeholder, initial_values.get(key, ""))
            row_index += 1

        self._add_textbox(
            row_index,
            "instructions",
            "Instructions",
            "Enter instructions for the patient",
            initial_values.get("instructions", ""),
        )

    def _add_entry(self, row, key, label, placeholder, value):
        ctk.CTkLabel(self.form, text=label, text_color="#64748B", anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        entry = ctk.CTkEntry(self.form, placeholder_text=placeholder, height=40)
        if value:
            entry.insert(0, value)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.entries[key] = entry

    def _add_textbox(self, row, key, label, placeholder, value):
        ctk.CTkLabel(self.form, text=label, text_color="#64748B", anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        textbox = ctk.CTkTextbox(self.form, height=120)
        if value:
            textbox.insert("1.0", value)
        textbox.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.entries[key] = textbox

    def handle_back(self):
        self.portal.show_sub_page(self.back_page)

    def handle_submit(self):
        prescription = {}
        for key, widget in self.entries.items():
            if isinstance(widget, ctk.CTkTextbox):
                prescription[key] = widget.get("1.0", "end").strip()
            else:
                prescription[key] = widget.get()
        self.portal.prescription_controller.submit_prescription(prescription)
