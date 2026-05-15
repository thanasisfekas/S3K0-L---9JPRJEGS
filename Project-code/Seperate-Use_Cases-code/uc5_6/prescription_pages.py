from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox


CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"
SUCCESS_GREEN = "#15803D"
WARNING_RED = "#B91C1C"


class PrescriptionPatientSearchFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Prescription Issuance",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3D59AB",
        ).pack(pady=(20, 10))
        ctk.CTkLabel(
            self,
            text="Search for the patient who needs a prescription.",
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

        ctk.CTkButton(
            card,
            text="Search Patient",
            height=45,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.handle_search,
        ).grid(row=0, column=1, padx=(0, 24), pady=24)

        ctk.CTkButton(
            self,
            text="Back to Doctor Menu",
            width=180,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=lambda: self.portal.show_sub_page("menu"),
        ).pack(pady=20)

    def reset(self):
        self.search_entry.delete(0, "end")

    def handle_search(self):
        patient = self.portal.prescription_repository.search_patient(self.search_entry.get())
        if not patient:
            messagebox.showerror("Patient not found", "No patient matched the search criteria.")
            return
        self.portal.load_prescription_patient(patient["patient_id"])


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

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="Create New Prescription",
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.start_medicine_search,
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
            text_color=TEXT_DARK,
        ).pack(anchor="w", padx=24, pady=(24, 8))

    def _add_row(self, label, value):
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=3)
        row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row, text=f"{label}:", width=170, anchor="w", text_color=TEXT_MUTE).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row, text=str(value), anchor="w", justify="left", text_color=TEXT_DARK, wraplength=800).grid(row=0, column=1, sticky="ew")

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
            text_color=TEXT_MUTE,
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            row,
            text=value,
            anchor="w",
            justify="left",
            text_color=TEXT_DARK,
            wraplength=700,
        ).grid(row=0, column=1, sticky="ew")
        ctk.CTkButton(
            row,
            text="Renew",
            width=90,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=lambda selected=log: self.portal.renew_prescription(selected),
        ).grid(row=0, column=2, padx=(16, 0))


class MedicineSearchFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Medicine Search",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3D59AB",
        ).pack(pady=(20, 10))
        ctk.CTkLabel(
            self,
            text="Only medicines allowed for your specialty will appear.",
            font=ctk.CTkFont(size=15),
            text_color=TEXT_MUTE,
        ).pack(pady=(0, 30))

        card = ctk.CTkFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        card.pack(fill="x", padx=120, pady=20)
        card.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            card,
            placeholder_text="Search medicine, category, or active substance",
            height=45,
            border_width=1,
            corner_radius=8,
        )
        self.search_entry.grid(row=0, column=0, padx=24, pady=24, sticky="ew")

        ctk.CTkButton(
            card,
            text="Search Medicine",
            height=45,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.handle_search,
        ).grid(row=0, column=1, padx=(0, 24), pady=24)

        ctk.CTkButton(
            self,
            text="Back to Patient Details",
            width=200,
            fg_color="transparent",
            text_color="#3D59AB",
            hover_color="#E0F2FE",
            command=lambda: self.portal.show_sub_page("prescription_patient_details"),
        ).pack(pady=20)

    def reset(self):
        self.search_entry.delete(0, "end")

    def handle_search(self):
        doctor_name = getattr(self.portal.controller, "current_user_name", "Doctor")
        medicines = self.portal.prescription_repository.search_medicines(self.search_entry.get(), doctor_name)
        if not medicines:
            messagebox.showinfo("No medicines", "No allowed medicines matched the search criteria.")
            return
        self.portal.show_medicine_results(medicines)


class MedicineSelectionFrame(ctk.CTkFrame):
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
            text="Medicine Selection",
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
            command=lambda: self.portal.show_sub_page("medicine_search"),
        ).grid(row=0, column=1, sticky="e")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

    def set_medicines(self, medicines):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        if not medicines:
            ctk.CTkLabel(
                self.scroll,
                text="No safe alternative medicines were found for this patient.",
                text_color=TEXT_MUTE,
                font=ctk.CTkFont(size=15),
            ).pack(anchor="w", padx=24, pady=24)
            return

        for medicine in medicines:
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=10)
            row.grid_columnconfigure(0, weight=1)

            title = f"{medicine.get('name', '')} ({medicine.get('active_substance', '')})"
            subtitle = f"{medicine.get('category', '')} | {medicine.get('form', '')} | {medicine.get('strength', '')}"
            ctk.CTkLabel(row, text=title, anchor="w", text_color=TEXT_DARK, font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky="ew")
            ctk.CTkLabel(row, text=subtitle, anchor="w", text_color=TEXT_MUTE).grid(row=1, column=0, sticky="ew")

            ctk.CTkButton(
                row,
                text="Select",
                width=100,
                fg_color=ACCENT_BLUE,
                hover_color="#1D4ED8",
                command=lambda selected=medicine: self.portal.select_medicine(selected),
            ).grid(row=0, column=1, rowspan=2, padx=(16, 0))


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

        self.form = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, corner_radius=12, border_width=1, border_color="#E2E8F0")
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
            fg_color=ACCENT_BLUE,
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
            text_color=TEXT_DARK,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(24, 8))
        ctk.CTkLabel(
            self.form,
            text=f"{medicine.get('name', '')} | {medicine.get('form', '')} | {medicine.get('strength', '')}",
            text_color=TEXT_MUTE,
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 16))

        row_index = 2
        if warnings:
            ctk.CTkLabel(
                self.form,
                text="Safety warning: " + " ".join(warnings),
                text_color=WARNING_RED,
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
        ctk.CTkLabel(self.form, text=label, text_color=TEXT_MUTE, anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
        entry = ctk.CTkEntry(self.form, placeholder_text=placeholder, height=40)
        if value:
            entry.insert(0, value)
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 24), pady=10)
        self.entries[key] = entry

    def _add_textbox(self, row, key, label, placeholder, value):
        ctk.CTkLabel(self.form, text=label, text_color=TEXT_MUTE, anchor="w").grid(row=row, column=0, sticky="nw", padx=24, pady=10)
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
        self.portal.submit_prescription(prescription)


class PrescriptionSuccessFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.prescription_id = ""

        self.title_label = ctk.CTkLabel(
            self,
            text="Prescription Issued",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=SUCCESS_GREEN,
        )
        self.title_label.pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The prescription was saved successfully.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_DARK,
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Patient Details",
            width=220,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.return_to_prescription_patient,
        ).pack()

    def set_prescription_id(self, prescription_id):
        self.prescription_id = prescription_id
        self.message_label.configure(text=f"Prescription {prescription_id} was saved successfully.")


class PrescriptionSafetyWarningFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Allergy or Contraindication Warning",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=WARNING_RED,
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The selected medicine is not suitable for this patient.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_DARK,
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Show Alternative Medicines",
            width=260,
            height=42,
            fg_color=ACCENT_BLUE,
            hover_color="#1D4ED8",
            command=self.portal.confirm_prescription_safety_warning,
        ).pack()

    def set_warning(self, medicine, warnings):
        message = (
            f"{medicine.get('name', 'Selected medicine')} cannot be prescribed safely. "
            + " ".join(warnings)
        )
        self.message_label.configure(text=message)
