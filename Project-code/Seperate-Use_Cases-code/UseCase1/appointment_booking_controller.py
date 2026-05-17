from pathlib import Path
import pandas as pd

from MenuControllers.Reader.readerHandlers import (
    AppointmentReader,
    DoctorAppointmentTimeSlotsReader
)

from .confirmation_screen import ConfirmationScreen
from .booking_completion_screen import BookingCompletionScreen


class AppointmentBookingController:
    def __init__(self, patient_id, doctor_id, doctor_name, specialty, date, time, root, search_controller):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.specialty = specialty
        self.date = date
        self.time = time
        self.root = root
        self.search_controller = search_controller

        self.slot_reserved = False
        self.appointments_path = Path(__file__).resolve().parents[2] / "Data" / "appointments.csv"


    def validateAvailability(self):
        csv_path = Path(__file__).resolve().parents[2] / "Data" / "doctor_appointment_timeslots.csv"
        df = DoctorAppointmentTimeSlotsReader(str(csv_path)).data

        slot_exists = not df[
            (df["doctor_id"] == self.doctor_id) &
            (df["available_date"] == self.date) &
            (df["available_time"] == self.time)
        ].empty

        if slot_exists:
            self._remove_timeslot()
            self.slot_reserved = True
            self.search_controller.timeAvailableFlag = True
            self.displayConfirmationScreen()

        else:
            self.search_controller.timeAvailableFlag = False
            self.search_controller.current_screen.showError(
                "This time slot is no longer available. Please select another."
            )
            self.search_controller.returnToTimeSelection()


    def displayConfirmationScreen(self):
        self._clear_screen()
        self.current_screen = ConfirmationScreen(self.root, doctor_name=self.doctor_name, specialty=self.specialty, date=self.date, time=self.time, on_confirm=self.createAppointment, on_cancel=self.cancelBooking)
        return self.current_screen

    def cancelBooking(self):
        if self.slot_reserved:
            self._restore_timeslot()
            self.slot_reserved = False

        self.search_controller.returnToTimeSelection()

    def createAppointment(self):
        reader = AppointmentReader(str(self.appointments_path))
        reader.createAppointment(self.patient_id, self.doctor_id, self.date, self.time)
        self.slot_reserved = False
        self.displayCompletionScreen()

    def _remove_timeslot(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "doctor_appointment_timeslots.csv"
        reader = DoctorAppointmentTimeSlotsReader(str(path))
        reader.removeSlot(self.doctor_id, self.date, self.time)

    def _restore_timeslot(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "doctor_appointment_timeslots.csv"
        reader = DoctorAppointmentTimeSlotsReader(str(path))
        reader.restoreSlot(self.doctor_id, self.date, self.time)


    def displayCompletionScreen(self):
        self._clear_screen()
        self.current_screen = BookingCompletionScreen(self.root, close_command=self.search_controller.displaySearchAppointmentScreen)
        return self.current_screen

    # helper
    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()