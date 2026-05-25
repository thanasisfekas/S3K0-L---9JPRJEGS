import tkinter as tk

class PatientDetailsScreen:
    def __init__(self, root, details, controller):
        self.root = root
        self.data = details
        self.controller = controller
        
        self.root.configure(bg="#f0f2f5")
        
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            self.main_frame, 
            text="Patient's Details", 
            font=("Segoe UI", 20, "bold"),
            fg="#1a73e8",
            bg="#f0f2f5").pack(pady=(0, 20))

        card_frame = tk.Frame(
            self.main_frame, 
            bg="white", 
            padx=30, 
            pady=30,
            highlightbackground="#dcdfe3",
            highlightthickness=1)
        card_frame.pack(pady=10, padx=50, fill="x")

        parsed_data = self._parse_details_to_tuple(self.data)
        labels = ["Patient ID", "First Name", "Last Name",  "Gender", "Date of Birth"]

        if parsed_data:
            for label_text, value in zip(labels, parsed_data):
                row = tk.Frame(card_frame, bg="white")
                row.pack(fill="x", pady=8)

                tk.Label(
                    row, 
                    text=f"{label_text.upper()}:", 
                    font=("Segoe UI", 9, "bold"),
                    fg="#5f6368",
                    bg="white",
                    width=15,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    row, 
                    text=value, 
                    font=("Segoe UI", 11),
                    fg="#202124",
                    bg="white",
                    anchor="w").pack(side="left", padx=10)
                
                line = tk.Frame(card_frame, height=1, bg="#e8eaed")
                line.pack(fill="x", pady=2)

        tk.Button(
            self.main_frame,
            text="Cancel",
            command=lambda: self.controller.displaySearchScreen(), 
            font=("Segoe UI", 10, "bold"),
            bg="#DC143C",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat").place(relx=0.02, rely=0.95, anchor="sw")

      
        tk.Button(
            self.main_frame,
            text="Next",
            command=lambda: self.controller.prescriptionAdministration(), 
            font=("Segoe UI", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat").place(relx=0.98, rely=0.95, anchor="se") 

    def _parse_details_to_tuple(self, details):
        if details is None:
            return ("", "", "", "", "")

        
        if isinstance(details, list) and len(details) > 0:
            details = details[0]

        try:
            return (str(details.get('patient_id', details.get('id', ""))), str(details.get('first_name', details.get('name', ""))), str(details.get('last_name', "")), str(details.get('gender', "")), str(details.get('date_of_birth', details.get('dob', ""))))
        except AttributeError:
            pass 

        try:
            if len(details) >= 5:
                return (str(details[0]), str(details[1]), str(details[2]), str(details[3]), str(details[4]))
            elif len(details) == 4:
                return (str(details[0]), str(details[1]), str(details[2]), "", str(details[3]))
            elif len(details) == 3:
                return (str(details[0]), str(details[1]), "", "", str(details[2]))
        except TypeError:
            pass

        
        return (str(getattr(details, 'patient_id', getattr(details, 'id', ""))),str(getattr(details, 'first_name', getattr(details, 'name', ""))),str(getattr(details, 'last_name', "")),str(getattr(details, 'gender', "")),str(getattr(details, 'date_of_birth', getattr(details, 'dob', ""))))