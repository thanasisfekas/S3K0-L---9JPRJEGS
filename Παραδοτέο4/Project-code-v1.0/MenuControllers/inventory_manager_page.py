from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path

import customtkinter as ctk

from MenuControllers.centralMenu import CentralMenu

USE_CASES_DIR = Path(__file__).resolve().parents[1] / "Seperate-Use_Cases-code"
if str(USE_CASES_DIR) not in sys.path:
    sys.path.append(str(USE_CASES_DIR))

from UseCase3.controllers import InvMgMainMenuController

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"


class EmbeddedUseCaseFrame(tk.Frame):
    def title(self, *_args, **_kwargs):
        return None

    def geometry(self, *_args, **_kwargs):
        return None


class InventoryManagerPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.inventory_order_controller = None
        self.configure(fg_color=BG_COLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="Vitalink | Inventory Manager Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.order_inventory_page = ctk.CTkFrame(self.container, fg_color="transparent")
        self.order_inventory_page.grid_columnconfigure(0, weight=1)
        self.order_inventory_page.grid_rowconfigure(1, weight=1)

        self.order_back_button = ctk.CTkButton(
            self.order_inventory_page,
            text="Back to Menu",
            width=120,
            fg_color="transparent",
            text_color=ACCENT_BLUE,
            command=self.return_to_menu,
        )
        self.order_back_button.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.order_inventory_host = EmbeddedUseCaseFrame(self.order_inventory_page, bg="#ffffff", highlightthickness=0)
        self.order_inventory_host.grid(row=1, column=0, sticky="nsew")

        self.sub_pages = {
            "menu": InvManagerCentralMenu(self.container, self),
            "order_inventory": self.order_inventory_page,
        }

        for sp in self.sub_pages.values():
            sp.grid(row=0, column=0, sticky="nsew")

        self.show_sub_page("menu")

        self.btn_logout = ctk.CTkButton(
            self,
            text="Logout",
            width=100,
            fg_color="transparent",
            text_color="#800000",
            hover_color="#DC143C",
            command=self.handle_logout,
        )
        self.btn_logout.place(relx=0.02, rely=0.95, anchor="sw")
        self.btn_logout.lift()

    def show_sub_page(self, name):
        self.sub_pages[name].tkraise()

    def start_order_inventory_flow(self):
        self.show_sub_page("order_inventory")
        self._clear_order_inventory_host()
        self.inventory_order_controller = InvMgMainMenuController(self.order_inventory_host)

    def return_to_menu(self):
        self._clear_order_inventory_host()
        self.show_sub_page("menu")

    def _clear_order_inventory_host(self):
        for widget in self.order_inventory_host.winfo_children():
            widget.destroy()

    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except Exception:
            self.controller.show_login(user_name="")


class InvManagerCentralMenu(CentralMenu):
    def __init__(self, parent, portal):
        super().__init__(
            parent,
            portal,
            user_t="INV",
            tile_commands={
                "Order of Equipment and Medicines": portal.start_order_inventory_flow,
            },
        )
