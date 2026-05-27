import os
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import random
from pathlib import Path
from Bill_Issue.Screens.bill_issueing_screen import BillIssuingScreen
from data_paths import data_path

# Assuming BillIssuingScreen is imported from your Screens package
# from Bill_Payment.Screens.bill_issuing_screen import BillIssuingScreen



class BillController:
    def __init__(self, root, patient_id, patient_name, insurance_provider, treatments, prescriptions, on_back_click):
        """
        Initializes the controller with patient context, including insurance provider data.
        """
        self.root = root
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.insurance_provider = str(insurance_provider).strip()
        self.treatments = treatments
        self.prescriptions = prescriptions
        self.on_back_click = on_back_click

        # Financial variables tracking
        self.insurance_discount_ratio = 0.0  # Percentage coverage (e.g., 0.50 for 50%)
        self.insurance_deduction_amount = 0.0

    def display_bill_issue_screen(self):
        """Clears the screen, evaluates insurance coverage adjustments, and loads the UI."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Run insurance calculation prior to rendering view
        self.check_insurance()

        # Import screen here to avoid circular dependencies
        # from Bill_Payment.Screens.bill_issuing_screen import BillIssuingScreen

        # Launch screen, passing the save callback hook
        return BillIssuingScreen(
            root=self.root,
            patient_id=self.patient_id,
            patient_name=self.patient_name,
            treatments=self.treatments,
            prescriptions=self.prescriptions,
            on_back=self.on_back_click,
            on_confirm=self.save_bill
        )

    def check_insurance(self):
        """
        Validates insurance status. If the patient has an active provider,
        generates a random coverage cut percentage between 20% and 80%.
        """
        no_insurance_keywords = ['none', 'no insurance', 'nan', '', 'null']

        if self.insurance_provider.lower() in no_insurance_keywords:
            self.insurance_discount_ratio = 0.0
            print(f"[Insurance Check] Patient {self.patient_id} has no coverage provider listed.")
        else:
            # Generate a random integer percentage between 20% and 80%
            discount_percent = random.randint(20, 80)
            self.insurance_discount_ratio = discount_percent / 100.0
            print(
                f"[Insurance Check] Active Provider: {self.insurance_provider}. Coverage Approved: {discount_percent}% cut.")

    def calculate_bill(self, selected_treats, selected_prescs):
        """
        Backend business logic validation method.
        Calculates subtotal, applies the insurance markdown cut, and returns final parameters.
        """
        subtotal = 0.0

        # Sum selected item values out of initial memory references
        for t_id in selected_treats:
            item = next((t for t in self.treatments if t['id'] == t_id), None)
            if item: subtotal += item['cost']

        for p_id in selected_prescs:
            item = next((p for p in self.prescriptions if p['id'] == p_id), None)
            if item: subtotal += item['cost']

        # Apply the pre-calculated random insurance cut
        self.insurance_deduction_amount = subtotal * self.insurance_discount_ratio
        final_total = subtotal - self.insurance_deduction_amount

        return subtotal, self.insurance_deduction_amount, final_total

    def check_if_bill_issued(self, selected_treats, selected_prescs):
        """
        NEW METHOD: Scans final_billing4.csv to ensure none of the selected
        treatments or prescriptions have already been billed for this patient.
        Returns a tuple: (bool_already_issued, list_of_already_billed_ids)
        """
        csv_path = data_path("final_billing4.csv")

        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            return False, []

        try:
            df = pd.read_csv(csv_path)

            # Filter the billing history ledger specifically down to this patient
            patient_history = df[df['patient_id'] == self.patient_id]
            if patient_history.empty:
                return False, []

            already_billed = []

            # Check for already billed treatments
            existing_treats = patient_history['treatment_id'].dropna().astype(str).tolist()
            for t_id in selected_treats:
                if str(t_id) in existing_treats:
                    already_billed.append(t_id)

            # Check for already billed prescriptions
            if 'prescription_id' in patient_history.columns:
                existing_prescs = patient_history['prescription_id'].dropna().astype(str).tolist()
                for p_id in selected_prescs:
                    if str(p_id) in existing_prescs:
                        already_billed.append(p_id)

            if already_billed:
                return True, already_billed

            return False, []

        except Exception as e:
            print(f"[Duplicate Detection Warning] Could not parse log for historical duplicates: {e}")
            return False, []

    def save_bill(self, selected_treats, selected_prescs, screen_amount_passed):
        """
        Saves the issued bill items into final_billing4.csv following its layout:
        bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status, prescription_id
        """
        # 1. Validation check to make sure items are selected
        if not selected_treats and not selected_prescs:
            messagebox.showwarning("Selection Error",
                                   "Please select at least one treatment or prescription to issue a bill.")
            return

        # 1b. NEW STEP: Intercept and halt execution if items have already been invoiced
        is_duplicate, duplicate_ids = self.check_if_bill_issued(selected_treats, selected_prescs)
        if is_duplicate:
            item_list = ", ".join(duplicate_ids)
            messagebox.showerror(
                "Duplicate Billing Detected",
                f"Action Denied! A bill has already been issued for the following item(s) to this patient:\n\n{item_list}"
            )
            return

        try:
            csv_path = data_path("final_billing4.csv")

            # 2. Load existing records to maintain sequential bill_id integrity
            if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
                df_existing = pd.read_csv(csv_path)
                try:
                    max_id = df_existing['bill_id'].str.extract(r'B(\d+)').astype(int).max()[0]
                    next_id_num = int(max_id) + 1
                except:
                    next_id_num = len(df_existing) + 1
            else:
                df_existing = pd.DataFrame(columns=[
                    'bill_id', 'patient_id', 'treatment_id', 'bill_date',
                    'amount', 'payment_method', 'payment_status', 'prescription_id'
                ])
                next_id_num = 1

            new_rows = []
            bill_date_str = datetime.now().strftime('%Y-%m-%d')

            # 3. Choose primary payment classification according to insurance coverage
            if self.insurance_discount_ratio > 0:
                payment_method = "Insurance"
            else:
                payment_method = "Cash"

            # 4. Insert an itemized row for each selected treatment
            for t_id in selected_treats:
                item = next((t for t in self.treatments if t['id'] == t_id), None)
                if item:
                    final_item_cost = item['cost'] * (1 - self.insurance_discount_ratio)
                    new_rows.append({
                        'bill_id': f"B{next_id_num:03d}",
                        'patient_id': self.patient_id,
                        'treatment_id': t_id,
                        'bill_date': bill_date_str,
                        'amount': round(final_item_cost, 2),
                        'payment_method': payment_method,
                        'payment_status': 'Pending',
                        'prescription_id': None
                    })
                    next_id_num += 1

            # 5. Insert an itemized row for each selected prescription
            for p_id in selected_prescs:
                item = next((p for p in self.prescriptions if p['id'] == p_id), None)
                if item:
                    final_item_cost = item['cost'] * (1 - self.insurance_discount_ratio)
                    new_rows.append({
                        'bill_id': f"B{next_id_num:03d}",
                        'patient_id': self.patient_id,
                        'treatment_id': None,
                        'bill_date': bill_date_str,
                        'amount': round(final_item_cost, 2),
                        'payment_method': payment_method,
                        'payment_status': 'Pending',
                        'prescription_id': p_id
                    })
                    next_id_num += 1

            # 6. Append and save back to the primary database
            df_new = pd.DataFrame(new_rows)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_path, index=False)

            # 7. Provide detailed text response and window feedback notification
            subtotal, deduction, total_due = self.calculate_bill(selected_treats, selected_prescs)
            if self.insurance_discount_ratio > 0:
                msg = (f"Successfully generated {len(new_rows)} invoice line(s) in final_billing4.csv!\n\n"
                       f"Subtotal: ${subtotal:.2f}\n"
                       f"Insurance Cut ({int(self.insurance_discount_ratio * 100)}%): -${deduction:.2f}\n"
                       f"Patient Total Due: ${total_due:.2f}")
            else:
                msg = f"Successfully generated {len(new_rows)} invoice line(s)!\n\nTotal Due: ${total_due:.2f} (No Insurance)"

            messagebox.showinfo("Success", msg)
            self.on_back_click()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to append transaction records: {e}")
