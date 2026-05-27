from shiftRegScreen import ShiftRegScreen
from readerHandlers import HospitalStaffReader
from readerHandlers import ShiftReader
from messageScreens import ShiftAvailabilityFailureScreen, ShiftBoundariesFailureScreen, SuccessRegistrationShiftScreen
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import time
from data_paths import data_path

class ShiftFormController:
    def __init__(self, root, input_data, main_app):
        self.root = root
        self.input_data = input_data 
        self.parent_controller = main_app
        self.current_controller = None
        self.current_screen = None

        self.name = input_data[0]
        self.surname = input_data[1]
        self.role = input_data[2]
        self.id = input_data[3]
        self.email = input_data[4] if len(input_data) > 4 else ""

        self.date = ""
        self.type_shift = ""
        self.time_begin = ""
        self.time_end = ""
        self.status = "Pending"

        self.boundaries = { 
            "Morning": {"start": "06:00", "end": "14:00"}, 
            "Afternoon": {"start": "14:00", "end": "22:00"}, 
            "Night": {"start": "22:00", "end": "06:00"}
        }

        self.displayShiftRegistrationScreen()

    def displayShiftRegistrationScreen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.current_screen = ShiftRegScreen(self.root, self.id, self.name, self.surname, self.role, self)
        self.root.update_idletasks()

    def getForm(self, data):
        self.date = data.get("date")
        self.type_shift = data.get("type")
        self.time_begin = data.get("begin")
        self.time_end = data.get("end")
        self.checkCompletnessOfForm()

    def checkCompletnessOfForm(self):
        fields = [self.date, self.type_shift, self.time_begin, self.time_end]

        if any(not str(field).strip() for field in fields):
            messagebox.showwarning("Warning!", "Please fill in all the fields of the form.")
            return

        if not self.checkWorkShiftBoundaries() or not self.checkDate():
            time.sleep(1)
            self.displaySearchScreen()
            return

        if self.checkAvailability():
            create_shift = ShiftReader(data_path("uc7_scheduledShifts.csv"))
            create_shift.save_shift(self.id, self.name, self.surname, self.date, self.time_begin, self.time_end)
            SuccessRegistrationShiftScreen()            
            time.sleep(1)
            self.displaySearchScreen()
        return 

    def checkAvailability(self):
        hospStaff = HospitalStaffReader()
        existing_shifts = hospStaff.find_Shifts(self.id)
        shifts_today = []

        if existing_shifts: 
            for shift in existing_shifts:
                shift_date = shift.get("date")
                shift_time_begin = shift.get("begin","")
                shift_time_end = shift.get("end","")


                if shift_date == self.date:
                    shifts_today.append(self.id)
                  
                    #Έλεγχος για ρεπό
                    if  shift_time_begin == "OFF" or shift_time_end == "OFF":
                        ShiftAvailabilityFailureScreen("The Staff member has declared leave.")
                        return False
                        continue

                    #Έλεγχος για πάνω από 1 Βάρδιες
                    if len(shifts_today) >= 1:
                        ShiftAvailabilityFailureScreen("The Staff Member already has two Shifts the same day.")
                        return False

                    #Έλεγχος για ακριβώς την ίδια Βάρδια
                    if (shift_time_begin == self.time_begin and shift_time_end == self.time_end):
                        ShiftAvailabilityFailureScreen("This shift is already registered.")
                        return False

                    #Έλεγχος για επικάλυψη άλλης Βάρδιας
                    if self.time_begin < shift_time_end and self.time_end > shift_time_begin:
                        ShiftAvailabilityFailureScreen("Conflict detected: Time overlap with an existing shift.")
                        return False
        return True


    def checkWorkShiftBoundaries(self):
        if self.type_shift in self.boundaries:
            expected = self.boundaries[self.type_shift]
            if self.time_begin != expected["start"]:
                ShiftBoundariesFailureScreen(f"Unexpected start time for {self.type_shift} shift. Expected {expected['start']}.")
                return False

            if self.time_begin == self.time_end:
                ShiftBoundariesFailureScreen( "Invalid Working hours. Cannot insert 0 or 24 hours of Shift")
                return False


        try:
            format_str = "%H:%M"
            start = datetime.strptime(self.time_begin, format_str)
            end = datetime.strptime(self.time_end, format_str)
            
            if end < start:
                shift_duration = (end - start).total_seconds() / 3600 + 24
            else:
                shift_duration = (end - start).total_seconds() / 3600

            #Έλεγχος για τύρηση εργασίας λιγότερο των 8 ωρών/μέρα
            if shift_duration > 8:
                messagebox.showerror("Warning!", "The duration of the shift cannot exceed 11 hours.")
                return False
            return True

        except ValueError:
            messagebox.showerror("Error!", "Invalid time format.\nTry again...")
            return False

    def checkDate(self):
        date_str = str(self.date).strip()
        
        try:
            format_str = "%Y-%m-%d" 
            input_date = datetime.strptime(date_str, format_str)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            #Έλεγχος για παρελθοντικές ημερομηνίες
            if input_date <= today:
                messagebox.showwarning("Warning!", "The date must be in the future.")
                return False
            return True

        except ValueError:
            messagebox.showerror("Error!","Invalid date format.\nTry again...")
            return False


    def displaySearchScreen(self):
        for widget in self.root.winfo_children():
                widget.destroy()

        from memberSearchController import MemberSearchController
        new_search_app = MemberSearchController(self.root)
        new_search_app.displaySearchScreen()

