import pandas as pd
import tkinter as tk
import os
from pathlib import Path
from Bill_Issue.Screens.search_patient_screen import PatientSearchScreen
from Bill_Issue.Screens.patient_details_screen import PatientDetailScreen
from bill_issue_controller import BillController
from data_paths import data_path

class SearchChargesController:
    def __init__(self, root, csv_path):
        self.root = root
        self.csv_path = csv_path
        self.patients_df = None
        self.load_data()

    def load_data(self):
        """Loads CSV and combines name columns."""
        try:
            df = pd.read_csv(self.csv_path)

            # Combine First and Last name into a single helper column
            # We use .fillna('') to prevent 'NaN' if a name is missing
            df['full_name'] = (df['first_name'].fillna('') + ' ' +
                               df['last_name'].fillna('')).str.strip()

            self.patients_df = df
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.patients_df = pd.DataFrame(columns=['patient_id', 'first_name', 'last_name', 'date_of_birth'])

    def display_search_screen(self):
        """Prepares data and shows the independent search screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Map your CSV columns to the keys the PatientSearchScreen expects
        patient_list = []
        for _, row in self.patients_df.iterrows():
            patient_list.append({
                'id': row['patient_id'],
                'name': row['full_name'],  # Using our combined name
                'dob': row['date_of_birth']
            })

        return PatientSearchScreen(
            self.root,
            patient_list,
            on_patient_select=self.get_patient
        )

    def get_patient(self, patient_id):
        """Finds the patient by ID when selected from the list."""
        # Find the specific row
        patient_data = self.patients_df[self.patients_df['patient_id'] == patient_id].iloc[0]
        print(f"Secretary selected: {patient_data['full_name']}")

        # Move to the next step
        self.show_patient_details(patient_data)

    # Inside SearchChargesController

    def show_patient_details(self, patient_data):
        """Transition to the Detailed Patient View."""
        for widget in self.root.winfo_children():
            widget.destroy()

        return PatientDetailScreen(
            self.root,
            patient_data=patient_data,
            back_command=self.display_search_screen,
            # Ensure this parameter matches whatever button property name you used
            # (e.g., 'proceed_command' or 'issue_bill_command')
            proceed_command=lambda: self.check_charges(patient_data['patient_id'])
        )

    # We pass the row data directly from the CSV datafram

    def get_hosp_services_perscriptions(self, patient_id):
        """
        Retrieves all treatments and prescriptions associated with a specific patient.
        Returns two clean lists of dictionaries: (treatments, prescriptions)
        """
        import pandas as pd
        import os

        patient_prescriptions = []
        patient_treatments = []

        # --- 1. Fetch and Merge Prescriptions ---
        try:
            prescriptions_path = data_path("usecase9_prescriptions.csv")
            medicines_path = data_path("usecase9_medicines.csv")
            if prescriptions_path.exists() and medicines_path.exists():
                df_presc = pd.read_csv(prescriptions_path)
                df_meds = pd.read_csv(medicines_path)

                # Filter prescriptions for this specific patient
                df_patient_presc = df_presc[df_presc['patient_id'] == patient_id]

                # Merge with medicines database to get name and unit price
                merged_presc = df_patient_presc.merge(df_meds, on='medicine_id', how='inner')

                for _, row in merged_presc.iterrows():
                    patient_prescriptions.append({
                        'id': row['prescription_id'],
                        'item_name': row['name'],
                        'category': row['category'],
                        'date': row['date'],
                        'dosage': row['dosage'],
                        'cost': float(row['price']),
                        'status': row['status']
                    })
        except Exception as e:
            print(f"Error fetching prescriptions data: {e}")

        # --- 2. Fetch and Map Treatments ---
        try:
            treatments_path = data_path("treatments.csv")
            if treatments_path.exists():
                df_treatments = pd.read_csv(treatments_path)

                # If you have an appointments mapping file, merge through it
                appointments_path = data_path("appointments.csv")
                if appointments_path.exists():
                    df_apps = pd.read_csv(appointments_path)
                    df_patient_apps = df_apps[df_apps['patient_id'] == patient_id]
                    merged_treatments = df_treatments.merge(df_patient_apps, on='appointment_id', how='inner')
                else:
                    # Fallback relational mapping logic matching the 50-patient distribution cycle
                    df_treatments['derived_patient_id'] = df_treatments['appointment_id'].apply(
                        lambda app_id: f"P{(int(app_id[1:]) - 1) % 50 + 1:03d}" if pd.notna(app_id) else ""
                    )
                    merged_treatments = df_treatments[df_treatments['derived_patient_id'] == patient_id]

                for _, row in merged_treatments.iterrows():
                    patient_treatments.append({
                        'id': row['treatment_id'],
                        'item_name': row['treatment_type'],
                        'description': row['description'],
                        'date': row['treatment_date'],
                        'cost': float(row['cost'])
                    })
        except Exception as e:
            print(f"Error fetching treatments data: {e}")

        return patient_treatments, patient_prescriptions

    # Inside SearchChargesController

    def check_charges(self, patient_id):
        """
        Triggered when clicking 'Check Charges & Issue Bill' or 'Issue Bill'.
        Fetches the data, validates it, and hands control over to the BillController.
        """
        from tkinter import messagebox
        # Import your BillController here if it's in another file
        # from Bill_Payment.Controllers.bill_controller import BillController

        # 1. Fetch data from your existing helper function
        treatments, prescriptions = self.get_hosp_services_perscriptions(patient_id)

        # 2. Redirect back if there is nothing to bill
        if not treatments and not prescriptions:
            messagebox.showwarning("No Charges Found", "This patient has no recorded items to bill.")
            self.display_search_screen()
            return

        # 3. Pull patient profile details for their full name
        patient_row = self.patients_df[self.patients_df['patient_id'] == patient_id].iloc[0]
        full_name = f"{patient_row['first_name']} {patient_row['last_name']}"
        insurance = patient_row['insurance_provider']  # Pull data out of patients.csv column directly

        for widget in self.root.winfo_children():
            widget.destroy()

        # Pass the extra insurance column parameter into the initializer setup
        self.bill_module = BillController(
            root=self.root,
            patient_id=patient_id,
            patient_name=full_name,
            insurance_provider=insurance,
            treatments=treatments,
            prescriptions=prescriptions,
            on_back_click=self.display_search_screen
        )

        self.bill_module.display_bill_issue_screen()

    '''
    def check_charges(self, patient_id):
        """Calculates totals and prints/displays the charges statement."""
        # Call the new data function
        treatments, prescriptions = self.get_hosp_services_perscriptions(patient_id)

        # Calculate totals using a generator expression: Total = sum(cost_i)
        total_treatments_cost = sum(t['cost'] for t in treatments)
        total_prescriptions_cost = sum(p['cost'] for p in prescriptions)
        grand_total = total_treatments_cost + total_prescriptions_cost

        print(f"--- Charges Statement for {patient_id} ---")
        print(f"Treatments Found: {len(treatments)} (${total_treatments_cost:.2f})")
        print(f"Prescriptions Found: {len(prescriptions)} (${total_prescriptions_cost:.2f})")
        print(f"Grand Total Billable Amount: ${grand_total:.2f}")

        # Inside SearchChargesController

        def generate_invoice_records(self, patient_id, full_name, treatments, prescriptions):
            """
            Acts as the hand-off bridge. Instantiates the BillController
            to take over layout control for the billing summary screen sequence.
            """
            # Create the secondary controller instance, passing current root frame
            self.bill_module = BillController(
                root=self.root,
                patient_id=patient_id,
                patient_name=full_name,
                treatments=treatments,
                prescriptions=prescriptions,
                # If they click back inside the module, bring them back here to search panel
                on_back_click=self.display_search_screen
            )

            # Launch the billing screen
            self.bill_module.display_bill_issue_screen()

        # Next Step: Pass (treatments, prescriptions, grand_total)
        # to your billing invoice screen!
    '''
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hospital Billing System - Secretary Mode")
    root.geometry("600x800")

    # Initialize the controller
    controller = SearchChargesController(root, data_path("patients.csv"))

    # Start the application at the search screen
    controller.display_search_screen()

    root.mainloop()
