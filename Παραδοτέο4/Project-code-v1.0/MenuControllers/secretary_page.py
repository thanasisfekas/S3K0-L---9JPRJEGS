from __future__ import annotations
import json
import sys
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox
from MenuControllers.centralMenu import CentralMenu
from data_paths import data_path

USE_CASES_DIR = Path(__file__).resolve().parents[1] / "Seperate-Use_Cases-code"
UC9_DIR = USE_CASES_DIR / "UseCase9"
UC9_CONTROLLERS_DIR = UC9_DIR / "Bill_Issue" / "Controllers"
UC10_DIR = USE_CASES_DIR / "UseCase10"
UC10_CONTROLLERS_DIR = UC10_DIR / "Surgery_Appoint" / "Controllers"

for use_case_path in (UC9_DIR, UC9_CONTROLLERS_DIR, UC10_DIR, UC10_CONTROLLERS_DIR):
    if str(use_case_path) not in sys.path:
        sys.path.append(str(use_case_path))

from search_patient_charges_controller import SearchChargesController
from surgery_search_controller import SurgerySearchController
from surgery_request_controller import SurgeryRequestController

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


class SecretaryPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.account_statement_controller = None
        self.surgery_search_controller = None
        self.surgery_request_controller = None
        self.configure(fg_color=BG_COLOR)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink | Secretary Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.account_statement_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.account_statement_page.grid_columnconfigure(0, weight=1)
        self.account_statement_page.grid_rowconfigure(1, weight=1)

        self.account_back_button = ctk.CTkButton(
            self.account_statement_page,
            text="Back to Menu",
            width=120,
            fg_color="transparent",
            text_color=ACCENT_BLUE,
            command=self.return_to_menu,
        )
        self.account_back_button.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.account_statement_host = EmbeddedUseCaseFrame(self.account_statement_page, bg="#ffffff", highlightthickness=0)
        self.account_statement_host.grid(row=1, column=0, sticky="nsew")

        self.surgery_scheduling_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.surgery_scheduling_page.grid_columnconfigure(0, weight=1)
        self.surgery_scheduling_page.grid_rowconfigure(1, weight=1)

        self.surgery_back_button = ctk.CTkButton(
            self.surgery_scheduling_page,
            text="Back to Menu",
            width=120,
            fg_color="transparent",
            text_color=ACCENT_BLUE,
            command=self.return_to_menu,
        )
        self.surgery_back_button.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.surgery_scheduling_host = EmbeddedUseCaseFrame(self.surgery_scheduling_page, bg="#ffffff", highlightthickness=0)
        self.surgery_scheduling_host.grid(row=1, column=0, sticky="nsew")

        self.sub_pages = {
            "menu": SecretaryCentralMenu(self.container, self),
            "account_statement": self.account_statement_page,
            "surgery_scheduling": self.surgery_scheduling_page}
        
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
        self.sub_pages[name].tkraise()

    def start_account_statement_flow(self):
        self.show_sub_page("account_statement")
        self._clear_account_statement_host()
        self.account_statement_controller = SearchChargesController(
            self.account_statement_host,
            data_path("patients.csv"),
        )
        self.account_statement_controller.display_search_screen()

    def start_surgery_scheduling_flow(self):
        self.show_sub_page("surgery_scheduling")
        self._clear_surgery_scheduling_host()
        self.surgery_search_controller = SurgerySearchController(
            root=self.surgery_scheduling_host,
            on_back_click=None,
        )
        self.surgery_request_controller = SurgeryRequestController(
            root=self.surgery_scheduling_host,
            on_back_click=self.return_to_menu,
            search_controller=self.surgery_search_controller,
        )
        self.surgery_search_controller.on_back_click = self.surgery_request_controller.display_surgery_requests
        self.surgery_request_controller.display_surgery_requests()

    def return_to_menu(self):
        self._clear_account_statement_host()
        self._clear_surgery_scheduling_host()
        self.show_sub_page("menu")

    def _clear_account_statement_host(self):
        for widget in self.account_statement_host.winfo_children():
            widget.destroy()

    def _clear_surgery_scheduling_host(self):
        for widget in self.surgery_scheduling_host.winfo_children():
            widget.destroy()

    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except:
            self.controller.show_login(user_name="")


class SecretaryCentralMenu(CentralMenu):
    def __init__(self, parent, portal):
        super().__init__(
            parent,
            portal,
            user_t="SECRETARY",
            tile_commands={
                "Account statement Issuance": portal.start_account_statement_flow,
                "Surgery Scheduling": portal.start_surgery_scheduling_flow,
            },
        )
