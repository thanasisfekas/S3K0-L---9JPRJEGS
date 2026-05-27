import tkinter as tk
from tkinter import messagebox


class SearchAppointmentScreen:
    def __init__(self, root, on_submit, back_command=None):
        self.root = root
        self.on_submit = on_submit

        if hasattr(self.root, "title"):
            self.root.title("Search Appointment")
        if hasattr(self.root, "geometry"):
            self.root.geometry("500x500")
        self.root.configure(bg="#ffffff")

        header = tk.Frame(root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        if back_command:
            tk.Button(
                header,
                text="< Back",
                font=("Arial", 10),
                bg="white",
                relief="flat",
                command=back_command,
            ).pack(side="left", padx=20)

        tk.Label(
            root,
            text="Select Appointment Date",
            font=("Arial", 18, "bold"),
            bg="#ffffff",
            fg="#1a1c3d",
        ).pack(pady=50)

        self.date_entry = tk.Entry(root, font=("Arial", 14), relief="solid", bd=1)
        self.date_entry.pack(fill="x", padx=60, ipady=8)

        tk.Label(root, text="Format: YYYY-MM-DD", bg="#ffffff", fg="gray").pack(pady=10)
        tk.Button(
            root,
            text="Continue",
            font=("Arial", 12, "bold"),
            bg="#007bff",
            fg="white",
            relief="flat",
            height=2,
            command=self.submit,
        ).pack(fill="x", padx=60, pady=40)

    def submit(self):
        date = self.date_entry.get()

        if not date:
            messagebox.showerror("Error", "Please enter a date.")
            return

        self.on_submit(date)
