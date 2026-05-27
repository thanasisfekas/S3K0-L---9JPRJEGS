from __future__ import annotations

import customtkinter as ctk



class PatientRecordValidationFailureFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Validation Failed",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#B91C1C",
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The edited medical folder data could not be validated.",
            font=ctk.CTkFont(size=16),
            text_color="#1E293B",
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Edit Form",
            width=220,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.patient_record_controller.confirm_validation_failure,
        ).pack()

    def set_message(self, message):
        self.message_label.configure(text=message)

