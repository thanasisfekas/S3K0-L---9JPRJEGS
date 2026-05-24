import sys
import os
import csv
from datetime import datetime
import re
from tkinter import messagebox
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from screens import PatientAdmissionReqScreen,PatientSearchScreen,TransferPatientScreen,PatientRegScreen,AcceptScreen,PatientInfoScreen

from MenuControllers.Reader.readerHandlers import WardReader,LabTestRequestReader,PatientFolderReader,DocReader,PatientAdmissionReader
from models import PatientHandler

class PatientAdmissReqController:
    def __init__(self,parent,patient):
        self.parent =parent
        self.patient = patient
        self.patientAdmReqScrn = PatientAdmissionReqScreen(self.parent,self.patient,self)

    # missing doctor 
    def createLabTestReq(self,entries):
        # fixed doctor id. with login pass here the doctor id
        # update here
        self.doc = 'D007'
        self.labReqReader = LabTestRequestReader("../Seperate-Use_Cases-code/uc5/lab_test_requests.csv")
        target =self.patient["patient_id"].iloc[0]
        folders = PatientFolderReader("../Seperate-Use_Cases-code/uc5/patient_medical_folders.csv").data
        self.acceptScreen = AcceptScreen( "Submit Lab Test Request")
        res = self.acceptScreen.displayConfirmMsg()

        if res:
            self.patientInfoScreen = PatientInfoScreen(self.parent,self,self.patient)
            self.patientInfoScreen.displayPatientAdmForm()
            self.labReqReader.submitLabtest({
                                            "request_id": self.labReqReader.generate_req_id(),
                                            "patient_id":target ,
                                            "folder_id":folders[folders["patient_id"]== target]["folder_id"].iloc[0],
                                            "doctor_id":self.doc, 
                                            "status": 'Pending',
                                            "request_date": datetime.now().strftime("%Y-%-m-%-d")
            })
        else:
            messagebox.showwarning("","No Lab Test submitted")

    def checkFormInfo(self):
        doc_validation = self.validate_doc(self.patientInfoScreen.doc_entry.get().strip())
        reason_validation = self.validate_reason(self.patientInfoScreen.reason_text.get("1.0","end-1c").strip())
        if doc_validation and reason_validation:
            return True
        else:
            False

    # helper functions for checking form integrity
    def validate_doc(self,doc):
        if re.match(r"^D[0-9]+$",doc) and doc in DocReader("../Data/doctors.csv").getDoctorId().values:
            return True
        else:
            return False
        
    def validate_reason(self,reason):
        if not reason:
            return False
        else:
            return True
        
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
        
        messagebox.showinfo("","Trasnfer completed")

class PatientSearchController:
    def __init__(self,parent):
        self.parent = parent
        self.patient = PatientHandler()
        self.available_patient = self.patient.getAvailablePatients()
        self.searchScreen = PatientSearchScreen(parent,self)
        self.searchScreen.display()
        self.searchScreen.displayPatientList()

    def setPatient(self):
        self.searched_patient = self.searchScreen.entry_search.get()
        self.patient_res = self.patient.retreivePatientDetails(self.searched_patient)

        #alt 2 check if search result is None
        if self.patient_res is None:
            #alternative flow registration 
            messagebox.showinfo("","Patient not Found")
            self.searchScreen.pack_forget()
            self.patientRegController = PatientRegController(self.parent,self)
        else :
            # main flow
            messagebox.showinfo("","Patient Found")
            # alternative 1
            if self.patient.checkPatientStatus(self.patient_res):
                # alternative flow tranfer patient
                self.searchScreen.pack_forget()
                self.transfer_Patient_Controller = TransferPatientController(self.patient_res,self.parent)
            else:
                # main flow
                self.searchScreen.pack_forget()
                self.patientAdmissionReqController = PatientAdmissReqController(self.parent,self.patient_res)

class PatientRegController:
    def __init__(self,parent,controller):
        self.parent = parent
        self.search_controller = controller
        self.patientRegScreen = PatientRegScreen(self.parent , self)
        self.patientRegScreen.displayPatientRegForm()

    def getPatientRegFormDetails(self):
        self.patient = PatientHandler().savePatient(self.patientRegScreen.formDetails)

class DoctorMainMenuController:
    def __init__(self,parent):
        self.searchController = PatientSearchController(parent)
        