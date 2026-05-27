import tkinter as tk
from tkinter import ttk


class SurgeryFormScreen:
    def __init__(self, root, controller, request_id, doctor_id, on_back_click):
        self.root = root
        self.controller = controller
        self.request_id = request_id
        self.doctor_id = doctor_id
        self.on_back_click = on_back_click

        self.root.title("Surgery Assignment Form")
        self.root.geometry("600x550")  # Vertically extended slightly to fit the new date row
        self.root.configure(bg="#ffffff")

        self.create_widgets()

    def create_widgets(self):
        # --- Top Header Area ---
        header_frame = tk.Frame(self.root, bg="#ffffff")
        header_frame.pack(fill="x", pady=25)

        tk.Label(header_frame, text="SURGERY APPOINTMENT DETAILS",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333").pack()

        tk.Label(header_frame, text=f"Request: {self.request_id}  |  Assigned Doctor ID: {self.doctor_id}",
                 font=("Arial", 9, "italic"), bg="#ffffff", fg="#666666").pack(pady=5)

        # --- Form Container ---
        form_frame = tk.LabelFrame(self.root, text=" Logistics Scheduling ", font=("Arial", 10, "bold"),
                                   bg="#ffffff", fg="#666", padx=25, pady=25, relief="solid", bd=1)
        form_frame.pack(padx=40, fill="both", expand=True)

        # 1. Operating Room Field
        tk.Label(form_frame, text="Select Operating Room:", font=("Arial", 10), bg="#ffffff", fg="#333").grid(row=0,
                                                                                                              column=0,
                                                                                                              sticky="w",
                                                                                                              pady=10)

        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(form_frame, textvariable=self.room_var, font=("Arial", 10), width=24,
                                       state="readonly")

        # Populating theater suites based on the provided csv options
        self.room_combo['values'] = (
        "OR Suite A - General", "OR Suite B - Pediatrics", "OR Suite C - Oncology", "OR Suite D - ICU Backup",
        "OR Suite E - Dermatology")
        self.room_combo.current(0)
        self.room_combo.grid(row=0, column=1, sticky="w", padx=15, pady=10)

        # 2. NEW FIELD: Surgery Date Field
        tk.Label(form_frame, text="Scheduled Date:", font=("Arial", 10), bg="#ffffff", fg="#333").grid(row=1, column=0,
                                                                                                       sticky="w",
                                                                                                       pady=10)

        self.date_var = tk.StringVar(value="2026-05-21")  # Sets default to next available date slot
        self.date_entry = tk.Entry(form_frame, textvariable=self.date_var, font=("Arial", 10), width=26,
                                   highlightthickness=1, highlightbackground="#cccccc", relief="flat")
        self.date_entry.grid(row=1, column=1, sticky="w", padx=15, pady=10)

        # 3. Nurses Count Field
        tk.Label(form_frame, text="Nurses Needed:", font=("Arial", 10), bg="#ffffff", fg="#333").grid(row=2, column=0,
                                                                                                      sticky="w",
                                                                                                      pady=10)

        self.nurses_var = tk.IntVar(value=2)
        self.nurses_spin = tk.Spinbox(form_frame, from_=1, to=10, textvariable=self.nurses_var, font=("Arial", 10),
                                      width=10, justify="center")
        self.nurses_spin.grid(row=2, column=1, sticky="w", padx=15, pady=10)

        # --- Bottom Action Bar ---
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=40)

        tk.Button(btn_frame, text="← Cancel", font=("Arial", 10),
                  bg="#ffffff", fg="#666666", relief="flat",
                  command=self.on_back_click).pack(side="left")

        tk.Button(btn_frame, text="Confirm Booking", font=("Arial", 10, "bold"),
                  bg="#007bff", fg="white", relief="flat",
                  width=16, height=2,
                  command=self.on_submit_click).pack(side="right")

    def on_submit_click(self):
        selected_room = self.room_var.get()
        selected_date = self.date_var.get()
        assigned_nurses = self.nurses_var.get()

        # Submit data elements seamlessly back to controller including the newly assigned surgery date
        self.controller.display_surgery_details(
            self.request_id,
            self.doctor_id,
            selected_room,
            selected_date,
            assigned_nurses
        )