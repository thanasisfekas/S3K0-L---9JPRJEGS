import tkinter as tk


class ConfirmationScreen:
    def __init__(self, root, doctor_name, specialty, date, time, on_confirm, on_cancel):
        self.root = root
        self.root.configure(bg="#ffffff")

        header = tk.Frame(root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        tk.Label(root, text="Confirm Appointment", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=30)

        card = tk.Frame(root, bg="#f9f9f9", bd=1, relief="solid")
        card.pack(fill="x", padx=50, pady=20)

        self.row(card, "Doctor", doctor_name)
        self.row(card, "Specialty", specialty)
        self.row(card, "Date", date)
        self.row(card, "Time", time)

        tk.Button(root, text="Confirm Booking", bg="#28a745", fg="white", font=("Arial", 12, "bold"), height=2, command=on_confirm).pack(fill="x", padx=50, pady=(20, 10))
        tk.Button(root, text="Cancel", bg="#dc3545", fg="white", font=("Arial", 12, "bold"), height=2, command=on_cancel).pack(fill="x", padx=50, pady=(0, 40))

    def row(self, parent, label, value):
        row = tk.Frame(parent, bg="#f9f9f9")
        row.pack(fill="x", padx=20, pady=10)

        tk.Label(row, text=label, bg="#f9f9f9").pack(side="left")
        tk.Label(row, text=value, bg="#f9f9f9").pack(side="right")