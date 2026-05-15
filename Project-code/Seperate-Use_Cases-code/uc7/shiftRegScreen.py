import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ShiftRegScreen:
    def __init__(self, root, worker_id, name, surname, role, controller):
        self.root = root
        self.controller = controller

        self.root.configure(bg="#f0f2f5")
        self.root.title("Shift Registration")
        self.root.geometry("600x750")

        self.worker_data = {
            "First Name": name,
            "Last Name": surname,
            "Specialization": role,
            "ID": worker_id}

        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        title_label = tk.Label(
            self.main_frame,
            text="Shift Registration",
            font=("Segoe UI", 22, "bold"),
            fg="#1a73e8",
            bg="#f0f2f5"
        )
        title_label.pack(pady=(0, 25))

        info_card = tk.Frame(
            self.main_frame,
            bg="white",
            padx=20,
            pady=15,
            highlightbackground="#dcdfe3",
            highlightthickness=1
        )
        info_card.pack(fill="x", padx=10, pady=10)

        for label_text, value in self.worker_data.items():
            row = tk.Frame(info_card, bg="white")
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=f"{label_text}:",
                font=("Segoe UI", 9, "bold"),
                fg="#5f6368",
                bg="white",
                width=16,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Segoe UI", 10),
                fg="#202124",
                bg="white",
                anchor="w"
            ).pack(side="left", padx=10)

        form_card = tk.Frame(
            self.main_frame,
            bg="white",
            padx=30,
            pady=30,
            highlightbackground="#dcdfe3",
            highlightthickness=1
        )
        form_card.pack(fill="x", padx=10, pady=10)

        form_card.grid_columnconfigure(1, weight=1)

        self.inputs = {}

        fields = [
            ("Date (YYYY-MM-DD)", "date"),
            ("Shift Type", "type"),
            ("Start Time (HH:MM)", "begin"),
            ("End Time (HH:MM)", "end")
        ]

        for i, (label_text, key) in enumerate(fields):
            label = tk.Label(
                form_card,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg="#202124",
                bg="white"
            )
            label.grid(row=i, column=0, sticky="w", pady=10)

            if key == "type":
                widget = ttk.Combobox(
                    form_card,
                    values=["Morning", "Afternoon", "Night"],
                    font=("Segoe UI", 10),
                    state="readonly"
                )
                widget.current(0)
            else:
                widget = tk.Entry(
                    form_card,
                    font=("Segoe UI", 11),
                    bg="#f8f9fa",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#dcdfe3")

            widget.grid(row=i, column=1, sticky="ew", padx=(20, 0), pady=10)
            self.inputs[key] = widget

        button_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        button_frame.pack(fill="x", pady=20)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.controller.parent_controller.displaySearchScreen,
            font=("Segoe UI", 10, "bold"),
            bg="#DC143C",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat",
            activebackground="#b01030",
            activeforeground="white")

        cancel_btn.pack(side="left")

        save_btn = tk.Button(
            button_frame,
            text="Save Shift",
            command=lambda: self.controller.getForm({"worker_id": self.worker_data["ID"],"date": self.inputs["date"].get(),"type": self.inputs["type"].get(),"begin": self.inputs["begin"].get(),"end": self.inputs["end"].get()}),
            font=("Segoe UI", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat",
            activebackground="#1558b0",
            activeforeground="white")

        save_btn.pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()