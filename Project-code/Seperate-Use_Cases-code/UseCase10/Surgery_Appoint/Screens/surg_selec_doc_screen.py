import tkinter as tk
from tkinter import ttk


class SelectDoctorScreen:
    def __init__(self, root, controller, request_id, specialty, on_back_click):
        self.root = root
        self.controller = controller
        self.request_id = request_id
        self.specialty = specialty
        self.on_back_click = on_back_click

        self.root.title("Assign Doctors")
        self.root.geometry("900x600")
        self.root.configure(bg="#ffffff")

        self.create_widgets()
        # Automatically load specialized doctors using the controller reference mapping
        self.load_specialized_doctors()

    def create_widgets(self):
        # --- Top Header Area ---
        header_frame = tk.Frame(self.root, bg="#ffffff")
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text=f"AVAILABLE DOCTORS FOR REQUEST {self.request_id}",
                 font=("Arial", 10, "bold"), bg="#ffffff", fg="#666").pack()

        tk.Label(header_frame, text=f"Required Specialty: {self.specialty}",
                 font=("Arial", 11, "italic"), bg="#ffffff", fg="#007bff").pack(pady=5)

        # --- Central Data Grid ---
        grid_frame = tk.Frame(self.root, bg="#ffffff")
        grid_frame.pack(padx=30, fill="both", expand=True, pady=10)

        columns = ("doctor_id", "name", "specialization", "years_experience", "hospital_branch", "email")
        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings", selectmode="extended")

        self.tree.heading("doctor_id", text="Doctor ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("specialization", text="Specialty")
        self.tree.heading("years_experience", text="Experience (Yrs)")
        self.tree.heading("hospital_branch", text="Hospital Branch")
        self.tree.heading("email", text="Email Contact")

        self.tree.column("doctor_id", width=90, anchor="center")
        self.tree.column("name", width=160, anchor="w")
        self.tree.column("specialization", width=120, anchor="center")
        self.tree.column("years_experience", width=110, anchor="center")
        self.tree.column("hospital_branch", width=150, anchor="w")
        self.tree.column("email", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- Bottom Action Buttons Bar ---
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=30)

        tk.Button(btn_frame, text="← Back", font=("Arial", 10),
                  bg="#ffffff", fg="#666", relief="flat",
                  command=self.on_back_click).pack(side="left")

        self.btn_assign = tk.Button(btn_frame, text="Assign Doctor", font=("Arial", 10, "bold"),
                                    bg="#cccccc", fg="white", relief="flat",
                                    width=14, height=2, state="disabled",
                                    command=self.on_assign_click)
        self.btn_assign.pack(side="right")

    def load_specialized_doctors(self):
        """ Clears grid and pulls rows directly via the connected controller """
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Uses the controller method to query rows filtering by required specialty
        doctors = self.controller.get_surgery_doctors(self.specialty)
        for doc in doctors:
            self.tree.insert("", "end", values=doc)

    def on_row_select(self, event):
        if self.tree.selection():
            self.btn_assign.config(state="normal", bg="#007bff")  # standard blue theme on selection active
        else:
            self.btn_assign.config(state="disabled", bg="#cccccc")
    '''
    def on_assign_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item[0], "values")
        doctor_id = row_values[0]
        doctor_name = row_values[1]

        # Route assignment completion back up to controller action tracking methods
        self.controller.validate_multi_doc_count(self.request_id, selected_doctors=)
    '''

    def on_assign_click(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        selected_doctors = []
        for item in selected_items:
            row_values = self.tree.item(item, "values")
            doctor_id = row_values[0]
            doctor_name = row_values[1]
            selected_doctors.append((doctor_id, doctor_name))

        # Pass the whole list of tuples directly to the controller layout validator
        self.controller.validate_multi_doc_count(self.request_id, selected_doctors)