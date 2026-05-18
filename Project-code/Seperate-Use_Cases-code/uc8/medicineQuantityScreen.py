import tkinter as tk
from tkinter import messagebox

class MedicineQuantityScreen:
    def __init__(self, parent_root, controller, drug_data):
        self.controller = controller
        self.drug_data = drug_data
        
        self.window = tk.Toplevel(parent_root)
        self.window.title("Enter Quantity")
        self.window.configure(bg="#f0f2f5")
        
        self.window.geometry("400x320")
        self.window.resizable(False, False)
        
        self.window.grab_set() 
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg="#f0f2f5", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame, 
            text="Selected Medicine:", 
            font=("Segoe UI", 10, "bold"), 
            fg="#5f6368", 
            bg="#f0f2f5", 
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            main_frame, 
            text=self.drug_data.get('name', 'Unknown'), 
            font=("Segoe UI", 14, "bold"), 
            fg="#202124", 
            bg="#f0f2f5", 
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            main_frame, 
            text="Doctor's Instructions:", 
            font=("Segoe UI", 10, "bold"), 
            fg="#1a73e8", 
            bg="#f0f2f5", 
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            main_frame, 
            text=self.drug_data.get('dosage', 'No specific instructions.'), 
            font=("Segoe UI", 11, "italic"), 
            fg="#3c4043", 
            bg="#f0f2f5", 
            anchor="w",
            wraplength=350,
            justify="left"
        ).pack(fill="x", pady=(0, 20))

        line = tk.Frame(main_frame, height=1, bg="#dcdfe3")
        line.pack(fill="x", pady=(0, 15))

        tk.Label(
            main_frame, 
            text="Enter Dispensed Quantity:", 
            font=("Segoe UI", 11, "bold"), 
            fg="#202124", 
            bg="#f0f2f5", 
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.quantity_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=10, justify="center")
        self.quantity_entry.pack(anchor="w", pady=(0, 20))
        self.quantity_entry.insert(0, "1")  
        self.quantity_entry.focus_set()    

        btn_frame = tk.Frame(main_frame, bg="#f0f2f5")
        btn_frame.pack(fill="x", side="bottom")

        tk.Button(
            btn_frame,
            text="Confirm",
            command=self.confirm_quantity,
            font=("Segoe UI", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=15,
            pady=6,
            relief="flat",
            cursor="hand2"
        ).pack(side="right", padx=(5, 0))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.on_cancel, 
            font=("Segoe UI", 10, "bold"),
            bg="#5f6368",
            fg="white",
            padx=15,
            pady=6,
            relief="flat",
            cursor="hand2"
        ).pack(side="right")

    def confirm_quantity(self):
        input_value = self.quantity_entry.get().strip()
        
        if not input_value.isdigit() or int(input_value) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for quantity.")
            return
            
        quantity = int(input_value)
        
        self.window.destroy()
        
        if self.controller and hasattr(self.controller, 'submitDrugQuantity'):
            self.controller.submitDrugQuantity(self.drug_data, quantity)

    def on_cancel(self):
        if self.controller and hasattr(self.controller, 'cancelDrugSelection'):
            self.controller.cancelDrugSelection(self.drug_data.get('id'))
        
        self.window.destroy()