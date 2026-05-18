from __future__ import annotations
import json
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox
from MenuControllers.centralMenu import CentralMenu
from uc_3.main import Inventory
from CTkTable import *
import tkinter as tk 
from tkinter import messagebox

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"


class InventoryManagerPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=BG_COLOR)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink | Inventory Manager Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.sub_pages = {
            "menu": InvManagerCentralMenu(self.container, self),
            "search": InvSearchScreen(self.container, self),
            "result": SearchResultScreen(self.container,self)
        }
        
        self.classController = InvMainMenuController(self,sub_pages=self.sub_pages)

        for sp in self.classController.sub_pages.values():
            sp.grid(row=0, column=0, sticky="nsew")
        
        self.classController.show_sub_page("menu")

        self.btn_logout = ctk.CTkButton(
            self, text="\U0001F6AA Logout", width=100, fg_color="transparent", 
            text_color=	"#800000", hover_color="#DC143C",
            command=self.classController.handle_logout
        )

        self.btn_logout.place(relx=0.02, rely=0.95, anchor="sw")
        self.btn_logout.lift()

class InvManagerCentralMenu(CentralMenu):
    def __init__(self, parent, portal):
            super().__init__(parent, portal,user_t="INV")

class InvMainMenuController:
    def __init__(self , frame , sub_pages):
        self.frame = frame
        self.sub_pages = sub_pages

    def handle_logout(self):
        try:
            self.frame.controller.show_frame("LoginPage")
        except:
            self.frame.controller.show_login(user_name="")

    # display() invmaincontroller -> invmainmenu portalframe
    def show_sub_page(self, name):
        self.sub_pages[name].tkraise()


class MessageScreen:
    def __init__(self):
        pass

    def dispError(self):
        messagebox.showerror("","Error No Item Found")
        return messagebox.askyesnocancel("","Do you want to return to list")

class InvSearchController:
    def __init__(self, parent:ctk.CTkEntry,portal):
        self.parent = parent
        self.portal = portal

    def getInvItem(self):
        usr_inp =self.parent.get()
        self.item_info = Inventory().searchInvItem(usr_inp)

        if self.item_info is None:
            # print("item not found")
            if not MessageScreen().dispError():
                self.portal.classController.show_sub_page("menu")
        else:
            result_screen = self.portal.sub_pages["menu"]
            result_screen.displayResults(self.item_info)
            self.portal.classController.show_sub_page("result")

class InvSearchScreen(ctk.CTkFrame):
    def __init__(self, parent , portal):
        super().__init__(parent)
        self.portal = portal
        self.configure(fg_color=BG_COLOR)

        self.lbl_title = ctk.CTkLabel(
            self, text="Search Inventory", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_title.pack(pady=(40, 20))

        # Search Container (To hold Entry and Button side-by-side)
        self.search_container = ctk.CTkFrame(self, fg_color="transparent")
        self.search_container.pack(fill="x", padx=100)

        # The Search Bar (Entry) - This is where user 'Enters Item Details'
        self.entry_search = ctk.CTkEntry(
            self.search_container, 
            placeholder_text="Enter equipment or medicine name...",
            height=45,
            width=400
        )
        self.entry_search.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.search_controller = InvSearchController(self.entry_search,self.portal)
        
        self.btn_search = ctk.CTkButton(
            self.search_container, 
            text="Search", 
            width=100, 
            height=45,
            command=self.search_controller.getInvItem
        )
        self.btn_search.pack(side="right")

        # Back Button to return to Central Menu
        self.btn_back = ctk.CTkButton(
            self, text="← Back to Menu", fg_color="transparent", text_color="#2563EB",
            command=lambda: self.portal.classController.show_sub_page("menu")
        )
        self.showResults()

        

    def showResults(self): 
        self.results = ctk.CTkScrollableFrame(
            self, 
            label_text="Available Items",
            fg_color=CARD_WHITE,
            height=300
        )

        self.results.pack(fill="both", expand=True, padx=100, pady=20)

        for child in self.results.winfo_children():
            child.destroy()

        df = Inventory().getAvailableInv()
        meds = df["Medicines"].loc[0]
        equip = df["Equipment"].loc[0]
        # print(meds)
        med_lb = ctk.CTkLabel(
            self.results, text="Available Medicines", 
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#dbdbdb",
            corner_radius=10
        )
        med_lb.pack(pady=(40, 20))
        table_data = [["ID", "Name", "Category", "Stock", "Expires", "Price"]]
    
    # Add the data rows
        for _, row in meds.iterrows():
            table_data.append([
            row['medicine_id'], 
            row['name'], 
            row['category'], 
            row['stock_level'], 
            row['expiry_date'], 
            f"${row['price']:.2f}"
            ])

        table = CTkTable(master=self.results, row=len(table_data), column=6, values=table_data)
        table.pack(expand=True, fill="both", padx=20, pady=20)

        equip_lb = ctk.CTkLabel(
            self.results, text="Available Equipment", 
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#dbdbdb",
            corner_radius=10
        )
        equip_lb.pack(pady=(40, 20))

        table_equip = [["ID", "Name", "Type", "Stock"]]
    
        for _, row in equip.iterrows():
            table_equip.append([
            row['equipment_id'], 
            row['name'], 
            row['type'], 
            row['stock_level'], 
            ])


        table_eq = CTkTable(master=self.results, row=len(equip), column=4, values=table_equip)
        table_eq.pack(expand=True, fill="both", padx=20, pady=20)



class SearchResultScreen(ctk.CTkFrame):
    def __init__(self,parent,portal):
        super().__init__(parent)
        self.portal = portal
        self.configure(fg_color=BG_COLOR)
    
        self.lb_title = ctk.CTkLabel(self, text="Search Results", font=ctk.CTkFont(size=24, weight="bold"))
        self.lb_title.pack(pady=20)
        self.results_area = ctk.CTkScrollableFrame(self, fg_color=CARD_WHITE, height=400)
        self.results_area.pack(fill="both", expand=True, padx=40, pady=20)

        self.btn_back = ctk.CTkButton(self, text="Back to Search", 
                                      command=lambda: self.portal.classController.show_sub_page("search"))
        self.btn_back.pack(pady=20)


    def displayResults(self,portal , item_info):
        for child in self.results_area.winfo_children():
            child.destroy()

        if "medicine_id" in item_info.columns:
            med_lb = ctk.CTkLabel(
                self.results_area, text="Medicine Info", 
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color="#dbdbdb",
                corner_radius=10
            )

            med_lb.pack(pady=(40, 20))
            table_data = [["ID", "Name", "Category", "Stock", "Expires", "Price"]]
            

            table_data.append([
            item_info['medicine_id'], 
            item_info['name'], 
            item_info['category'], 
            item_info['stock_level'], 
            item_info['expiry_date'], 
            f"${item_info['price']:.2f}"
            ])

            table = CTkTable(master=self.results, row=len(table_data), column=6, values=table_data)
            table.pack(expand=True, fill="both", padx=20, pady=20)

        elif "equipment_id" in item_info.columns:
            equip_lb = ctk.CTkLabel(
                self.results_area, text="Medicine Info", 
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color="#dbdbdb",
                corner_radius=10
            )
            equip_lb.pack(pady=(40, 20))
            table_data = [["ID", "Name", "Type", "Stock"]]
            table_data.append([
                item_info['equipment_id'], 
                item_info['name'], 
                item_info['type'], 
                item_info['stock_level'], 
            ])

            table = CTkTable(master=self.results, row=len(table_data), column=4, values=table_data)
            table.pack(expand=True, fill="both", padx=20, pady=20)
            



