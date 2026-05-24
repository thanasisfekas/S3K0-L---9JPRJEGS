import tkinter as tk
from tkinter import ttk


class SurgeryRequestScreen:
    def __init__(self, root, controller, on_back_click):
        self.root = root
        self.controller = controller
        self.on_back_click = on_back_click

        self.root.title("Surgery Requests")
        self.root.geometry("1550x600")  # Slightly widened to display new columns comfortably
        self.root.configure(bg="#ffffff")

        self.create_widgets()
        # Fetch and load rows via the controller reference mapping
        self.load_records()

    def create_widgets(self):
        # --- Top Header Area ---
        header_frame = tk.Frame(self.root, bg="#ffffff")
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text="SURGERY REQUESTS",
                 font=("Arial", 10, "bold"), bg="#ffffff", fg="#666").pack()

        # --- Central Data Grid ---
        grid_frame = tk.Frame(self.root, bg="#ffffff")
        grid_frame.pack(padx=30, fill="both", expand=True, pady=10)

        # UPDATED: Added "doctors_needed" and "specialty_needed" to the columns tuple
        '''
        columns = ("request_id", "patient_id", "doctor_name", "surgery_type",
                   "urgency", "requested_date", "status", "doctors_needed", "specialty_needed")
        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings")
        '''

        # Update this line inside SurgeryRequestScreen.create_widgets()
        columns = ("request_id", "patient_id", "doctor_name", "surgery_type", "urgency",
                   "requested_date", "status", "doctors_needed", "specialty_needed",
                   "assigned_operating_room", "nurses_needed")

        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings")

        # Add the new column headings and formatting alignments
        self.tree.heading("assigned_operating_room", text="Assigned OR")
        self.tree.heading("nurses_needed", text="Nurses Req.")

        self.tree.column("assigned_operating_room", width=160, anchor="w")
        self.tree.column("nurses_needed", width=90, anchor="center")

        self.tree.heading("request_id", text="Request ID")
        self.tree.heading("patient_id", text="Patient ID")
        self.tree.heading("doctor_name", text="Doctor")
        self.tree.heading("surgery_type", text="Surgery Type")
        self.tree.heading("urgency", text="Urgency")
        self.tree.heading("requested_date", text="Date")
        self.tree.heading("status", text="Status")
        # UPDATED: Headings for the new data points
        self.tree.heading("doctors_needed", text="Docs Needed")
        self.tree.heading("specialty_needed", text="Specialty Needed")

        self.tree.column("request_id", width=90, anchor="center")
        self.tree.column("patient_id", width=90, anchor="center")
        self.tree.column("doctor_name", width=140, anchor="w")
        self.tree.column("surgery_type", width=180, anchor="w")
        self.tree.column("urgency", width=90, anchor="center")
        self.tree.column("requested_date", width=90, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        # UPDATED: Layout alignments and distributions for new columns
        self.tree.column("doctors_needed", width=90, anchor="center")
        self.tree.column("specialty_needed", width=130, anchor="w")

        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- Bottom Action Buttons ---
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=30)

        tk.Button(btn_frame, text="← Back", font=("Arial", 10),
                  bg="#ffffff", fg="#666", relief="flat",
                  command=self.on_back_click).pack(side="left")

        self.btn_schedule = tk.Button(btn_frame, text="Process", font=("Arial", 10, "bold"),
                                      bg="#cccccc", fg="white", relief="flat",
                                      width=12, height=2, state="disabled",
                                      command=self.on_process_click)
        self.btn_schedule.pack(side="right")

    def load_records(self):
        """ Clears list and requests rows from the controller """
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.controller.get_surgery_requests()
        for row in records:
            self.tree.insert("", "end", values=row)

    def on_row_select(self, event):
        if self.tree.selection():
            self.btn_schedule.config(state="normal", bg="#007bff")
        else:
            self.btn_schedule.config(state="disabled", bg="#cccccc")

    def on_process_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item[0], "values")
        # Extract row meta context to pass back into the controller handling methods
        request_id = row_values[0]
        specialty_needed = row_values[8]

        self.controller.display_surgery_form(request_id, specialty_needed)

























