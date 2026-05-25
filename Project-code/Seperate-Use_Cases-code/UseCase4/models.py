
import sys
import os
import csv
import pandas as pd
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MenuControllers.Reader.readerHandlers import PatientReader
from data_paths import data_path

class PatientHandler:
    def __init__(self):
        self.patients = pd.DataFrame({"Patients": [PatientReader(data_path("patients.csv")).data]})

    def getAvailablePatients(self):
        return self.patients

    def retreivePatientDetails(self, patient):
        if (re.match(r"^P[0-9]+",patient.strip())):
            patients =self.patients.iloc[0,0] 
            item_info = patients[patients["patient_id"] == patient.strip()]
            return  item_info if not item_info.empty else None 

    def savePatient(self,patient):
        fields = ["patient_id","first_name","last_name","gender","date_of_birth","contact_number","address","registration_date","insurance_provider","insurance_number","email","password"]

        with open(data_path("patients.csv") , 'r' , newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row["patient_id"]
            new_id = f"P{int(id.lstrip('P')) + 1:03d}"

        with open(data_path("patients.csv") , 'a' , newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writerow({"patient_id" : new_id} | patient)


    def checkPatientStatus(self,patient):
        found = False
        with open(data_path("hospitalizations.csv") ,'r',newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(patient.iloc[0,0]) == row["patient_id"] and row["status"] == "Admitted" and not found: 
                    return True
                else:
                    return False
