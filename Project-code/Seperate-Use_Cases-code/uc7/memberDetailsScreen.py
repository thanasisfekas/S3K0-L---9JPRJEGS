import tkinter as tk

class MemberDetailsScreen:
    def __init__(self, root, details, controller):
        self.root = root
        self.data = details
        self.controller = controller
        
        self.root.configure(bg="#f0f2f5")
        
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=20)

    
        tk.Label(
            self.main_frame, 
            text="Staff Member Details", 
            font=("Segoe UI", 20, "bold"),
            fg="#1a73e8",
            bg="#f0f2f5"
        ).pack(pady=(0, 20))


        card_frame = tk.Frame(
            self.main_frame, 
            bg="white", 
            padx=30, 
            pady=30,
            highlightbackground="#dcdfe3",
            highlightthickness=1
        )
        card_frame.pack(pady=10, padx=50, fill="x")

        labels = ["First Name", "Last Name", "Property", "ID", "Phone Number"]

        if self.data and isinstance(self.data, tuple):
            for label_text, value in zip(labels, self.data):
                row = tk.Frame(card_frame, bg="white")
                row.pack(fill="x", pady=8)

                tk.Label(
                    row, 
                    text=f"{label_text.upper()}:", 
                    font=("Segoe UI", 9, "bold"),
                    fg="#5f6368",
                    bg="white",
                    width=15,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    row, 
                    text=value, 
                    font=("Segoe UI", 11),
                    fg="#202124",
                    bg="white",
                    anchor="w"
                ).pack(side="left", padx=10)
                
            
                line = tk.Frame(card_frame, height=1, bg="#e8eaed")
                line.pack(fill="x", pady=2)
        
    
        tk.Button(
            self.main_frame,
            text="Cancel",
            command=lambda:self.controller.displaySearchScreen(), 
            font=("Segoe UI", 10, "bold"),
            bg="#DC143C",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat"
        ).place(relx=0.02, rely=0.95, anchor="sw")

        tk.Button(
            self.main_frame,
            text="Create Shift",
            command=lambda:self.controller.createShiftController(), 
            font=("Segoe UI", 10, "bold"),
            bg="#1a73e8",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat"
        ).place(relx=0.90, rely=0.95, anchor="sw")