'''
class SurgeryRequestScreen:
    def __init__(self, root, controller, on_back_click):
        self.root = root
        self.controller = controller
        self.on_back_click = on_back_click

        self.root.title("Surgery Requests")
        self.root.geometry("900x600")
        self.root.configure(bg="#ffffff")

        self.create_widgets()
        # Fetch and load rows via the controller reference mapping
        self.load_records()

    def create_widgets(self):
        # --- Top Header Area ---
        header_frame = tk.Frame(self.root, bg="#ffffff")
        header_frame.pack(fill="x", pady=20)

        tk.Label(header_frame, text="SURGERY REQUESTS",
                 font=("Arial", 10, "bold"), bg="#ffffff", fg="#666").pack()

        # --- Central Data Grid ---
        grid_frame = tk.Frame(self.root, bg="#ffffff")
        grid_frame.pack(padx=30, fill="both", expand=True, pady=10)

        columns = ("request_id", "patient_id", "doctor_name", "surgery_type", "urgency", "requested_date", "status")
        self.tree = ttk.Treeview(grid_frame, columns=columns, show="headings")

        self.tree.heading("request_id", text="Request ID")
        self.tree.heading("patient_id", text="Patient ID")
        self.tree.heading("doctor_name", text="Doctor")
        self.tree.heading("surgery_type", text="Surgery Type")
        self.tree.heading("urgency", text="Urgency")
        self.tree.heading("requested_date", text="Date")
        self.tree.heading("status", text="Status")

        self.tree.column("request_id", width=100, anchor="center")
        self.tree.column("patient_id", width=100, anchor="center")
        self.tree.column("doctor_name", width=150, anchor="w")
        self.tree.column("surgery_type", width=200, anchor="w")
        self.tree.column("urgency", width=100, anchor="center")
        self.tree.column("requested_date", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # --- Bottom Action Buttons ---
        btn_frame = tk.Frame(self.root, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=30, padx=30)

        tk.Button(btn_frame, text="← Back", font=("Arial", 10),
                  bg="#ffffff", fg="#666", relief="flat",
                  command=self.on_back_click).pack(side="left")

        self.btn_schedule = tk.Button(btn_frame, text="Process", font=("Arial", 10, "bold"),
                                      bg="#cccccc", fg="white", relief="flat",
                                      width=12, height=2, state="disabled",
                                      command=self.on_process_click)
        self.btn_schedule.pack(side="right")

    def load_records(self):
        """ Clears list and requests rows from the controller """
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.controller.get_surgery_requests()
        for row in records:
            self.tree.insert("", "end", values=row)

    def on_row_select(self, event):
        if self.tree.selection():
            self.btn_schedule.config(state="normal", bg="#007bff")
        else:
            self.btn_schedule.config(state="disabled", bg="#cccccc")

    def on_process_click(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        row_values = self.tree.item(selected_item[0], "values")
        # Extract row meta context to pass back into the controller handling methods
        request_id = row_values[0]
        patient_id = row_values[1]

        self.controller.display_surgery_form(request_id, patient_id)
# --- INDEPENDENT TEST / RUN VERIFICATION HARNESS CONTAINER ---


if __name__ == "__main__":
    app_root = tk.Tk()


    def simulate_back():
        print("Navigation Request: Re-routing execution track back to Main Desktop Dashboard Hub Screen Workspace.")
        app_root.destroy()


    def simulate_action(req_id, pat_id):
        print(
            f"Action Hook Triggered Successfully: Initializing workflow assignment for target: {req_id} bound to Patient: {pat_id}")


    active_screen = SurgeryRequestScreen(app_root, on_back_click=simulate_back, on_action_click=simulate_action)
    app_root.mainloop()
'''