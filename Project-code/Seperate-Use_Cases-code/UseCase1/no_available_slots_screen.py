import tkinter as tk


class NoAvailableSlotsScreen:
    def __init__(self, root, on_next, back_command):
        self.root = root
        self.root.configure(bg="#ffffff")

        header = tk.Frame(root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        tk.Button(header, text="← Back", bg="white", relief="flat", command=back_command).pack(side="left", padx=20)
        tk.Label(root, text="No Available Slots", font=("Arial", 18, "bold"), fg="red", bg="#ffffff").pack(pady=50)
        tk.Label(root, text="No slots found for this date.", font=("Arial", 12), bg="#ffffff").pack(pady=10)
        tk.Button(root, text="Find Next Available Date", bg="#007bff", fg="white", font=("Arial", 12, "bold"), height=2, command=on_next).pack(fill="x", padx=60, pady=40)