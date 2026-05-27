from __future__ import annotations
import tkinter as tk


class BillDetailScreen:
    def __init__(self, root, amount, date, treatment, bill_id, pay_command=None, back_command=None):
        self.root = root
        self.back_command = back_command
        self.amount = amount
        self.date = date
        self.treatment = treatment
        self.bill_id = bill_id
        self.pay_command = pay_command

        self.root.title("Bill Details")
        self.root.geometry("400x600")
        self.root.configure(bg="#ffffff")

        # ---------------- HEADER ----------------
        header_frame = tk.Frame(root, bg="#ffffff")
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text="BILL PAYMENT", font=("Arial", 10, "bold"), bg="#ffffff", fg="#666").pack()
        tk.Label(header_frame, text=str(self.amount), font=("Arial", 36, "bold"), bg="#ffffff", fg="#1a1c3d").pack(pady=10)

        # ---------------- DETAILS CARD ----------------
        details_card = tk.Frame(root, bg="#f9f9f9", bd=1, relief="solid")
        details_card.pack(padx=30, fill="x", pady=10)

        inner = tk.Frame(details_card, bg="#f9f9f9")
        inner.pack(padx=15, pady=15, fill="x")

        self.add_info_row(inner, "Issue Date", self.date, "📅")
        self.add_divider(inner)

        self.add_info_row(inner, "Description", self.treatment, "✎")
        self.add_divider(inner)

        self.add_info_row(inner, "Bill ID", self.bill_id, None)

        # ---------------- EMPTY REMINDER CARD ----------------
        reminder_frame = tk.Frame(root, bg="#f9f9f9", bd=1, relief="solid")
        reminder_frame.pack(padx=30, fill="x", pady=10)

        # ---------------- BUTTONS ----------------
        btn_frame = tk.Frame(root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=30)

        tk.Button(btn_frame, text="← Back", font=("Arial", 10), bg="#ffffff", fg="#666", relief="flat", command=self.back_command).pack(side="left")
        tk.Button(btn_frame, text="Pay", font=("Arial", 10, "bold"), bg="#007bff", fg="white", relief="flat", width=12, height=2, command=self.pay_command).pack(side="right")

    def add_info_row(self, parent, label, value, icon):
        row_frame = tk.Frame(parent, bg="#f9f9f9")
        row_frame.pack(fill="x", pady=5)

        tk.Label(row_frame, text=label, font=("Arial", 8), fg="#888", bg="#f9f9f9").pack(anchor="w")

        val_line = tk.Frame(row_frame, bg="#f9f9f9")
        val_line.pack(fill="x")

        if icon:
            tk.Label(val_line, text=icon, font=("Arial", 10), bg="#f9f9f9").pack(side="left")

        tk.Label(val_line, text=value, font=("Arial", 11, "bold"), bg="#f9f9f9").pack(side="left", padx=5)

    def add_divider(self, parent):
        tk.Frame(parent, height=1, bg="#eeeeee").pack(fill="x", pady=8)