import tkinter as tk
from tkinter import messagebox


class PaymentFormScreen:
    def __init__(self, root, method_type, amount, on_submit, back_command):
        self.root = root
        self.method_type = method_type
        self.on_submit = on_submit

        self.root.configure(bg="#ffffff")
        self.root.title("Payment Form")
        self.root.geometry("400x600")

        # ---------- Header ----------
        header = tk.Frame(self.root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        tk.Button(header, text="← Back", font=("Arial", 10), bg="white", relief="flat", command=back_command).pack(side="left", padx=20)
        tk.Label(self.root, text=f"{method_type} Card Details", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=20)

        # ---------- Form ----------
        form_frame = tk.Frame(self.root, bg="#ffffff")
        form_frame.pack(padx=40, fill="x")

        self.card_ent = self.create_input(form_frame, "Card Number (16 digits)")

        row_frame = tk.Frame(form_frame, bg="#ffffff")
        row_frame.pack(fill="x", pady=10)

        self.expiry_ent = self.create_small_input(row_frame, "Expiry (MM/YY)", "left")

        self.cvv_ent = self.create_small_input(row_frame, "CVV", "right")

        # ---------- Submit ----------
        tk.Button(self.root, text=f"Pay {amount}", font=("Arial", 12, "bold"), bg="#28a745", fg="white", relief="flat", height=2, command=self.validate_and_submit).pack(fill="x", padx=40, pady=40)

    def create_input(self, parent, label_text):
        tk.Label(parent, text=label_text, font=("Arial", 9), bg="#ffffff", fg="gray").pack(anchor="w", pady=(10, 2))

        ent = tk.Entry(parent, font=("Arial", 12), bd=1, relief="solid")
        ent.pack(fill="x", ipady=8)

        return ent

    def create_small_input(self, parent, label_text, side):
        container = tk.Frame(parent, bg="#ffffff")
        container.pack(side=side, fill="x", expand=True, padx=5)

        tk.Label(container, text=label_text, font=("Arial", 9), bg="#ffffff", fg="gray").pack(anchor="w")

        ent = tk.Entry(container, font=("Arial", 12), bd=1, relief="solid")
        ent.pack(fill="x", ipady=8)

        return ent

    def validate_and_submit(self):
        payment_data = {"card_number": self.card_ent.get(), "expiry": self.expiry_ent.get(), "cvv": self.cvv_ent.get()}
        self.on_submit(payment_data)