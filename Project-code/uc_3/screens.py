from tkinter import messagebox
import customtkinter as ctk
import sys
import os
from CTkTable import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
TEXT_MUTE = "#64748B"

class SearchResultScreen(ctk.CTkFrame):
    def __init__(self,parent ,search_controller):
        super().__init__(parent)
        self.parent = parent
        self.search_controller = search_controller
        self.configure(fg_color=BG_COLOR)
        self.create_screen()
        self.selected_row = None

    def create_screen(self):
        self.result_lb = ctk.CTkLabel(
            self,
            text="Selected Items", 
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#dbdbdb",
            corner_radius=10
        )
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        
    def display(self)->None:
        self.search_controller.searchScreen.pack_forget()
        self.pack(fill="both", expand=True)
        self.result_lb.pack(pady=(40, 20))
        self.result_container.pack(fill="x", padx=100)

    def destroy_chld(self):
        for child in self.result_container.winfo_children():
            child.destroy()

    def displayResults(self,items):
        self.destroy_chld()

        if "medicine_id" in items.columns:
            data = [["ID", "Name", "Category", "Stock", "Expires", "Price"]]
    
            for _, row in items.iterrows():
                data.append([
                    row['medicine_id'], 
                    row['name'], 
                    row['category'], 
                    row['stock_level'], 
                    row['expiry_date'], 
                    f"${row['price']:.2f}"
                ])

            self.med_table = CTkTable(master=self.result_container ,
                                    row=len(data) ,
                                    column=6 ,
                                    values=data , 
                                    command=lambda data: self.on_click(data,self.med_table)
            )
            self.med_table.pack(expand=True, fill="both", padx=20, pady=20)

        elif "equipment_id" in items.columns:
            data = [["ID", "Name", "Type", "Stock"]]
    
            for _, row in items.iterrows():
                data.append([
                    row['equipment_id'], 
                    row['name'], 
                    row['type'], 
                    row['stock_level'], 
                ])
                
            self.equip_table = CTkTable(master=self.result_container ,
                                        row=len(data) ,
                                        column=4 ,
                                        values=data , 
                                        command=lambda data: self.on_click(data,self.equip_table)
            )
            self.equip_table.pack(expand=True, fill="both", padx=20, pady=20)
    
    def on_click(self , data , table):
        row = data["row"]
        if row ==0:
            return 
        table.select_row(row)
        self.selected_row = table.get_row(row)
        self.search_controller.OrderController.startOrder(self.selected_row)

class InvSearchScreen(ctk.CTkFrame):
    def __init__(self,parent ,search_controller):
        super().__init__(parent)
        self.search_controller = search_controller
        self.parent = parent
        self.configure(fg_color=BG_COLOR)
        self.create_form()

    def create_form(self):
        self.search_inv_lb = ctk.CTkLabel(self ,
                                        text="Search Inventory" ,
                                        font=ctk.CTkFont(size=24, weight="bold") ,
                                        fg_color="#dbdbdb" , 
                                        corner_radius=10
        )

        self.search_container = ctk.CTkFrame(self, fg_color="transparent")
        self.search_entry = ctk.CTkEntry(self.search_container ,
                                        placeholder_text="Enter equipment or medicine name Id" ,
                                        height=45 ,
                                        width=400
        )
        self.search_results = ctk.CTkScrollableFrame(self ,
                                                    label_text="Available Items" , 
                                                    fg_color=CARD_WHITE ,
                                                    height=300
        )
        self.search_btn = ctk.CTkButton(self.search_container ,
                                        text="Search" ,
                                        width=100 ,
                                        height=45 ,
                                        command=self.search_controller.getInvItem
        )

    def display(self):
        self.pack(fill="both", expand=True)
        self.search_inv_lb.pack(pady=(40, 20))
        self.search_container.pack(fill="x", padx=100)
        self.search_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.search_results.pack(fill="both", expand=True, padx=100, pady=20)
        self.search_btn.pack(side="right")

    def destroy_chld(self):
        for child in self.search_results.winfo_children():
            child.destroy()

    def showResults(self)->None:
        self.destroy_chld()
        
        meds = self.search_controller.available_inv["Medicines"].loc[0]
        equip = self.search_controller.available_inv["Equipment"].loc[0]

        med_lb = ctk.CTkLabel(self.search_results ,
                            text="Available Medicines" ,
                            font=ctk.CTkFont(size=15, weight="bold") ,
                            fg_color="#dbdbdb" ,
                            corner_radius=10
        )
        med_lb.pack(pady=(40, 20))

        data_med = [["ID", "Name", "Category", "Stock", "Expires", "Price"]]
    
        for _, row in meds.iterrows():
            data_med.append([
                row['medicine_id'], 
                row['name'], 
                row['category'], 
                row['stock_level'], 
                row['expiry_date'], 
                f"${row['price']:.2f}"
            ])

        med_table = CTkTable(master=self.search_results ,
                        row=len(data_med) ,
                        column=6 ,
                        values=data_med
        )
        med_table.pack(expand=True, fill="both", padx=20, pady=20)

        equip_lb = ctk.CTkLabel(self.search_results ,
                                text="Available Equipment" ,
                                font=ctk.CTkFont(size=15, weight="bold") ,
                                fg_color="#dbdbdb" ,
                                corner_radius=10
        )
        equip_lb.pack(pady=(40, 20))

        data_equip = [["ID", "Name", "Type", "Stock"]]
    
        for _, row in equip.iterrows():
            data_equip.append([
                row['equipment_id'], 
                row['name'], 
                row['type'], 
                row['stock_level'], 
            ])


        equip_table = CTkTable(master=self.search_results ,
                               row=len(data_equip) ,
                               column=4 ,
                               values=data_equip
        )
        equip_table.pack(expand=True, fill="both", padx=20, pady=20)

