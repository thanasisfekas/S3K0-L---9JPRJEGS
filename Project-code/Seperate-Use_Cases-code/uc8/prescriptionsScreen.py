import tkinter as tk
from tkinter import messagebox

class PrescriptionsScreen:
    def __init__(self, root, data, controller=None):
        self.root = root
        self.data = data 
        self.controller = controller
        
        self.root.configure(bg="#f0f2f5")
        
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            self.main_frame, 
            text="Patient's Prescriptions", 
            font=("Segoe UI", 20, "bold"),
            fg="#1a73e8",
            bg="#f0f2f5").pack(pady=(0, 10))

        self.canvas = tk.Canvas(self.main_frame, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((265, 0), window=self.scrollable_frame, anchor="n", width=500)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)

        self.display_prescriptions()

        tk.Button(
            self.main_frame,
            text="Back to Search Screen",
            command=self.returnToSearchScreen, 
            font=("Segoe UI", 10, "bold"),
            bg="#DC143C",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat",
            activebackground="#b01030",
            activeforeground="white"
        ).pack(side="bottom", anchor="se", pady=(10, 0))

    def display_prescriptions(self):
        if not self.data:
            empty_label = tk.Label(
                self.scrollable_frame,
                text="No prescriptions found for this patient.",
                font=("Segoe UI", 12, "italic"),
                fg="#5f6368",
                bg="#f0f2f5"
            )
            empty_label.pack(pady=50)
            return

        for prescription in self.data:
            pres_id = prescription.get('prescription_id', 'N/A')
            status = prescription.get('status', 'Unknown').lower()
            
            
            is_clickable = (status == "active")
            card_cursor = "hand2" if is_clickable else "no"
            card_bg = "white" if is_clickable else "#f8f9fa" 

    
            card = tk.Frame(
                self.scrollable_frame, 
                bg=card_bg, 
                padx=20, 
                pady=15,
                highlightbackground="#dcdfe3",
                highlightthickness=1,
                cursor=card_cursor)
            card.pack(fill="x", pady=10, padx=5)

    
            header_frame = tk.Frame(card, bg=card_bg, cursor=card_cursor)
            header_frame.pack(fill="x", pady=(0, 5))

            lbl_id = tk.Label(
                header_frame, 
                text=f"Prescription: {pres_id}", 
                font=("Segoe UI", 12, "bold"), 
                fg="#1a73e8" if is_clickable else "#70757a", 
                bg=card_bg,
                cursor=card_cursor)
            lbl_id.pack(side="left")

            pres_date = prescription.get('date', 'N/A')
            lbl_date = tk.Label(
                header_frame, 
                text=f"Date: {pres_date}", 
                font=("Segoe UI", 10), 
                fg="#5f6368", 
                bg=card_bg,
                cursor=card_cursor)
            lbl_date.pack(side="right")

            line = tk.Frame(card, height=1, bg="#e8eaed", cursor=card_cursor)
            line.pack(fill="x", pady=5)

            doc_id = prescription.get('doctor_id', '-')
            row_doc = self._create_info_row(card, "DOCTOR :", doc_id, bg_color=card_bg, cursor_type=card_cursor)

            status_color = "#28a745" if status == "active" else "#5f6368"
            if status == "cancelled" or status == "inactive": 
                status_color = "#dc3545"

            status_frame = tk.Frame(card, bg=card_bg, cursor=card_cursor)
            status_frame.pack(fill="x", pady=3)
            
            lbl_stat = tk.Label(
                status_frame, 
                text=f"STATUS: {status.upper()}", 
                font=("Segoe UI", 10, "bold"), 
                fg=status_color, 
                bg=card_bg, 
                cursor=card_cursor)
            lbl_stat.pack(anchor="center")

            all_widgets = [
                card, header_frame, lbl_id, lbl_date, line, status_frame, lbl_stat, row_doc, row_doc.winfo_children()[0]]

            for widget in all_widgets:
                widget.bind("<Button-1>", lambda event, pid=pres_id, stat=status: self.on_card_click(pid, stat))

    def _create_info_row(self, parent, label_text, value_text, bg_color="white", cursor_type="hand2"):
        row = tk.Frame(parent, bg=bg_color, cursor=cursor_type)
        row.pack(fill="x", pady=3)
        
        lbl = tk.Label(
            row, 
            text=f"{label_text} {value_text}", 
            font=("Segoe UI", 11), 
            fg="#3c4043", 
            bg=bg_color,
            cursor=cursor_type)
        lbl.pack(anchor="center")
        
        return row

    def on_card_click(self, prescription_id, status):
        if status != "active":
            messagebox.showwarning( "Access Denied", f"This prescription is {status.upper()}.\nPharmacists can only process ACTIVE prescriptions.")
            return

        if self.controller:
            if hasattr(self.controller, 'selectPrescription'):
                self.controller.selectPrescription(prescription_id)
        else:
            messagebox.showinfo("Card Clicked", f"Standalone Mode:\nProcessing Active Prescription: {prescription_id}")

    def returnToSearchScreen(self):
        if self.controller:
            self.controller.returnToSearchScreen()
        else:
            messagebox.showinfo("Standalone Mode", "Redirecting back to Search Screen (Simulation)")

