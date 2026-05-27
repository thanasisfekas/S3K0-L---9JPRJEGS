from __future__ import annotations

import customtkinter as ctk


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

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0",
        )
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

    def set_medicines(self, medicines):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        if not medicines:
            ctk.CTkLabel(
                self.scroll,
                text="No safe alternative medicines were found for this patient.",
                text_color="#64748B",
                font=ctk.CTkFont(size=15),
            ).pack(anchor="w", padx=24, pady=24)
            return

        for medicine in medicines:
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", padx=24, pady=10)
            row.grid_columnconfigure(0, weight=1)

            title = f"{medicine.get('name', '')} ({medicine.get('active_substance', '')})"
            subtitle = f"{medicine.get('category', '')} | {medicine.get('form', '')} | {medicine.get('strength', '')}"
            ctk.CTkLabel(row, text=title, anchor="w", text_color="#1E293B", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky="ew")
            ctk.CTkLabel(row, text=subtitle, anchor="w", text_color="#64748B").grid(row=1, column=0, sticky="ew")

            ctk.CTkButton(
                row,
                text="Select",
                width=100,
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                command=lambda selected=medicine: self.portal.prescription_controller.select_medicine(selected),
            ).grid(row=0, column=1, rowspan=2, padx=(16, 0))
