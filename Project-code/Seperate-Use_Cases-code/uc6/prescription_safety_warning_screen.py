from __future__ import annotations

import customtkinter as ctk



class PrescriptionSafetyWarningFrame(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        self.portal = portal

        ctk.CTkLabel(
            self,
            text="Allergy or Contraindication Warning",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#B91C1C",
        ).pack(pady=(120, 12))

        self.message_label = ctk.CTkLabel(
            self,
            text="The selected medicine is not suitable for this patient.",
            font=ctk.CTkFont(size=16),
            text_color="#1E293B",
            wraplength=760,
            justify="center",
        )
        self.message_label.pack(pady=(0, 30))

        ctk.CTkButton(
            self,
            text="Show Alternative Medicines",
            width=260,
            height=42,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.portal.prescription_controller.confirm_safety_warning,
        ).pack()

    def set_warning(self, medicine, warnings):
        message = (
            f"{medicine.get('name', 'Selected medicine')} cannot be prescribed safely. "
            + " ".join(warnings)
        )
        self.message_label.configure(text=message)
