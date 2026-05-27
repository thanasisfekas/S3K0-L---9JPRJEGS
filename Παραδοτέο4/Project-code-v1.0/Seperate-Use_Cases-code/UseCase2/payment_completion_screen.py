import tkinter as tk


class PaymentCompletionScreen:

    def __init__(self, root, receipt, close_command):

        self.root = root
        self.root.configure(bg="#f8f9fa")

        tk.Label(
            root,
            text="Payment Successful",
            font=("Arial", 16, "bold"),
            bg="#f8f9fa"
        ).pack(pady=20)

        tk.Label(root, text=str(receipt)).pack(pady=10)

        tk.Button(
            root,
            text="Back to Dashboard",
            bg="#007bff",
            fg="white",
            command=close_command
        ).pack(pady=20)