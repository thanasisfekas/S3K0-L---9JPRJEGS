from __future__ import annotations

import customtkinter as ctk



class PatientRecordSuccessFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Medical Folder Saved",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#15803D",
        ).pack(pady=(120, 12))
        ctk.CTkLabel(
            self,
            text="The patient's medical folder was updated successfully.",
            font=ctk.CTkFont(size=16),
            text_color="#1E293B",
        ).pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Medical History",
            width=220,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.patient_record_controller.return_to_saved_record,
        ).pack()

