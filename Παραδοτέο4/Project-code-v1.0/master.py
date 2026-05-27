from __future__ import annotations
import os
import ctypes
import sys
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__))) # Change the working directory to the script's directory

from MenuControllers.login import LoginFrame
from MenuControllers.patient_dashboard import PatientPortalFrame
from MenuControllers.doctor_page import DoctorPortalFrame
from MenuControllers.pharmacist_page import PharmacistPortalFrame
from MenuControllers.inventory_manager_page import InventoryManagerPortalFrame
from MenuControllers.hr_manager_page import HRManagerPortalFrame
from MenuControllers.secretary_page import SecretaryPortalFrame
import tkinter as tk

APP_BACKGROUND = "#F7F7F5"
CARD_BACKGROUND = "#FFFFFF"
CARD_BORDER = "#D7D8DB"
TEXT_PRIMARY = "#2A2B2E"
TEXT_SECONDARY = "#7A7D82"
INPUT_BORDER = "#D9D9DE"
BUTTON_BACKGROUND = "#F2F2F2"
BUTTON_ACTIVE = "#E5E5E5"


# Icon for Windows taskbar grouping
def set_windows_taskbar_app_id():
    if sys.platform != "win32":
        return

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("vitalink.hospital.system")
    except Exception:
        pass


class HospitalMaster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1365x900")
        self.configure(bg=APP_BACKGROUND)
        self._set_window_icon()

        # The master container
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        self.current_frame = None
        self.current_user_name = "User"
        self.current_patient_id = None
        self.show_login(user_name="User")


    # το grabage collertor του tkinter καθαριζει τις φωτογραφιες αν δεν κραταμε αναφορα σε αυτες,
    # με αποτελεσμα να μην εμφανιζονται τα εικονιδια
    def _set_window_icon(self):
        base_dir = Path(__file__).resolve().parent
        icon_paths = [
            base_dir / "Data" / "icon.png",
            base_dir.parent / "icon.png",
            base_dir / "Data" / "app_icon.png",
        ]

        for icon_path in icon_paths:
            if not icon_path.exists():
                continue

            try:
                self.app_icon = tk.PhotoImage(file=str(icon_path))
                self.iconphoto(True, self.app_icon)
                return
            except Exception as error:
                print(f"Could not load window icon from {icon_path}: {error}")

        print("Could not load window icon: no icon file was found.")

    def show_login(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(LoginFrame)

    def show_patient_portal(self, user_name, patient_id=None):
        self.current_user_name = user_name
        self.current_patient_id = patient_id
        self._switch_frame(PatientPortalFrame)

    def show_doctor_portal(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(DoctorPortalFrame)

    def show_pharmacist_portal(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(PharmacistPortalFrame)

    def show_inventory_manager_portal(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(InventoryManagerPortalFrame)

    def show_hr_portal(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(HRManagerPortalFrame)

    def show_secretary_portal(self, user_name):
        self.current_user_name = user_name
        self.current_patient_id = None
        self._switch_frame(SecretaryPortalFrame)

    def _switch_frame(self, frame_class):
        new_frame = frame_class(self.main_container, self)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    set_windows_taskbar_app_id()
    app = HospitalMaster()
    app.mainloop()
