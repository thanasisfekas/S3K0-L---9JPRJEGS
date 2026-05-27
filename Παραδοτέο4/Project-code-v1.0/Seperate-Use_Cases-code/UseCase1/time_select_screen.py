import tkinter as tk
from tkinter import messagebox


class TimeSelectScreen:
    def __init__(self, root, slots, selected_date, selected_specialty, selected_doctor, on_select, back_command):
        self.root = root
        self.root.configure(bg="#ffffff")

        header = tk.Frame(root, bg="#ffffff")
        header.pack(fill="x", pady=(20, 10))

        tk.Button(header, text="← Back", bg="white", relief="flat", command=back_command).pack(side="left", padx=20)
        tk.Label(root, text="Choose Appointment Time", font=("Arial", 16, "bold"), bg="#ffffff", fg="#1a1c3d").pack(pady=(20, 10))

        self.selection_card([("Date", selected_date), ("Specialty", selected_specialty), ("Doctor", selected_doctor)])

        container = tk.Frame(root, bg="#ffffff")
        container.pack(fill="both", expand=True, padx=50, pady=20)
        canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg="#ffffff")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=frame, anchor="nw")

        def resize_frame(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", resize_frame)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        canvas.bind("<Enter>", lambda e: canvas.focus_set())
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        scrollbar.pack(side="right", fill="y", padx=(8, 0))

        for slot in slots:
            tk.Button(frame, text=slot, font=("Arial", 12), bg="#f9f9f9", fg="#1a1c3d", activebackground="#ececec", relief="solid", bd=1, height=3, command=lambda s=slot: on_select(s)).pack(fill="x", pady=8)

    def selection_card(self, items):
        card = tk.Frame(self.root, bg="#f9f9f9", bd=1, relief="solid")
        card.pack(fill="x", padx=50, pady=10)

        for label, value in items:
            row = tk.Frame(card, bg="#f9f9f9")
            row.pack(fill="x", padx=20, pady=6)

            tk.Label(row, text=f"{label}:", font=("Arial", 11, "bold"), bg="#f9f9f9").pack(side="left")
            tk.Label(row, text=value, font=("Arial", 11), bg="#f9f9f9").pack(side="right")

    def showError(self, message):
        messagebox.showerror("Unavailable", message)