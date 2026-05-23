import tkinter as tk


class PatientDetailScreen:
    def __init__(self, root, patient_data, back_command, proceed_command):
        self.root = root
        self.data = patient_data
        self.root.configure(bg="#f8f9fa")
        self.issue_bill_command = None

        # --- Header ---
        header = tk.Frame(self.root, bg="#ffffff", height=60)
        header.pack(fill="x", side="top")

        tk.Button(header, text="← Back", font=("Arial", 10), bg="white",
                  relief="flat", command=back_command).pack(side="left", padx=20, pady=15)

        # --- Patient Identity ---
        title_frame = tk.Frame(self.root, bg="#f8f9fa")
        title_frame.pack(pady=20, padx=30, fill="x")

        full_name = f"{self.data['first_name']} {self.data['last_name']}"
        tk.Label(title_frame, text=full_name, font=("Arial", 18, "bold"),
                 bg="#f8f9fa", fg="#1a1c3d").pack(anchor="w")
        tk.Label(title_frame, text=f"Patient ID: {self.data['patient_id']}",
                 font=("Arial", 10), bg="#f8f9fa", fg="#666").pack(anchor="w")

        # --- Information Cards ---
        self.create_info_card("Personal Information", [
            ("Gender", self.data['gender']),
            ("DOB", self.data['date_of_birth']),
            ("Contact", self.data['contact_number']),
            ("Email", self.data['email']),
            ("Address", self.data['address'])
        ])

        self.create_info_card("Insurance Details", [
            ("Provider", self.data['insurance_provider']),
            ("Policy #", self.data['insurance_number']),
            ("Reg. Date", self.data['registration_date'])
        ])

        # --- Action Button ---
        tk.Button(self.root, text="Check Charges & Issue Bill", font=("Arial", 12, "bold"),
                  bg="#28a745", fg="white", relief="flat", height=2,
                  command=proceed_command).pack(fill="x", padx=30, pady=30, side="bottom")


    def create_info_card(self, title, items):
        """Creates a stylized card containing rows of data."""
        card = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        card.pack(fill="x", padx=30, pady=10)

        tk.Label(card, text=title.upper(), font=("Arial", 9, "bold"),
                 bg="#ffffff", fg="#007bff").pack(anchor="w", pady=(0, 10))

        for label, value in items:
            row = tk.Frame(card, bg="#ffffff")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label}:", font=("Arial", 10), bg="#ffffff", fg="#999", width=10, anchor="w").pack(
                side="left")
            tk.Label(row, text=value, font=("Arial", 10), bg="#ffffff", fg="#333", wraplength=200, justify="left").pack(
                side="left")