class MessageScreen:
    def __init__(self,msg):
        self.msg = msg

    def dispError(self):
        messagebox.showerror("",self.msg)
 
class OrderScreen(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.orderController= controller
        self.configure(fg_color=BG_COLOR)
        self.create_form()
        
    def create_form(self):
        self.lbl_form_title = ctk.CTkLabel(self ,
                                           text="Order Form" ,
                                           font=ctk.CTkFont(size=22, weight="bold")
        )

        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.idLabel = ctk.CTkLabel(self.form_frame, text="ID")
        self.idEntry = ctk.CTkEntry(self.form_frame)

        self.nameEntry = ctk.CTkEntry(self.form_frame)
        self.nameLabel = ctk.CTkLabel(self.form_frame, text="NAME")

        self.orderLabel = ctk.CTkLabel(self.form_frame, text="Order")
        self.orderAmountMenu = ctk.CTkComboBox(self.form_frame, values=[str(i) for i in range(1,11)], state="readonly")

        self.displayBox = ctk.CTkTextbox(self.form_frame , 
                                        width=600 ,
                                        height=100 ,
                                        fg_color=BG_COLOR ,
                                        text_color=TEXT_MUTE ,
                                        border_width=3 
        )
        
        self.submit_btn = ctk.CTkButton(self.form_frame, text="Submit Order", command=self.orderController.setFormDetails)

    def showOrderForm(self,data):
        self.lbl_form_title.pack(pady=20)
        self.pack(fill="both", expand=True)

        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
        self.idLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.idEntry.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="ew")
        self.idEntry.configure(placeholder_text=f"{data[0]}")
        self.idEntry.configure(state="disabled")
        
        self.nameLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.nameEntry.configure(placeholder_text=f"{data[1]}")
        self.nameEntry.configure(state="disabled")
        self.nameEntry.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="ew")        

        self.orderLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        self.orderAmountMenu.grid(row=4, column=1, padx=20, pady=20, columnspan=2, sticky="ew")

        self.displayBox.grid(row=0, column=3, rowspan=5, columnspan=1, padx=20, pady=20, sticky="nsew")

        self.submit_btn.grid(row=5, column=0, columnspan=3, padx=20, pady=20)

class SuccessScreen:
    def __init__(self,msg)->None:
        self.msg= msg

    def showSuccMsg(self)->None:
        messagebox.showinfo("",self.msg)
class OrderConfirmationScreen:
    def __init__(self,msg):
        self.succ_msg = msg
    
    def displayConfirmationMessage(self):
        messagebox.showwarning("",self.succ_msg)
