from CTkTable import *
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
from tkinter import messagebox
import customtkinter as ctk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MenuControllers.Reader.readerHandlers import PatientAdmissionReader

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
TEXT_MUTE = "#64748B"

class PatientSearchScreen(ctk.CTkFrame):
    def __init__(self,parent,search_controller):
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

    def destroy_chld(self):
        for child in self.results.winfo_children():
            child.destroy()

    def displayPatientList(self):
        self.destroy_chld()
        
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


class PatientRegScreen(ctk.CTkFrame):
    def __init__(self,parent,controller):
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

class TransferPatientScreen(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller= controller
        self.configure(fg_color=BG_COLOR)
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(fill="x", padx=100)
        self.pack(fill="both", expand=True)
        self.tranf_lb = ctk.CTkLabel(self.frame, text="Transfer Patient", font = ctk.CTkFont(size=22, weight="bold"),fg_color="#dbdbdb",corner_radius=10)
        self.tranf_lb.pack(pady=5)
        self.wards_res = ctk.CTkScrollableFrame(self.frame, label_text="Available Wards",fg_color=CARD_WHITE,height=500)
        self.wards_res.pack(fill="both", expand=True, padx=100, pady=20)

    def displayPatientStatus(self,msg):
        messagebox.showinfo("",msg)

    def displayHospitalWings(self,wards):
        for child in self.wards_res.winfo_children():
            child.destroy()

        table_data = [["ID", "Name", "Availability"]]
        for _, row in wards.iterrows():
            if row['availability'] == 'Available':
                table_data.append([
                    row['ward_id'], 
                    row['name'], 
                    row['availability']
                ])

        self.table = CTkTable(master=self.wards_res, row=len(table_data), column=3, values=table_data , command=self.on_click_event)
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

    def on_click_event(self,data):
        idx = data['row']
        if idx ==0:return
        self.controller.write_tranfer(self.controller.patient_data,self.table.get_row(idx))
    

class PatientInfoScreen(ctk.CTkFrame):
    def __init__(self,parent,controller,patient):
        super().__init__(parent)
        self.controller= controller
        self.parent= parent
        self.patient=patient
        self.createForm()

    def createForm(self):
        self.controller.patientAdmReqScrn.pack_forget()
        self.configure(fg_color=BG_COLOR)
        self.pack(fill="both", expand=True)

        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frame.pack(fill="x", padx=100)

        self.container = ctk.CTkFrame(self.frame, fg_color="transparent")
        
        self.patient_adm_lb = ctk.CTkLabel(self.frame, text="Patient Admission", font = ctk.CTkFont(size=22, weight="bold"),fg_color="#dbdbdb",corner_radius=10)

        self.container.grid_columnconfigure(1,weight=1)

        self.patient_id_lb = ctk.CTkLabel(self.container, text="Patient Id : ", font = ctk.CTkFont(size=14, weight="bold"),text_color=TEXT_MUTE,corner_radius=10)

        self.patient_id_val_lb = ctk.CTkLabel(self.container, text=f"{self.patient["patient_id"].iloc[0]}", font = ctk.CTkFont(size=12, weight="bold"),corner_radius=10)

        self.doc_id_lb = ctk.CTkLabel(self.container, text="Doctor Id : ", font = ctk.CTkFont(size=14, weight="bold"),text_color=TEXT_MUTE,corner_radius=10)

        self.doc_entry = ctk.CTkEntry(self.container, placeholder_text="Enter Doctor Id")
        # when we get the logged in doctor id
        # self.doc_entry.insert(0,logged_in_doc)

        self.reason = ctk.CTkLabel(self.container,text="Reason :" ,font = ctk.CTkFont(size=14, weight="bold"),text_color=TEXT_MUTE,corner_radius=10)

        self.reason_text = ctk.CTkTextbox(self.container,                                        width=600 ,
                                        height=100 ,
                                        fg_color=BG_COLOR ,
                                        text_color=TEXT_MUTE ,
                                        border_width=3 )

        self.status_lb = ctk.CTkLabel(self.container,text="Status :" ,font = ctk.CTkFont(size=14, weight="bold"),text_color=TEXT_MUTE,corner_radius=10)

        self.status_drop = ctk.CTkOptionMenu(self.container,values=["Admitted","Pending","Discharged"])

        self.date_ld = ctk.CTkLabel(self.container,text="Admission Date :" ,font = ctk.CTkFont(size=14, weight="bold"),text_color=TEXT_MUTE,corner_radius=10)

        self.calendar = Calendar(self.container, selectmode = 'day',year = 2022, month = 5,day = 22,date_pattern='yyyy-mm-dd')

        self.subm_btn = ctk.CTkButton(self.frame,text="Submit Admission" , font = ctk.CTkFont(size=14, weight="bold"),width=150, height=60 , corner_radius=10,command=self.on_click_event)
        
    def displayPatientAdmForm(self):
        self.patient_adm_lb.pack(anchor="center",pady=10)
        self.container.pack(fill="x",pady=10)
        self.reason_text.grid(row=2, column=1,pady=10,padx=10,sticky="ew")
        self.status_lb.grid(row=3, column=0,pady=10,padx=10,sticky="e")
        self.status_drop.grid(row=3, column=1,pady=10,padx=10,sticky="w")
        self.reason.grid(row=2, column=0,pady=10,padx=10,sticky="ne")
        self.doc_entry.grid(row=1, column=1,pady=10,padx=10,sticky="ew")
        self.doc_id_lb.grid(row=1, column=0,pady=10,padx=10,sticky="e")
        self.patient_id_val_lb.grid(row=0, column=1,pady=10,padx=10,sticky="w")
        self.patient_id_lb.grid(row=0, column=0,pady=10,padx=10,sticky="e")
        self.date_ld.grid(row=4, column=0,pady=10,padx=10,sticky="ne")
        self.calendar.grid(row=4, column=1,padx=10, pady=10, sticky="w")
        self.subm_btn.pack(anchor="center",pady=10)

    def on_click_event(self):
        if self.controller.checkFormInfo():
            self.confAdmissionScreen =AcceptScreen("Confirm Admission ? ")
            self.confAdmissionScreen.displayConfirmMsg()
            self.patientAdmissionReader = PatientAdmissionReader("./Data/patient_Admission.csv")
            self.patientAdmissionReader.submitAdmission({
                                            "admission_id": self.patientAdmissionReader.generate_adm_id(),
                                            "patient_id":self.patient["patient_id"].iloc[0],
                                            "doctor_id":self.doc_entry.get().strip(), 
                                            "reason": self.reason_text.get("1.0","end-1c").strip(),
                                            "status" : self.status_drop.get(),
                                            "admission_date": self.calendar.get_date()
            })

            MsgScreen().displayMsg("Admission Succesful")

class MsgScreen:
    def displayMsg(self,msg):
        messagebox.showinfo("",msg)

class PatientAdmissionReqScreen(ctk.CTkFrame):
    def __init__(self,parent,patient,controller):
        super().__init__(parent)
        self.parent=parent
        self.controller=controller
        self.patient=patient.iloc[0]
        self.createScreen()

    def createScreen(self):
        self.configure(fg_color=BG_COLOR)
        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.patient_adm_lb = ctk.CTkLabel(self.frame, text="Patient Admission Request", font = ctk.CTkFont(size=22, weight="bold"),fg_color="#dbdbdb",corner_radius=10)
        self.patient_adm_lb.pack(anchor="center",pady=10)
        self.pack(fill="both", expand=True)
        self.frame.pack(fill="x", padx=100)
        self.entries = {}
        
        patient_text = {"header" : "Patient Personal Info",
                        "info": [
                            ("Patient Id", self.patient["patient_id"]),
                            ("Full Name" , f"{self.patient["first_name"]}{self.patient["last_name"]}"),
                            ("Gender" , f"{self.patient["gender"]}"),
                            ("Date Of Birth" , f"{self.patient["date_of_birth"]}"),
                            ("Contact Number",f"{self.patient["contact_number"]}"),
                            ("Adress" , f"{self.patient["address"]}"),
                            ("Email" , f"{self.patient["email"]}")
                        ]
        }

        insurance_text = {"header" : "Insurance Info",
                          "info" :[
                           ("Insurance Provide ",f"{self.patient["insurance_provider"]}"),
                            ("Insurance Number" , f"{self.patient["insurance_number"]}"),
                            ("Registration Date",f"{self.patient["registration_date"]}")
                          ]
        }

        self.patient_info_frame = ctk.CTkFrame(self.frame, fg_color=CARD_WHITE,corner_radius=10)
        self.patient_info_lb = ctk.CTkLabel(self.patient_info_frame, text = patient_text["header"] ,font=ctk.CTkFont(size=10, weight="bold"))
        self.patient_info_lb.grid(row = 0 , column = 0, columnspan=2,sticky="w")
        self.patient_info_frame.pack(fill="x",pady=(0,15))

        self.displayDetails(patient_text,self.patient_info_frame)        

        self.patient_insurance_frame = ctk.CTkFrame(self.frame, fg_color=CARD_WHITE,corner_radius=10)
        self.patient_insurance_info_lb = ctk.CTkLabel(self.patient_insurance_frame, text = insurance_text["header"] ,font=ctk.CTkFont(size=10, weight="bold"))
        self.patient_insurance_info_lb.grid(row = 0 , column = 0, columnspan=2,sticky="w")
        self.patient_insurance_frame.pack(fill="x",pady=(0,15))

        self.displayDetails(insurance_text,self.patient_insurance_frame)

        self.create_req_btn = ctk.CTkButton(self.frame,text="Create Request",command=lambda : self.controller.createLabTestReq(self.entries) ,corner_radius=10)
        self.create_req_btn.pack(pady=10)

    def displayDetails(self,text,frame):
        row =1
        for idx,(lb_text,value_text) in enumerate(text["info"]):
            row += idx
            lb_title = ctk.CTkLabel(frame,text=lb_text, font=ctk.CTkFont(size=10, weight="bold"), text_color=TEXT_MUTE)
            lb_title.grid(row=row,column=0,padx=(20, 10), pady=6, sticky="w")

            lb_text = ctk.CTkLabel(frame, text=value_text, font=ctk.CTkFont(size=14, weight="normal"), text_color="#1E293B")
            lb_text.grid(row=row, column= 1, padx=(0, 30), pady=6, sticky="w")        

class AcceptScreen:
    def __init__(self,msg):
        self.msg = msg

    def displayConfirmMsg(self):
        return messagebox.askyesno("",self.msg)