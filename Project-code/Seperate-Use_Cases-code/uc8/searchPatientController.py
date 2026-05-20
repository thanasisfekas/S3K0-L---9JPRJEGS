from patientSearchScreen import PatientSearchScreen
from patientDetailsScreen import PatientDetailsScreen
from MenuControllers.Reader.readerHandlers import PatientReader
from prescriptionController import PrescriptionController
from tkinter import messagebox
import tkinter as tk

class SearchPatientController:
    def __init__(self, root):
        self.root = root
        self.current_screen = None
        self.input_data = {}
        self.current_controller = None
        self.id = ""
        self.first_name = ""
        self.last_name = ""

    def displaySearchScreen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_screen = PatientSearchScreen(self.root, controller=self)

    def searchPatient(self, data):
        if not (data.get('id') and data.get('name')):
            messagebox.showwarning("Warning!", "Enter the Required information.")
            return None

        print(data)

        if self.checkInput(data):
            self.id = data['id']
            self.first_name, self.last_name = ([p for p in data.get('name', '').split() if len(p) >= 2] + ["", ""])[:2]

            patient_inst = PatientReader("patients.csv")
            print(data)
            results = patient_inst.find_patient(self.id, self.first_name, self.last_name)

            if not results:
                messagebox.showinfo("Error!", "No patient found with this ID.\n Try again...")
                return None

            print(results)
            self.displayPatientDetails(results)
            return results

        else:
            messagebox.showinfo("Warning, wrong Format!", "Re-enter the required data with the right format.\n Try again...")
            return None

   
    def checkInput(self, data):
        id_str = str(data['id']).strip()

        if len(id_str) != 4 :
            print("Triggered_id")
            return False

        name_parts = data['name'].strip().split()
        if len(name_parts) < 2:
            print("Triggered_name1")
            return False
            
        for part in name_parts:
            if not part.isalpha():
                print("Triggered_name2")
                return False

        return True

    def displayPatientDetails(self,details):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_screen = PatientDetailsScreen(self.root, details, self)

    def prescriptionAdministration(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_controller = PrescriptionController(self.root, self, self.id)
        

if __name__ == "__main__":
    root = tk.Tk()
    controller = SearchPatientController(root)
    controller.displaySearchScreen()
    root.mainloop()
