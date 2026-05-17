import tkinter as tk


class PaymentMethodSelectScreen:
    def __init__(self, root, methods, on_select, back_command):
        self.root = root
        self.on_select = on_select

        self.root.title("Payment Methods")
        self.root.geometry("400x600")
        self.root.configure(bg="#ffffff")

        # -------- Header --------
        header = tk.Frame(self.root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        tk.Button(header, text="← Back", font=("Arial", 10), bg="white", relief="flat", command=back_command).pack(side="left", padx=20)

        # -------- Content --------
        tk.Label(self.root, text="Choose Payment Method", font=("Arial", 16, "bold"), bg="#ffffff", fg="#1a1c3d").pack(pady=(30, 40))

        # -------- Payment Cards --------
        options_frame = tk.Frame(self.root, bg="#ffffff")
        options_frame.pack(padx=50, fill="x")

        for method in methods:
            icon = "💳" if method == "Debit" else "🪪"

            self.create_method_button(options_frame, f"{method} Card", icon, lambda m=method: self.on_select(m))

            tk.Frame(options_frame, height=15, bg="#ffffff").pack()

    def create_method_button(self, parent, text, icon, command):
        btn = tk.Button(parent, text=f"{icon}   {text}", font=("Arial", 12, "bold"), bg="#f9f9f9", fg="#1a1c3d", activebackground="#ececec", relief="solid", bd=1, height=3, command=command)

        btn.pack(fill="x", pady=5)