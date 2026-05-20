from __future__ import annotations
import json
import sys
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox
from MenuControllers.centralMenu import CentralMenu

UC7_DIR = Path(__file__).resolve().parents[1] / "Seperate-Use_Cases-code" / "uc7"
if str(UC7_DIR) not in sys.path:
    sys.path.append(str(UC7_DIR))

from memberSearchController import MemberSearchController

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


class HRManagerPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.shift_assignment_controller = None
        self.configure(fg_color=BG_COLOR)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink | HR Manager Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)
       
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        
        self.shift_assignment_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.shift_assignment_page.grid_columnconfigure(0, weight=1)
        self.shift_assignment_page.grid_rowconfigure(1, weight=1)

        self.shift_back_button = ctk.CTkButton(
            self.shift_assignment_page,
            text="Back to Menu",
            width=120,
            fg_color="transparent",
            text_color=ACCENT_BLUE,
            command=self.return_to_menu,
        )
        self.shift_back_button.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.shift_assignment_host = EmbeddedUseCaseFrame(self.shift_assignment_page, bg="#ffffff", highlightthickness=0)
        self.shift_assignment_host.grid(row=1, column=0, sticky="nsew")

        self.sub_pages = {
            "menu": HRManagerCentralMenu(self.container, self),
            "shift_assignment": self.shift_assignment_page}
        
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

    def start_shift_assignment_flow(self):
        self.show_sub_page("shift_assignment")
        self._clear_shift_assignment_host()
        self.shift_assignment_controller = MemberSearchController(self.shift_assignment_host)
        self.shift_assignment_controller.displaySearchScreen()

    def return_to_menu(self):
        self._clear_shift_assignment_host()
        self.show_sub_page("menu")

    def _clear_shift_assignment_host(self):
        for widget in self.shift_assignment_host.winfo_children():
            widget.destroy()

    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except:
            self.controller.show_login(user_name="")


class HRManagerCentralMenu(CentralMenu):
    def __init__(self,parent,portal):
        super().__init__(
            parent,
            portal,
            user_t="HR",
            tile_commands={
                "Shift and Staff Assignment": portal.start_shift_assignment_flow,
            },
        )

