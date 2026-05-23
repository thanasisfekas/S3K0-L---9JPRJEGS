import tkinter as tk
from tkinter import ttk


class PatientSearchScreen:
    def __init__(self, root, patient_list, on_patient_select):
        self.root = root
        self.patient_list = patient_list  # The data passed in from outside
        self.on_patient_select = on_patient_select  # The external function to call

        self.setup_ui()
        self.populate_table(self.patient_list)

    def setup_ui(self):
        """Builds the UI components."""
        self.root.configure(bg="#ffffff")

        # Search Section
        container = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Patient Search", font=("Arial", 16, "bold"),
                 bg="#ffffff").pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search_change)

        search_entry = tk.Entry(container, textvariable=self.search_var, font=("Arial", 12))
        search_entry.pack(fill="x", pady=(10, 20), ipady=5)
        search_entry.insert(0, "Search by name or ID...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0,
                                                                     'end') if self.search_var.get() == "Search by name or ID..." else None)

        # Table Section
        columns = ("id", "name", "dob")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Full Name")
        self.tree.heading("dob", text="Date of Birth")
        self.tree.pack(fill="both", expand=True)

        # Selection Button
        tk.Button(container, text="Select Patient", bg="#007bff", fg="white",
                  font=("Arial", 10, "bold"), command=self.submit_selection,
                  height=2).pack(fill="x", pady=(20, 0))

    def populate_table(self, data):
        """Clears and refills the table with provided data."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in data:
            self.tree.insert("", "end", values=(p['id'], p['name'], p['dob']))

    def on_search_change(self, *args):
        """Filters the local patient_list based on user input."""
        query = self.search_var.get().lower()
        if query == "search by name or id...": return

        filtered = [
            p for p in self.patient_list
            if query in str(p['id']).lower() or query in p['name'].lower()
        ]
        self.populate_table(filtered)

    def submit_selection(self):
        """Finds selected row and sends it back to the caller."""
        selected = self.tree.selection()
        if selected:
            patient_id = self.tree.item(selected)['values'][0]
            self.on_patient_select(patient_id)



'''
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")

    # Mock data that would normally come from your CSV
    sample_patients = [
        {'id': 'P001', 'name': 'Alice Smith', 'dob': '1990-05-12'},
        {'id': 'P002', 'name': 'Bob Jones', 'dob': '1985-11-23'},
        {'id': 'P003', 'name': 'Charlie Brown', 'dob': '2001-01-30'}
    ]


    # Simple callback function
    def my_callback(p_id):
        print(f"Secretary selected Patient ID: {p_id}")
        root.destroy()


    # Launch screen
    app = PatientSearchScreen(root, sample_patients, my_callback)
    root.mainloop()
'''