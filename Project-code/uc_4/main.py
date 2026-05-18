import pandas as pd
import re
import customtkinter as ctk
import sys
import os
from CTkTable import *
from tkinter import messagebox
from tkcalendar import Calendar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MenuControllers.Reader.readerHandlers import WardReader
import csv

from MenuControllers.Reader.readerHandlers import PatientReader

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
TEXT_MUTE = "#64748B"

class TransferPatientScreen:
    def __init__(self,parent):
        pass

    def displayPatientStatus(self,msg):
        messagebox.showinfo("",msg)

class TransferPatientController:
    def __init__(self,patient_data):
        self.patient_data = patient_data
        self.wardReader = WardReader("wards.csv")
        TransferPatientScreen().displayPatientStatus("Patient has active treatment")
        self.wards = self.wardReader.data

class Patient:
    def __init__(self):
        self.patients = pd.DataFrame({"Patients": [PatientReader("../Data/patients.csv").data]})

    def getAvailablePatients(self):
        return self.patients

    def retreivePatientDetails(self, patient):
        if (re.match(r"^P[0-9]+",patient.strip())):
            patients =self.patients.iloc[0,0] 
            item_info = patients[patients["patient_id"] == patient.strip()]
            return  item_info if not item_info.empty else None 


    def savePatient(self,patient):
        fields = ["patient_id","first_name","last_name","gender","date_of_birth","contact_number","address","registration_date","insurance_provider","insurance_number","email","password"]

        with open("../Data/patients.csv" , 'r' , newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row["patient_id"]
            new_id = f"P{int(id.lstrip('P')) + 1:03d}"

        with open("../Data/patients.csv" , 'a' , newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({"patient_id" : new_id} | patient)


    def checkPatientStatus(self,patient):
        with open("hospitalizations.csv" ,'r',newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(patient.iloc[0,0]) == row["patient_id"] and row["status"] == "Admitted": 
                   self.tranferPatientController = TransferPatientController(patient)
                else:
                    print("no treatment at the moment")

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
            self.patient.checkPatientStatus(self.patient_res)


class PatientRegController:
    def __init__(self,parent,controller:PatientSearchController):
        self.parent = parent
        self.search_controller = controller
        self.patientRegScreen = PatientRegScreen(self.parent , self)
        self.patientRegScreen.displayPatientRegForm()

    def getPatientRegFormDetails(self):
        self.patient = Patient().savePatient(self.patientRegScreen.formDetails)

class PatientRegScreen(ctk.CTkFrame):
    def __init__(self,parent,controller:PatientRegController):
        super().__init__(parent)
        self.configure(fg_color=BG_COLOR)
        self.controller = controller
        ctk.set_appearance_mode("Light") 
        self.lbl_form_title = ctk.CTkLabel(self, text="Patient Registration Form", font=ctk.CTkFont(size=22, weight="bold"))

        self.frame = ctk.CTkFrame(self,fg_color="transparent")

        self.firstNameEntry = ctk.CTkEntry(self.frame)
        self.firstNameLabel = ctk.CTkLabel(self.frame, text="FIRST NAME")

        self.lastNameEntry = ctk.CTkEntry(self.frame)
        self.lastNameLabel = ctk.CTkLabel(self.frame, text="LAST NAME")

        self.genderMenu = ctk.CTkComboBox(self.frame, values=["Male", "Female"], state="readonly")
        self.genderLabel = ctk.CTkLabel(self.frame, text="GENDER")

        self.calendarLabel = ctk.CTkLabel(self.frame, text="DATE OF BIRTH")        
        self.calendar = Calendar(self.frame, selectmode = 'day',year = 2022, month = 5,day = 22,date_pattern='yyyy-mm-dd')
        
        self.numberEntry = ctk.CTkEntry(self.frame)
        self.numberLabel = ctk.CTkLabel(self.frame, text="CONTACT NUMBER")

        self.addressEntry = ctk.CTkEntry(self.frame)
        self.addressLabel = ctk.CTkLabel(self.frame, text="ADDRESS")

        self.registration_label = ctk.CTkLabel(self.frame, text="INSURANCE REGISTRATION DATE")
        self.registration_calendar = Calendar(self.frame, selectmode = 'day',year = 2022, month = 5,day = 22,date_pattern='yyyy-mm-dd') 
        
        self.insuranceProviderEntry = ctk.CTkEntry(self.frame)
        self.insuranceProviderLabel = ctk.CTkLabel(self.frame, text="INSURANCE PROVIDER")

        self.insuranceNumberEntry = ctk.CTkEntry(self.frame)
        self.insuranceNumberLabel = ctk.CTkLabel(self.frame, text="INSURANCE NUMBER")
        
        self.emailEntry = ctk.CTkEntry(self.frame)
        self.emailLabel = ctk.CTkLabel(self.frame, text="EMAIL")

        self.passwordEntry = ctk.CTkEntry(self.frame)
        self.passwordLabel = ctk.CTkLabel(self.frame, text="PASSWORD")

        self.subm_patient_btn = ctk.CTkButton(self.frame, text="Submit Patient", width=150, height=60,command=self.on_click_event)

    def displayPatientRegForm(self):
        self.lbl_form_title.pack(pady=20)
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.firstNameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.firstNameEntry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        self.firstNameEntry.configure(placeholder_text="First Name")

        self.lastNameLabel.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.lastNameEntry.grid(row=0, column=3, padx=20, pady=10, sticky="ew")
        self.lastNameEntry.configure(placeholder_text="Last Name")

        self.genderLabel.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.genderMenu.grid(row=0, column=5, padx=20, pady=10, sticky="ew")

        self.numberLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.numberEntry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.numberEntry.configure(placeholder_text="Contact Number")

        self.emailLabel.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.emailEntry.grid(row=1, column=3, padx=20, pady=10, sticky="ew")
        self.emailEntry.configure(placeholder_text="Email Address")

        self.addressLabel.grid(row=1, column=4, padx=10, pady=10, sticky="w")
        self.addressEntry.grid(row=1, column=5, padx=20, pady=10, sticky="ew")
        self.addressEntry.configure(placeholder_text="Street Address")

        self.passwordLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.passwordEntry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        self.passwordEntry.configure(placeholder_text="Password", show="*")

        self.insuranceProviderLabel.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.insuranceProviderEntry.grid(row=2, column=3, padx=20, pady=10, sticky="ew")
        self.insuranceProviderEntry.configure(placeholder_text="Insurance Provider")

        self.insuranceNumberLabel.grid(row=2, column=4, padx=10, pady=10, sticky="w")
        self.insuranceNumberEntry.grid(row=2, column=5, padx=20, pady=10, sticky="ew")
        self.insuranceNumberEntry.configure(placeholder_text="Insurance Policy #")

        self.calendarLabel.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        self.calendar.grid(row=3, column=1,padx=10, pady=10, sticky="w")

        self.registration_label.grid(row=3, column=4, padx=10, pady=10, sticky="nw")
        self.registration_calendar.grid(row=3, column=5, padx=10, pady=10, sticky="w")

        self.subm_patient_btn.grid(row=5, column=2,columnspan=2, padx=20, pady=10)
        
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)
        self.frame.grid_columnconfigure(5,weight=1)
        
    def on_click_event(self):
        self.formDetails = {
            "first_name":self.firstNameEntry.get(),
            "last_name":self.lastNameEntry.get(),
            "gender":self.genderMenu.get(),
            "date_of_birth":self.calendar.get_date(),
            "contact_number":self.numberEntry.get(),
            "address":self.addressEntry.get(),
            "registration_date":self.registration_calendar.get_date(),
            "insurance_provider":self.insuranceProviderEntry.get(),
            "insurance_number":self.insuranceNumberEntry.get(),
            "email":self.emailEntry.get(),
            "password":self.passwordEntry.get()
        }
        self.controller.getPatientRegFormDetails()
        self.pack_forget()
        self.controller.search_controller.searchScreen.display()
        self.controller.search_controller.searchScreen.displayPatientList()


class PatientSearchScreen(ctk.CTkFrame):
    def __init__(self,parent,search_controller : PatientSearchController ):
        super().__init__(parent)
        self.search_controller = search_controller
        self.parent = parent
        self.configure(fg_color=BG_COLOR)
        self.lbl_title = ctk.CTkLabel(self, text="Search Patient", font=ctk.CTkFont(size=24, weight="bold"),fg_color="#dbdbdb",corner_radius=10)
        self.search_container = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_search = ctk.CTkEntry(self.search_container, placeholder_text="Enter Patient Id",height=45,width=400)

        self.results = ctk.CTkScrollableFrame(self, label_text="Available Items",fg_color=CARD_WHITE,height=300)
        self.search_btn = ctk.CTkButton(self.search_container, text="Search", width=100, height=45,command=self.search_controller.setPatient)

    def display(self):
        self.pack(fill="both", expand=True)
        self.lbl_title.pack(pady=(40, 20))
        self.search_container.pack(fill="x", padx=100)
        self.entry_search.pack(side="left", padx=(0, 10), expand=True, fill="x")
        self.results.pack(fill="both", expand=True, padx=100, pady=20)
        self.search_btn.pack(side="right")

    def displayPatientList(self):
        for child in self.results.winfo_children():
            child.destroy()
        
        patients = self.search_controller.available_patient["Patients"].loc[0]

        med_lb = ctk.CTkLabel(self.results, text="Available Medicines", font=ctk.CTkFont(size=15, weight="bold"),fg_color="#dbdbdb",corner_radius=10)
        med_lb.pack(pady=(40, 20))
        table_data = [["ID", "First Name", "Last Name", "Gender", "Date of birth", "Number", "Address" , "Registration", "Insurance Number" , "Email"]]
        for _, row in patients.iterrows():
            table_data.append([
                row['patient_id'], 
                row['first_name'], 
                row['last_name'], 
                row['gender'], 
                row['date_of_birth'], 
                row['contact_number'],
                row['address'],
                row['registration_date'],
                row['insurance_number'],
                row['email']
            ])

        table = CTkTable(master=self.results, row=len(table_data), column=10, values=table_data)
        table.pack(expand=True, fill="both", padx=20, pady=20)

class DoctorMainMenuController:
    def __init__(self,parent):
        self.searchController = PatientSearchController(parent)


        
if __name__=="__main__":
    app = ctk.CTk()
    app.geometry("1550x750")
    search = DoctorMainMenuController(app)
    app.mainloop()