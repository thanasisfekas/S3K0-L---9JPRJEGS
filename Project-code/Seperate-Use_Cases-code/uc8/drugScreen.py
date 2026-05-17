import tkinter as tk
from tkinter import messagebox

class DrugScreen:
    def __init__(self, root, controller, prescription_data):
        self.root = root
        self.controller = controller
        self.prescription_data = prescription_data  

        self.root.configure(bg="#f0f2f5")
        
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        pres_id = self.prescription_data.get('prescription_id', 'N/A')
        
        title_label = tk.Label(
            self.main_frame, 
            text=f"Prescription's Drugs: {pres_id}", 
            font=("Segoe UI", 18, "bold"),
            fg="#1a73e8",
            bg="#f0f2f5")
        title_label.pack(pady=(0, 5))

        tk.Button(
            self.main_frame,
            text="Back to Prescriptions",
            command=self.go_back,
            font=("Segoe UI", 10, "bold"),
            bg="#DC143C",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat",
            activebackground="#b01030",
            activeforeground="white").pack(side="bottom", anchor="sw", pady=(15, 0))
    
        self.canvas = tk.Canvas(self.main_frame, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")
        
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((265, 0), window=self.scrollable_frame, anchor="n", width=500)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        
        self.display_medicines_and_instructions()

    def display_medicines_and_instructions(self):
        medicines = self.prescription_data.get('medicines', [])
        
        if not medicines:
            no_meds = tk.Label(
                self.scrollable_frame,
                text="No medicines found in this prescription.",
                font=("Segoe UI", 12, "italic"),
                fg="#5f6368",
                bg="#f0f2f5")
            no_meds.pack(pady=30)
            return

        controller_blocked = []
        if self.controller and hasattr(self.controller, 'processed_drugs'):
            controller_blocked = self.controller.processed_drugs

        for item in medicines:
            med_id = item.get('id')
            
            is_already_selected = med_id in controller_blocked
            
            card_bg = "#f1f3f4" if is_already_selected else "white"
            card_cursor = "no" if is_already_selected else "hand2"
            text_color = "#80868b" if is_already_selected else "#202124"

            med_card = tk.Frame(
                self.scrollable_frame,
                bg=card_bg,
                padx=20,
                pady=15,
                highlightbackground="#dcdfe3",
                highlightthickness=1,
                cursor=card_cursor)
            med_card.pack(fill="x", pady=8, padx=5)
            
            display_name = item.get('name', 'Unknown Medicine')
            if is_already_selected:
                display_name += " (ALREADY SELECTED)"

            med_name_lbl = tk.Label(
                med_card,
                text=display_name,
                font=("Segoe UI", 13, "bold"),
                fg="#dc3545" if is_already_selected else "#202124",
                bg=card_bg,
                anchor="w",
                cursor=card_cursor)
            med_name_lbl.pack(fill="x", pady=(0, 5))
        
            inner_line = tk.Frame(med_card, height=1, bg="#e8eaed", cursor=card_cursor)
            inner_line.pack(fill="x", pady=5)
            
            instr_title = tk.Label(
                med_card,
                text="Doctor's Instructions / Dosage:",
                font=("Segoe UI", 9, "bold"),
                fg="#70757a" if is_already_selected else "#1a73e8",
                bg=card_bg,
                anchor="w",
                cursor=card_cursor)
            instr_title.pack(fill="x", pady=(3, 0))
        
            instructions_lbl = tk.Label(
                med_card,
                text=item.get('dosage', 'No specific instructions.'),
                font=("Segoe UI", 11),
                fg=text_color,
                bg=card_bg,
                anchor="w",
                justify="left",
                wraplength=440,
                cursor=card_cursor)
            instructions_lbl.pack(fill="x", pady=(2, 0))

            card_widgets = [med_card, med_name_lbl, inner_line, instr_title, instructions_lbl]
            for widget in card_widgets:
                widget.bind("<Button-1>", lambda event, selected_item=item, mid=med_id: self.on_drug_click(selected_item, mid))

    def on_drug_click(self, drug_item, med_id):
        if self.controller and hasattr(self.controller, 'processed_drugs'):
            if med_id in self.controller.processed_drugs:
                messagebox.showwarning("Action Denied!",f"The medicine '{drug_item.get('name')}' has already been selected and processed.")
                return

        med_name = drug_item.get('name', 'Unknown Medicine')
        messagebox.showinfo("Success", f"Medicine selected. ")

        if self.controller and hasattr(self.controller, 'getDrug'):
            self.controller.getDrug(drug_item)

    def go_back(self):
        if self.controller and hasattr(self.controller, 'displayPrescriptions'):
            self.controller.displayPrescriptions()