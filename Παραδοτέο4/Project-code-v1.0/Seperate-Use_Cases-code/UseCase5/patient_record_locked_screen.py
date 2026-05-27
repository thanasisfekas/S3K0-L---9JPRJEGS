from __future__ import annotations

import customtkinter as ctk



class PatientRecordLockedFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Medical Folder Unavailable",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#B91C1C",
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The medical folder is already locked by another doctor.",
            font=ctk.CTkFont(size=16),
            text_color="#1E293B",
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Return to Medical History",
            width=240,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.patient_record_controller.confirm_locked_folder_notice,
        ).pack()

    def set_message(self, message):
        self.message_label.configure(text=message)
