import tkinter as tk


class PaymentErrorScreen:
    def __init__(self, root, message, close_command):
        self.root = root
        self.close_command = close_command

        self.root.configure(bg="#ffffff")
        self.root.title("Payment Error")
        self.root.geometry("400x600")

        # Icon
        tk.Label(root, text="✕", font=("Arial", 48, "bold"), fg="red", bg="#ffffff").pack(pady=(80, 10))

        # Title
        tk.Label(root, text="Payment Failed", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Message
        tk.Label(root, text=message, font=("Arial", 11), fg="#666", bg="#ffffff", wraplength=300).pack(pady=20)

        # Back button (returns to bill list)
        tk.Button(root, text="Back to Bills", bg="#007bff", fg="white", font=("Arial", 11, "bold"), command=self.close_command).pack(pady=40, fill="x", padx=40)