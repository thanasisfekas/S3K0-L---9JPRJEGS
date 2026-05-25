from __future__ import annotations

import customtkinter as ctk



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
            text_color="#64748B",
        ).pack(pady=(0, 30))

        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
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
            fg_color="#2563EB",
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
        self.portal.prescription_controller.search_patient(self.search_entry.get())

