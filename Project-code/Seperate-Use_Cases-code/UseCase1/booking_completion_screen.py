import tkinter as tk


class BookingCompletionScreen:
    def __init__(self, root, close_command):
        self.root = root
        self.root.configure(bg="#ffffff")

        tk.Label(root, text="✓", font=("Arial", 50), fg="green", bg="#ffffff").pack(pady=40)
        tk.Label(root, text="Appointment Booked Successfully", font=("Arial", 18, "bold"), bg="#ffffff").pack()
        tk.Button(root, text="Back to Search", bg="#007bff", fg="white", font=("Arial", 12, "bold"), height=2, command=close_command).pack(fill="x", padx=70, pady=60)