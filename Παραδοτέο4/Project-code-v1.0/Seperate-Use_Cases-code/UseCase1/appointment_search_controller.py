from pathlib import Path
import pandas as pd

from MenuControllers.Reader.readerHandlers import (
    DocReader,
    DoctorSpecialtyReader,
    DoctorAppointmentTimeSlotsReader
)

from .search_appointment_screen import SearchAppointmentScreen
from .specialty_select_screen import SpecialtySelectScreen
from .doctor_select_screen import DoctorSelectScreen
from .time_select_screen import TimeSelectScreen
from .no_available_slots_screen import NoAvailableSlotsScreen
from .appointment_booking_controller import AppointmentBookingController


class AppointmentSearchController:
    def __init__(self, patient_id, root, back_command=None):
        self.patient_id = patient_id
        self.root = root
        self.back_command = back_command

        self.selected_date = None
        self.selected_specialty = None
        self.selected_doctor = None
        self.selected_time = None

        self.booking_controller = None
        self.timeAvailableFlag = False

    def displaySearchAppointmentScreen(self):
        self._clear_screen()
        self.current_screen = SearchAppointmentScreen(self.root, on_submit=self.setDate, back_command=self.back_command)
        return self.current_screen

    def setDate(self, date):
        try:
            pd.to_datetime(date)
        except:
            self.current_screen.showError("Invalid date")
            return
        self.selected_date = date
        self.displaySpecialtyScreen()


    def getDoctorSpecialties(self):
        BASE_DIR = Path(__file__).resolve().parents[2]
        csv_path = BASE_DIR / "Data" / "doctor_specialties.csv"
        reader = DoctorSpecialtyReader(str(csv_path))
        specialties = reader.getSpecialtyName()
        return specialties.dropna().sort_values().tolist()

    def displaySpecialtyScreen(self):
        self._clear_screen()
        specialties = self.getDoctorSpecialties()
        self.current_screen = SpecialtySelectScreen(self.root, specialties, selected_date=self.selected_date, on_select=self.setSpecialty, back_command=self.displaySearchAppointmentScreen)
        return self.current_screen

    def setSpecialty(self, specialty):
        self.selected_specialty = specialty
        self.displayDoctorScreen()


    def getDoctors(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "doctors.csv"
        reader = DocReader(str(path))
        return reader.getDoctorsBySpecialty(self.selected_specialty)
    
    def displayDoctorScreen(self):
        self._clear_screen()
        doctors = self.getDoctors()
        self.current_screen = DoctorSelectScreen(self.root, doctors, selected_date=self.selected_date, selected_specialty=self.selected_specialty, on_select=self.setDoctor, back_command=self.displaySpecialtyScreen)
        return self.current_screen

    def setDoctor(self, doctor_id):
        self.selected_doctor = doctor_id
        self.timeAvailableFlag = False
        self.displayTimeScreen()

    def getSelectedDoctorName(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "doctors.csv"
        reader = DocReader(str(path))
        return reader.getDoctorFullName(self.selected_doctor)

    def getAvailableSlots(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "doctor_appointment_timeslots.csv"
        reader = DoctorAppointmentTimeSlotsReader(str(path))
        return reader.getAvailableSlots(self.selected_doctor, self.selected_date)

    def displayTimeScreen(self):
        self._clear_screen()
        slots = self.getAvailableSlots()
        if not slots:
            self.current_screen = NoAvailableSlotsScreen(self.root, on_next=self.findNextAvailableDate, back_command=self.displayDoctorScreen)
            return self.current_screen

        self.current_screen = TimeSelectScreen(self.root, slots, selected_date=self.selected_date, selected_specialty=self.selected_specialty, selected_doctor=self.getSelectedDoctorName(), on_select=self.setTime, back_command=self.displayDoctorScreen)
        return self.current_screen

    def findNextAvailableDate(self):
        current = pd.to_datetime(self.selected_date)
        for _ in range(365):
            current += pd.Timedelta(days=1)
            self.selected_date = current.strftime("%Y-%m-%d")
            if self.getAvailableSlots():
                return self.displayTimeScreen()

        self.current_screen.showError("No future appointments available.")


    def setTime(self, time):
        self.selected_time = time
        self.timeAvailableFlag = False
        self.booking_controller = AppointmentBookingController(patient_id=self.patient_id, doctor_id=self.selected_doctor, doctor_name=self.getSelectedDoctorName(), specialty=self.selected_specialty, date=self.selected_date, time=self.selected_time, root=self.root, search_controller=self)
        self.booking_controller.validateAvailability()

    def returnToTimeSelection(self):
        self.timeAvailableFlag = False
        self.displayTimeScreen()

    # helper
    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.geometry("900x600")

    controller = AppointmentSearchController(
        patient_id="P001",
        root=root
    )

    controller.displaySearchAppointmentScreen()

    root.mainloop()
