import tkinter as tk
from tkinter import ttk


class BillIssuingScreen:
    def __init__(self, root, patient_id, patient_name, treatments, prescriptions, on_back, on_confirm):
        self.root = root
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.treatments = treatments
        self.prescriptions = prescriptions
        self.on_back = on_back
        self.on_confirm = on_confirm

        self.root.configure(bg="#f8f9fa")
        self.setup_ui()

        # Pre-select all items by default when the screen loads
        self.select_all_items()
        self.update_running_total()

    def setup_ui(self):
        # --- Top Navigation & Header ---
        header = tk.Frame(self.root, bg="#ffffff", height=60)
        header.pack(fill="x", side="top")

        tk.Button(header, text="← Back", font=("Arial", 10), bg="white",
                  relief="flat", command=self.on_back).pack(side="left", padx=20, pady=15)

        tk.Label(header, text=f"Billing Summary: {self.patient_name} ({self.patient_id})",
                 font=("Arial", 12, "bold"), bg="#ffffff", fg="#1a1c3d").pack(side="left", pady=15)

        # --- Main Layout Body ---
        main_container = tk.Frame(self.root, bg="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Helper to create tables smoothly
        columns = ("id", "name", "date", "cost")

        # 1. Treatments Section
        tk.Label(main_container, text="Treatments & Procedures (Hold Ctrl/Shift to multi-select)",
                 font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#007bff").pack(anchor="w", pady=(10, 5))

        self.treat_tree = ttk.Treeview(main_container, columns=columns, show="headings", height=5,
                                       selectmode="extended")
        self.configure_tree(self.treat_tree)
        self.treat_tree.pack(fill="x", pady=(0, 15))
        self.treat_tree.bind("<<TreeviewSelect>>", lambda e: self.update_running_total())

        # 2. Prescriptions Section
        tk.Label(main_container, text="Prescribed Medications",
                 font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#007bff").pack(anchor="w", pady=(5, 5))

        self.presc_tree = ttk.Treeview(main_container, columns=columns, show="headings", height=5,
                                       selectmode="extended")
        self.configure_tree(self.presc_tree)
        self.presc_tree.pack(fill="x", pady=(0, 15))
        self.presc_tree.bind("<<TreeviewSelect>>", lambda e: self.update_running_total())

        # Populate tables
        for t in self.treatments:
            self.treat_tree.insert("", "end", iid=t['id'],
                                   values=(t['id'], t['item_name'], t['date'], f"${t['cost']:.2f}"))
        for p in self.prescriptions:
            self.presc_tree.insert("", "end", iid=p['id'],
                                   values=(p['id'], p['item_name'], p['date'], f"${p['cost']:.2f}"))

        # --- Footer Section ---
        footer = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        footer.pack(side="bottom", fill="x")

        # Total Price Readout
        self.total_var = tk.StringVar(value="Total Due: $0.00")
        tk.Label(footer, textvariable=self.total_var, font=("Arial", 14, "bold"),
                 bg="#ffffff", fg="#1a1c3d").pack(side="left", padx=30, pady=20)

        # Action Button
        tk.Button(footer, text="Generate Invoice", font=("Arial", 11, "bold"),
                  bg="#28a745", fg="white", relief="flat", width=18, height=2,
                  command=self.submit_final_bill).pack(side="right", padx=30, pady=15)

    def configure_tree(self, tree):
        """Standardizes header labels and row layout for treeviews."""
        tree.heading("id", text="Item ID")
        tree.heading("name", text="Description")
        tree.heading("date", text="Date")
        tree.heading("cost", text="Cost")
        tree.column("id", width=80, anchor="center")
        tree.column("name", width=240, anchor="w")
        tree.column("date", width=100, anchor="center")
        tree.column("cost", width=80, anchor="e")

    def select_all_items(self):
        """Programmatically highlights every row initially."""
        self.treat_tree.selection_set(self.treat_tree.get_children())
        self.presc_tree.selection_set(self.presc_tree.get_children())

    def update_running_total(self):
        """Calculates costs exclusively for rows currently highlighted by the user."""
        total = 0.0

        # Sum selected treatments
        for item_id in self.treat_tree.selection():
            # Find matching item object to get exact raw float value
            item_data = next((t for t in self.treatments if t['id'] == item_id), None)
            if item_data: total += item_data['cost']

        # Sum selected prescriptions
        for item_id in self.presc_tree.selection():
            item_data = next((p for p in self.prescriptions if p['id'] == item_id), None)
            if item_data: total += item_data['cost']

        self.running_total = total
        self.total_var.set(f"Total Due: ${total:.2f}")

    def submit_final_bill(self):
        """Gathers IDs of items highlighted and passes them to the confirmation callback."""
        selected_treatments = list(self.treat_tree.selection())
        selected_prescriptions = list(self.presc_tree.selection())

        # Execute external controller function
        self.on_confirm(selected_treatments, selected_prescriptions, self.running_total)