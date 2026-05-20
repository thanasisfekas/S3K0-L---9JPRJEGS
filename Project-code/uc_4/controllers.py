
import sys
import os
import csv
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from screens import PatientAdmissionReqScreen,PatientSearchScreen,TransferPatientScreen,PatientRegScreen

from MenuControllers.Reader.readerHandlers import WardReader
from models import Patient

class PatientAdmissReqController:
    def __init__(self,parent,patient):
        self.parent =parent
        self.patient = patient
        self.patientAdmReqScrn = PatientAdmissionReqScreen(self.parent,self.patient,self)

    # missing doctor 
    def createLabTestReq(self):
        # self.labReqReader = LabTestRequestReader("../Seperate-Use__Cases-code/uc5/lab_test_requests.csv")
        # self.labReqReader.submitLabtest()
        print("create and subm lab test req")

    # def finalizePatientForm(self):
    #     self.patientInfoScreen = PatientInfoScreen(self)
    #     messagebox.showinfo("","completed admission")


class TransferPatientController:
    def __init__(self,patient_data,parent):
        self.patient_data = patient_data
        self.parent = parent
        self.wardReader = WardReader("wards.csv")
        self.wards = self.wardReader.data
        self.transferScreen = TransferPatientScreen(self.parent,self)
        self.transferScreen.displayPatientStatus("Patient has already treatment")
        self.transferScreen.displayHospitalWings(self.wards)
        
    def write_tranfer(self,patient,ward):
        print("writing to hospitilization")
        fields = ["hospitalization_id","patient_id","status","ward","admission_date","discharge_date","attending_doctor_id"]
        with open("hospitalizations.csv" , 'r' , newline='') as file , open('temp.csv' , 'w') as writeFile:
            writer = csv.DictWriter(writeFile,fieldnames=fields)
            reader = csv.DictReader(file)
            writer.writeheader()
            for row in reader:
                if row["patient_id"] == patient["patient_id"].values[0] and row["status"] == 'Admitted':
                    row["ward"] = ward[1]
                    writer.writerow(row)
                else:
                    writer.writerow(row)
            os.replace('temp.csv','hospitalizations.csv')
        
        messagebox.showinfo("","treatment trasnfer completed")

class PatientSearchController:
    def __init__(self,parent):
        self.parent = parent
        self.patient = Patient()
        self.available_patient = self.patient.getAvailablePatients()
        self.searchScreen = PatientSearchScreen(parent,self)
        self.searchScreen.display()
        self.searchScreen.displayPatientList()
    #     self.SearchResultScreen = SearchResultScreen(self.parent,self)
    #     self.OrderController = OrderController(self.parent)

    def setPatient(self):
        self.searched_patient = self.searchScreen.entry_search.get()
        self.patient_res = self.patient.retreivePatientDetails(self.searched_patient)

        if self.patient_res is None:
            messagebox.showinfo("","Item not Found")
            self.searchScreen.pack_forget()
            self.patientRegController = PatientRegController(self.parent,self)
        else :
            messagebox.showinfo("","Item Found")
            if self.patient.checkPatientStatus(self.patient_res):
                self.searchScreen.pack_forget()
                self.transfer_Patient_Controller = TransferPatientController(self.patient_res,self.parent)
            else:
                self.searchScreen.pack_forget()
                self.patientAdmissionReqController = PatientAdmissReqController(self.parent,self.patient_res)

class PatientRegController:
    def __init__(self,parent,controller:PatientSearchController):
        self.parent = parent
        self.search_controller = controller
        self.patientRegScreen = PatientRegScreen(self.parent , self)
        self.patientRegScreen.displayPatientRegForm()

    def getPatientRegFormDetails(self):
        self.patient = Patient().savePatient(self.patientRegScreen.formDetails)



class DoctorMainMenuController:
    def __init__(self,parent):
        self.searchController = PatientSearchController(parent)
        