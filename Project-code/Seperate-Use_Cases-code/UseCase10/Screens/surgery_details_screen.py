import tkinter as tk
from tkinter import ttk


class SurgeryDetailScreen:
    def __init__(self, root, controller, request_id, doctor_id, room, date, assigned_nurses, on_back_click):
        self.root = root
        self.controller = controller
        self.request_id = request_id
        self.doctor_id = doctor_id
        self.room = room
        self.date = date
        self.assigned_nurses = assigned_nurses  # List of nurse names strings
        self.on_back_click = on_back_click

        self.root.title("Surgery Final Review")
        self.root.geometry("650x600")
        self.root.configure(bg="#ffffff")

        self.create_widgets()

    def create_widgets(self):
        # --- Top Header Area ---
        header_frame = tk.Frame(self.root, bg="#ffffff")
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text="FINAL SURGERY SUMMARY & SCHEDULING",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="#333333").pack()

        # --- Information Ledger Panel ---
        summary_frame = tk.LabelFrame(self.root, text=" Operational Roster Allocations ",
                                      font=("Arial", 10, "bold"), bg="#ffffff", fg="#666",
                                      padx=20, pady=15, relief="solid", bd=1)
        summary_frame.pack(padx=40, fill="x", pady=10)

        # Helper label function to maintain layout uniformity
        def add_summary_row(label_text, value_text, row_idx):
            tk.Label(summary_frame, text=label_text, font=("Arial", 10, "bold"), bg="#ffffff", fg="#555").grid(
                row=row_idx, column=0, sticky="w", pady=4)
            tk.Label(summary_frame, text=value_text, font=("Arial", 10), bg="#ffffff", fg="#111").grid(row=row_idx,
                                                                                                       column=1,
                                                                                                       sticky="w",
                                                                                                       padx=10, pady=4)

        add_summary_row("Request ID:", self.request_id, 0)
        add_summary_row("Assigned Physician:", self.doctor_id, 1)
        add_summary_row("Operating Venue:", self.room, 2)
        add_summary_row("Scheduled Date:", self.date, 3)

        # Assigned Nurses Sublist Section
        tk.Label(summary_frame, text="Assigned Nurses:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#555").grid(
            row=4, column=0, sticky="nw", pady=6)
        nurses_text = "\n".join([f"• {name}" for name in self.assigned_nurses])
        tk.Label(summary_frame, text=nurses_text, font=("Arial", 10), bg="#ffffff", fg="#111", justify="left").grid(
            row=4, column=1, sticky="w", padx=10, pady=6)

        # --- Interactive Timeline Configuration Input Form ---
        time_frame = tk.LabelFrame(self.root, text=" Time Allocation ", font=("Arial", 10, "bold"),
                                   bg="#ffffff", fg="#666", padx=20, pady=20, relief="solid", bd=1)
        time_frame.pack(padx=40, fill="x", pady=15)

        tk.Label(time_frame, text="Select Surgery Start Time:", font=("Arial", 10), bg="#ffffff", fg="#333").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  sticky="w")

        self.time_var = tk.StringVar()
        self.time_combo = ttk.Combobox(time_frame, textvariable=self.time_var, font=("Arial", 10), width=15,
                                       state="readonly")

        # Generates standard hospital theater blocks hourly increments list choices
        self.time_combo['values'] = (
            "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM",
            "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"
        )
        self.time_combo.current(1)  # Default selections targeting 08:00 AM slot
        self.time_combo.grid(row=0, column=1, sticky="w", padx=15)

        # --- Bottom Action Buttons ---
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=40)

        tk.Button(btn_frame, text="← Change Settings", font=("Arial", 10),
                  bg="#ffffff", fg="#666666", relief="flat",
                  command=self.on_back_click).pack(side="left")

        tk.Button(btn_frame, text="Finalize & Save", font=("Arial", 10, "bold"),
                  bg="#28a745", fg="white", relief="flat",  # Green confirmation palette theme accent
                  width=16, height=2,
                  command=self.on_finalize_click).pack(side="right")

    def on_finalize_click(self):
        start_time = self.time_var.get()

        # Passes the completed schedule package up to the execution completion layer
        self.controller.display_surgery_form(
            self.request_id,
            self.doctor_id,
            self.room,
            self.date,
            self.assigned_nurses,
            start_time
        )