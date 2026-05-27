from __future__ import annotations
import sys
import tkinter as tk
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox
from MenuControllers.centralMenu import CentralMenu

USE_CASES_DIR = Path(__file__).resolve().parents[1] / "Seperate-Use_Cases-code"
if str(USE_CASES_DIR) not in sys.path:
    sys.path.append(str(USE_CASES_DIR))

from UseCase1.appointment_search_controller import AppointmentSearchController
from UseCase2.bill_management_controller import BillManagementController


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"


class EmbeddedUseCaseFrame(tk.Frame):
    def title(self, *_args, **_kwargs):
        return None

    def geometry(self, *_args, **_kwargs):
        return None


class PatientPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.appointment_controller = None
        self.billing_controller = None
        self.configure(fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)

  
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.billing_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.billing_page.grid_columnconfigure(0, weight=1)
        self.billing_page.grid_rowconfigure(1, weight=1)

        self.billing_back_button = ctk.CTkButton(
            self.billing_page,
            text="Back to Menu",
            width=120,
            fg_color="transparent",
            text_color=ACCENT_BLUE,
            command=self.return_to_menu,
        )
        self.billing_back_button.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.billing_host = EmbeddedUseCaseFrame(self.billing_page, bg="#ffffff", highlightthickness=0)
        self.billing_host.grid(row=1, column=0, sticky="nsew")

        self.sub_pages = {
            "menu": PatientCentralMenu(self.container, self),
            "appointment": tk.Frame(self.container, bg="#ffffff", highlightthickness=0),
            "billing": self.billing_page,
        }
        
        for sp in self.sub_pages.values():
            sp.grid(row=0, column=0, sticky="nsew")
        
        self.show_sub_page("menu")

        self.btn_logout = ctk.CTkButton(
            self, text="\U0001F6AA Logout", width=100, fg_color="transparent", 
            text_color=	"#800000", hover_color="#DC143C",
            command=self.handle_logout
        )
        self.btn_logout.place(relx=0.02, rely=0.95, anchor="sw")
        self.btn_logout.lift()


    def show_sub_page(self, name):
        if name in self.sub_pages:
            self.sub_pages[name].tkraise()

    def start_appointment_flow(self):
        patient_id = getattr(self.controller, "current_patient_id", None)
        if not patient_id:
            messagebox.showerror("Error", "Could not find the logged-in patient ID.")
            return

        self.show_sub_page("appointment")
        appointment_page = self.sub_pages["appointment"]
        self.appointment_controller = AppointmentSearchController(
            patient_id=patient_id,
            root=appointment_page,
            back_command=self.return_to_menu,
        )
        self.appointment_controller.displaySearchAppointmentScreen()

    def start_bill_payment_flow(self):
        patient_id = getattr(self.controller, "current_patient_id", None)
        if not patient_id:
            messagebox.showerror("Error", "Could not find the logged-in patient ID.")
            return

        self.show_sub_page("billing")
        self._clear_frame(self.billing_host)
        self.billing_controller = BillManagementController(
            patient_id=patient_id,
            root=self.billing_host,
        )
        self.billing_controller.displayBillManagementScreen()

    def return_to_menu(self):
        self._clear_frame(self.sub_pages["appointment"])
        self._clear_frame(self.billing_host)
        self.show_sub_page("menu")

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    
    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except Exception:
            try:
                self.controller.show_login(user_name="")
            except Exception as e:
                messagebox.showerror("Error", f"Logout failed: {e}")

class PatientCentralMenu(CentralMenu):
    def __init__(self, parent, portal):
        super().__init__(
            parent,
            portal,
            user_t="PATIENT",
            tile_commands={
                "Schedule Appointment": portal.start_appointment_flow,
                "Bill Payment": portal.start_bill_payment_flow,
            },
        )
        
        ctk.CTkLabel(self, text="What would you like to do today?", font=ctk.CTkFont(size=16), text_color=TEXT_MUTE).pack(pady=(0, 40))


