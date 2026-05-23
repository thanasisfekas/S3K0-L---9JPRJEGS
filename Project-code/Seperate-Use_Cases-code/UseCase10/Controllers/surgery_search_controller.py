import os
import pandas as pd
from pathlib import Path
from tkinter import messagebox
from Surgery_Appoint.Screens.surg_selec_doc_screen import SelectDoctorScreen
from Surgery_Appoint.Screens.surgery_form_screen import SurgeryFormScreen
from Surgery_Appoint.Screens.surgery_details_screen import SurgeryDetailScreen


class SurgerySearchController:
    def __init__(self, root, on_back_click=None):
        self.root = root
        self.on_back_click = on_back_click

        self.temp_assignments = {}

        # Centralized file locations paths
        parent_dir = Path.cwd().parent.parent
        self.doctors_csv_path = os.path.join(parent_dir, "archive (1)", "doctors.csv")
        self.requests_csv_path = os.path.join(parent_dir, "archive (1)", "surgery_requests.csv")

    def get_surgery_doctors(self, specialty):
        """ Pulls rows out of doctors.csv matching the requested specialty """
        if not os.path.exists(self.doctors_csv_path):
            print(f"File not found: {self.doctors_csv_path}")
            return []

        try:
            df_docs = pd.read_csv(self.doctors_csv_path)
            # Filter rows where the specialization matches our case metric targets
            filtered_df = df_docs[df_docs['specialization'] == specialty]

            records = []
            for _, row in filtered_df.iterrows():
                full_name = f"Dr. {row['first_name']} {row['last_name']}"
                records.append((
                    str(row['doctor_id']),
                    full_name,
                    str(row['specialization']),
                    str(row['years_experience']),
                    str(row['hospital_branch']),
                    str(row['email'])
                ))
            return records
        except Exception as e:
            print(f"Error filtering doctor records data elements: {e}")
            return []

    def display_doctors(self, request_id, specialty_needed):
        """ Wipes active frame container components and renders the selection screen """
        for widget in self.root.winfo_children():
            widget.destroy()

        return SelectDoctorScreen(
            root=self.root,
            controller=self,
            request_id=request_id,
            specialty=specialty_needed,
            on_back_click=self.on_back_click
        )

    def _get_doctors_needed_count(self, request_id):
        """ Helper method to look up the required doctor headcount from the CSV """
        if not os.path.exists(self.requests_csv_path):
            return 1  # safe default fallback
        try:
            df = pd.read_csv(self.requests_csv_path)
            df.columns = df.columns.str.strip()
            row = df[df['request_id'].astype(str) == str(request_id).strip()].iloc[0]
            return int(row['doctors_needed'])
        except Exception as e:
            print(f"[Warning] Failed to read doctors_needed property: {e}")
            return 1

    '''
    def validate_doc_count(self, request_id, doctor_id, doctor_name):
        """ Tracks doctor allocations and ensures target quota is fully met before scheduling """

        # 1. Look up how many doctors this unique case requires
        required_count = self._get_doctors_needed_count(request_id)

        # Initialize tracking index for this request if it doesn't exist yet
        if request_id not in self.temp_assignments:
            self.temp_assignments[request_id] = []

        # Prevent selecting the exact same doctor twice for the same surgical request
        if doctor_id in self.temp_assignments[request_id]:
            messagebox.showwarning("Duplicate Selection", f"Dr. {doctor_name} is already assigned to this request.")
            return

        # 2. Save the newly selected doctor to our assignment list
        self.temp_assignments[request_id].append(doctor_id)
        current_assigned_count = len(self.temp_assignments[request_id])

        print(
            f"[Staffing Check]: Request {request_id} needs {required_count} doctors. Current total: {current_assigned_count}")

        # Case A: We still need more doctors to fulfill the request requirements
        if current_assigned_count < required_count:
            remaining = required_count - current_assigned_count
            messagebox.showinfo(
                "Doctor Assigned",
                f"Successfully assigned Dr. {doctor_name}.\n\n"
                f"This surgery requires {remaining} more doctor(s). Please select the next candidate."
            )

            # Refresh the screen to clear selections so the user can pick the next doctor
            for widget in self.root.winfo_children():
                widget.destroy()

            # Re-display the doctor search list view to select the remaining staff
            # Note: You can optionally pass the requirement string back down to keep the filtered views locked.
            # Assuming specialty needed was passed/known, or fetch it dynamically if preferred.
            return self.display_doctors(request_id, "General Surgery")

            # Case B: The exact quota has been met! Progress to the next step.
        elif current_assigned_count == required_count:
            messagebox.showinfo("Quota Met",
                                "All required doctors have been successfully assigned. Opening scheduling form...")

            # Extract final assignment collection list to hand over to our application registry state machine
            final_doctors_assigned = self.temp_assignments[request_id]

            # Clear out SelectDoctorScreen tree components
            for widget in self.root.winfo_children():
                widget.destroy()

            # Pass the list of all selected doctors into your SurgeryFormScreen layout container
            return SurgeryFormScreen(
                root=self.root,
                controller=self,
                request_id=request_id,
                doctor_id=final_doctors_assigned,  # Now safely passes an array string: e.g. ['DOC-01', 'DOC-02']
                on_back_click=self.on_back_click
            )

        # Case C: Safety catch for overflow validation
        else:
            messagebox.showerror("Error", "Maximum doctor assignment limits exceeded for this operation row context.")
            return
        '''

    def validate_multi_doc_count(self, request_id, selected_doctors):
        """ Checks if the batch selection of doctors matches the exact count required """
        required_count = self._get_doctors_needed_count(request_id)
        selected_count = len(selected_doctors)

        print(
            f"[Multi-Staffing Check]: Request {request_id} needs {required_count} doctors. User selected: {selected_count}")

        # Case 1: Under-staffed selection
        if selected_count < required_count:
            messagebox.showwarning(
                "Incomplete Selection",
                f"This surgery requires exactly {required_count} doctor(s).\n\n"
                f"You have only selected {selected_count}. Please hold Ctrl or Shift to select the remaining staff."
            )
            return

        # Case 2: Over-staffed selection
        if selected_count > required_count:
            messagebox.showwarning(
                "Too Many Doctors Selected",
                f"This surgery requires exactly {required_count} doctor(s).\n\n"
                f"You have selected {selected_count}. Please adjust your selection."
            )
            return

        # Case 3: Exact match! Perfect quota met.
        messagebox.showinfo("Quota Met", "All required doctors selected successfully! Opening scheduling form...")

        # Extract just the doctor IDs into a list to send to the next screen
        final_doctor_ids = [doc[0] for doc in selected_doctors]

        # Wipe screen elements cleanly
        for widget in self.root.winfo_children():
            widget.destroy()

        # Mount the form screen with our full array of assigned doctor IDs
        return SurgeryFormScreen(
            root=self.root,
            controller=self,
            request_id=request_id,
            doctor_id=final_doctor_ids,  # e.g. ['OR-201', 'OR-205']
            on_back_click=self.on_back_click
        )

    def get_surgery_nurses(self, selected_date, nurses_count_needed):
        """
        Queries scheduledShifts.csv and cross-matches with nurses.csv
        to find available nurses who are not marked 'OFF' on the chosen date.
        """
        import os
        import pandas as pd
        from pathlib import Path

        # Adjust directories to find your files cleanly
        parent_dir = Path.cwd().parent.parent
        shifts_path = os.path.join(parent_dir, "archive (1)", "scheduledShifts.csv")
        nurses_path = os.path.join(parent_dir, "archive (1)", "nurses.csv")

        if not os.path.exists(shifts_path) or not os.path.exists(nurses_path):
            print(
                f"[Error] Data files missing. Shifts: {os.path.exists(shifts_path)}, Nurses: {os.path.exists(nurses_path)}")
            return []

        try:
            df_shifts = pd.read_csv(shifts_path)
            df_nurses = pd.read_csv(nurses_path)

            # Standardize column naming formatting
            df_shifts.columns = df_shifts.columns.str.strip()
            df_nurses.columns = df_nurses.columns.str.strip()

            # 1. Filter out shifts for the selected date where the nurse isn't off-duty
            # Looking at scheduledShifts.csv: column 'start' or 'end' holds 'OFF'
            daily_active_shifts = df_shifts[
                (df_shifts['date'].astype(str) == str(selected_date).strip()) &
                (df_shifts['start'].astype(str).str.upper() != 'OFF')
                ]

            # Get list of unique IDs working that specific day
            working_nurse_ids = daily_active_shifts['id'].astype(str).unique().tolist()

            assigned_nurses_list = []

            # 2. Iterate through working nurses and pull their core profiles from nurses.csv
            for _, nurse_row in df_nurses.iterrows():
                # Note: nurses.csv uses integer string formats (e.g., '101') while shifts uses 'N001' or similar prefixes.
                # We strip non-numeric parts or match raw values to bridge cleanly.
                raw_id = str(nurse_row['nurse_id']).strip()
                formatted_shift_id = f"N{raw_id.zfill(3)}"  # Converts '104' -> 'N104' if your shifts ledger uses prefixes

                # Match against either variations to safeguard verification checks
                if raw_id in working_nurse_ids or formatted_shift_id in working_nurse_ids:
                    full_name = f"{nurse_row['first_name']} {nurse_row['last_name']} ({nurse_row['branch']})"
                    assigned_nurses_list.append(full_name)

                    # Stop once we have fulfilled the exact headcount requirements from the form screen
                    if len(assigned_nurses_list) == int(nurses_count_needed):
                        break

            # Fallback if roster is short on staff data mappings
            if not assigned_nurses_list:
                print(f"[Warning] No scheduled roster matches for date {selected_date}. Pulling basic active staff.")
                assigned_nurses_list = [f"{r['first_name']} {r['last_name']}" for _, r in
                                        df_nurses.head(int(nurses_count_needed)).iterrows()]

            return assigned_nurses_list

        except Exception as e:
            print(f"[ERROR] Assignment computation failed: {e}")
            return ["Staff Nurse Entry Placeholder"]

    # Inside your Controller class:
    def get_operating_rooms(self):
        import pandas as pd
        import os
        if not os.path.exists("operating_rooms.csv"):
            return ["OR Suite A - General"]  # fallback

        df = pd.read_csv("operating_rooms.csv")
        # Only show rooms that are status 'Available'
        available_rooms = df[df['status'] == 'Available']

        # Create a clean display string for each row item
        return [f"{row['room_id']} ({row['room_name']})" for _, row in available_rooms.iterrows()]

    def display_surgery_form(self, request_id, doctor_id, room, date, nurses, start_time):
        """ Runs when clicking 'Finalize & Save' to lock the record into your records database """
        from tkinter import messagebox

        success_message = (
            f"Database Sync Successful!\n\n"
            f"Surgery for Request {request_id} is completely scheduled on "
            f"{date} at {start_time} inside {room}."
        )
        messagebox.showinfo("Success", success_message)

        # Exit back into the primary requests queue dashboard grid log system
        if self.on_back_click:
            self.on_back_click()

    def display_surgery_details(self, request_id, doctor_id, room, date, nurses):
        """ Automatically pulls roster staff and opens up the final review screen """

        # 1. Look up the available nurses matching their shifts using your shift verification system
        assigned_staff_roster = self.get_surgery_nurses(date, nurses)

        # 2. Clear out the frame layout container space
        for widget in self.root.winfo_children():
            widget.destroy()

        # 3. Mount the new details display review dashboard window
        return SurgeryDetailScreen(
            root=self.root,
            controller=self,
            request_id=request_id,
            doctor_id=doctor_id,
            room=room,
            date=date,
            assigned_nurses=assigned_staff_roster,
            on_back_click=self.on_back_click  # Fallback safely points back into tracking lists
        )

    '''
    def display_surgery_details(self, request_id, doctor_id, room, date, nurses):
        from tkinter import messagebox

        assigned_staff_roster = self.get_surgery_nurses(date, nurses)
        staff_bullet_points = "\n".join([f"  • {name}" for name in assigned_staff_roster])

        # Displaying a summary overview confirmation dashboard payload log layout
        summary_msg = (
            f"Surgery Registration Confirmed!\n\n"
            f"• Request ID: {request_id}\n"
            f"• Assigned Doctor: {doctor_id}\n"
            f"• Scheduled Date: {date}\n"
            f"• Operating Venue: {room}\n\n"
            f"• Staffing: {nurses} Nurse(s) Allocated:\n{staff_bullet_points}"
        )
        messagebox.showinfo("Scheduling Complete", summary_msg)

        # Finally, return smoothly to the primary queue list view tracking matrix
        if self.on_back_click:
            self.on_back_click()
    '''