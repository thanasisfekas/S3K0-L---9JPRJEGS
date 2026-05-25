from __future__ import annotations

import customtkinter as ctk



class PrescriptionSuccessFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal
        self.prescription_id = ""

        self.title_label = ctk.CTkLabel(
            self,
            text="Prescription Issued",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#15803D",
        )
        self.title_label.pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The prescription was saved successfully.",
            font=ctk.CTkFont(size=16),
            text_color="#1E293B",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Patient Details",
            width=220,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.prescription_controller.return_to_patient,
        ).pack()

    def set_prescription_id(self, prescription_id):
        self.prescription_id = prescription_id
        self.message_label.configure(text=f"Prescription {prescription_id} was saved successfully.")

