from file_reader import File_reader
import pandas as pd
import os
from data_paths import data_path

class DocReader(File_reader):
    def __init__(self, file: str)->None:
        super().__init__(file)

    def getDoctorId(self) -> pd.Series:
        return self.data.iloc[:,0]
    
    def getDoctorFirstName(self) ->pd.Series:
        return self.data.iloc[:,1]
    
    def getDoctorLastName(self) ->pd.Series:
        return self.data.iloc[:,2]
    
    def getDoctorSpecialization(self) ->pd.Series:
        return self.data.iloc[:,3]
    
    def getDoctorPhoneNuber(self) ->pd.Series:
        return self.data.iloc[:,4]
    
    def getDoctorExperience(self) ->pd.Series:
        return self.data.iloc[:,5]
    
    def getDoctorBrach(self) ->pd.Series:
        return self.data.iloc[:,6]
    
    def getDoctorEmail(self) ->pd.Series:
        return self.data.iloc[:,7]
    
    def getDoctorPassword(self) ->pd.Series:
        return self.data.iloc[:,8]

class AppointmentReader(File_reader):
    def __init__(self, file : str)->None:
        super().__init__(file)

    def getAppointmentId(self) ->pd.Series:
        return self.data.iloc[:,0]
        
    def getPatientId(self) ->pd.Series:
        return self.data.iloc[:,1]
    
    def getDoctorId(self)->pd.Series:
        return self.data.iloc[:,2]
    
    def getAppointmentDate(self)->pd.Series:
        return self.data.iloc[:,3]
    
    def getAppointmentTime(self)->pd.Series:
        return self.data.iloc[:,4]
    
    def getAppointmentReasor(self)->pd.Series:
        return self.data.iloc[:,5]
    
    def getAppointmentStatus(self)->pd.Series:
        return self.data.iloc[:,6]
    

class BillingReader(File_reader):
    def __init__(self, file : str)->None:
        super().__init__(file)

    def getBillId(self)->pd.Series:
        return self.data.iloc[:,0]
    
    def getPatientId(self)->pd.Series:
        return self.data.iloc[:,1]
    
    def getTreatmentID(self)->pd.Series:
        return self.data.iloc[:,2]
    
    def getBillDate(self)->pd.Series:
        return self.data.iloc[:,3]
    
    def getBillAmount(self)->pd.Series:
        return self.data.iloc[:,4]
    
    def getBillPaymentMethod(self)->pd.Series:
        return self.data.iloc[:,5]
    
    def getBillPaymentStatus(self)->pd.Series:
        return self.data.iloc[:,6]
    
    
class HrManagerReader(File_reader):
    def __init__(self, file :str)->None:
        super().__init__(file)

    def getHrManagerId(self)->pd.Series:
        return self.data.iloc[:,0]
    
    def getHrManagerFirstName(self)->pd.Series:
        return self.data.iloc[:,1]
    
    def getHrManagerLastName(self)->pd.Series:
        return self.data.iloc[:,2]
    
    def getHrManagerPhone(self)->pd.Series:
        return self.data.iloc[:,3]
    
    def getHrManagerExperience(self)->pd.Series:
        return self.data.iloc[:,4]
    
    def getHrManagerBranch(self)->pd.Series:
        return self.data.iloc[:,5]
    
    def getHrManagerEmail(self)->pd.Series:
        return self.data.iloc[:,6]
    
    def getHrManagerPassword(self)->pd.Series:
        return self.data.iloc[:,7]
    
class InvManagerReader(File_reader):
    def __init__(self, file :str)->None:
        super().__init__(file)

    def getInvManagerId(self)->pd.Series:
        return self.data.iloc[:,0]


    def getInvManagerFirstName(self)->pd.Series:
        return self.data.iloc[:,1]

    def getInvManagerLastName(self)->pd.Series:
        return self.data.iloc[:,2]

    def getInvManagerPhone(self)->pd.Series:
        return self.data.iloc[:,3]

    def getInvManagerExperience(self)->pd.Series:
        return self.data.iloc[:,4]

    def getInvManagerBranch(self)->pd.Series:
        return self.data.iloc[:,5]

    def getInvManagerEmail(self)->pd.Series:
        return self.data.iloc[:,6]

    def getInvManagerPassword(self)->pd.Series:
        return self.data.iloc[:,7]


class PatientReader(File_reader):
    def __init__(self, file: str)->None:
        super().__init__(file)

    def getPatientId(self)->pd.Series:
        return self.data.iloc[:,0]

    def getPatientFirstName(self)->pd.Series:
        return self.data.iloc[:,1]

    def getPatientLastName(self)->pd.Series:
        return self.data.iloc[:,2]
    
    def getPatientGender(self)->pd.Series:
        return self.data.iloc[:,3]

    def getPatientBirth(self)->pd.Series:
        return self.data.iloc[:,4]

    def getPatientNumber(self)->pd.Series:
        return self.data.iloc[:,5]

    def getPatientAddress(self)->pd.Series:
        return self.data.iloc[:,6]

    def getPatientRegistrationDate(self)->pd.Series:
        return self.data.iloc[:,7]

    def getPatientInsuranceProvider(self)->pd.Series:
        return self.data.iloc[:,8]

    def getPatientInsuranceNumber(self)->pd.Series:
        return self.data.iloc[:,9]

    def getPatientEmail(self)->pd.Series:
        return self.data.iloc[:,10]
    
    def getPatientPassword(self)->pd.Series:
        return self.data.iloc[:,11]

class PharmacistReader(File_reader):
    def __init__(self, file: str)->None:
        super().__init__(file)

    def getPharmacistId(self)->pd.Series:
        return self.data.iloc[:,0]

    def getPharmacistFirstName(self)->pd.Series:
        return self.data.iloc[:,1]

    def getPharmacistLastName(self)->pd.Series:
        return self.data.iloc[:,2]

    def getPharmacistSpecialization(self)->pd.Series:
        return self.data.iloc[:,3]

    def getPharmacistBranch(self)->pd.Series:
        return self.data.iloc[:,4]

    def getPharmacistEmail(self)->pd.Series:
        return self.data.iloc[:,5]

    def getPharmacistPassword(self)->pd.Series:
        return self.data.iloc[:,6]
    

class TreatmentReader(File_reader):
    def __init__(self, file)->None:
        super().__init__(file)

    def getTreatmentId(self)->pd.Series:
        return self.data.iloc[:,0]

    def getAppointmentId(self)->pd.Series:
        return self.data.iloc[:,1]

    def getTreatmentType(self)->pd.Series:
        return self.data.iloc[:,2]

    def getTreatmentDescription(self)->pd.Series:
        return self.data.iloc[:,3]

    def getTreatmentCost(self)->pd.Series:
        return self.data.iloc[:,4]

    def getTreatmentDate(self)->pd.Series:
        return self.data.iloc[:,5]
    
class SecretaryReader(File_reader):
    def __init__(self, file:str):
        super().__init__(file)

    def getSecretaryId(self) ->pd.Series:
        return self.data.iloc[:,0]
    
    def getSecretaryFirstName(self) ->pd.Series:
        return self.data.iloc[:,1]
    
    def getSecretaryLastName(self) ->pd.Series:
        return self.data.iloc[:,2]
    
    def getSecretaryPhone(self) ->pd.Series:
        return self.data.iloc[:,3]
    
    def getSecretaryExperience(self) ->pd.Series:
        return self.data.iloc[:,4]
    
    def getSecretaryBranch(self) ->pd.Series:
        return self.data.iloc[:,5]
    
    def getSecretaryEmail(self) ->pd.Series:
        return self.data.iloc[:,6]
    
    def getSecretaryPassword(self) ->pd.Series:
        return self.data.iloc[:,7]


class NurseReader(File_reader):
        def __init__(self, file:str):
            super().__init__(file)

        def getNurseId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getNurseFirstName(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getNurseLastName(self) ->pd.Series:
            return self.data.iloc[:,2]
    
        def getNursePhone(self) ->pd.Series:
            return self.data.iloc[:,3]
    
        def getNurseExperience(self) ->pd.Series:
            return self.data.iloc[:,4]
    
        def getNurseBranch(self) ->pd.Series:
            return self.data.iloc[:,5]
    
        def getNurseEmail(self) ->pd.Series:
            return self.data.iloc[:,6]
    
        def getNursePassword(self) ->pd.Series:
            return self.data.iloc[:,7]

class ShiftReader(File_reader):
        def __init__(self, file:str):
            super().__init__(file)

        def getStaffId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getStaffFirstName(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getStaffLastName(self) ->pd.Series:
            return self.data.iloc[:,2]

        def getStaffDate(self) ->pd.Series:
            return self.data.iloc[:,3]

        def getStaffStart(self) ->pd.Series:
            return self.data.iloc[:,4]

        def getStaffEnd(self) ->pd.Series:
            return self.data.iloc[:,5]
        
        def save_shift(self,id, name, surname, date, time_begin, time_end):

            new_shift= {"id": [id], "first_name": [name],"last_name": [surname],"date": [date],"start": [time_begin],"end": [time_end]}
            new_df = pd.DataFrame(new_shift)

            if os.path.exists(self.file):
                try:
                    existing_df = pd.read_csv(self.file)
                    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                    updated_df.to_csv(self.file, index=False)
                    print(f"Shift appended successfully file.")
                except Exception as e:
                    print(f"Error updating CSV file: {e}")
            else:
                try:
                    new_df.to_csv(self.file, index=False)
                    print(f"File created and shift saved successfully.")
                except Exception as e:
                    print(f"Error creating CSV file: {e}")
            

class HospitalStaffReader:
    def __init__(self):
        self.DocReader = DocReader(data_path("uc7_doctors.csv"))
        self.NurseReader = NurseReader(data_path("uc7_nurses.csv"))
        self.ShiftReader = ShiftReader(data_path("uc7_scheduledShifts.csv"))

    def find_by_name_surname(self, name, surname):

        name = name.lower()
        surname = surname.lower()

        results=[]

        #Doctors
        doc_df = self.DocReader.data
        doc_mask = (doc_df.iloc[:, 1].str.lower() == name) & (doc_df.iloc[:, 2].str.lower() == surname)
        doc_result = doc_df[doc_mask]

        if not doc_result.empty:
            results.extend([
                self.process_info_doctor(row.to_dict())
                for _, row in doc_result.iterrows()])


        #Nurses
        nurse_df = self.NurseReader.data
        nurse_mask = (
            nurse_df.iloc[:, 1].str.lower() == name) & (nurse_df.iloc[:, 2].str.lower() == surname)

        nurse_result = nurse_df[nurse_mask]

        if not nurse_result.empty:
            results.extend([self.process_info_nurse(row.to_dict())
            for _, row in nurse_result.iterrows()])

        return results if results else None


    def find_Shifts(self, id):
        id = str(id)

        results = []

        shift_df = self.ShiftReader.data
        shift_mask = (shift_df.iloc[:, 0].astype(str) == id)
        shift_result = shift_df[shift_mask]

        if not shift_result.empty:
            results.extend([
                self.process_info_shift(row.to_dict()) 
                for _, row in shift_result.iterrows()
            ])
        
        return results if results else None


    
    def process_info_doctor(self, raw_data):
        
        processed_data = {
            'id': raw_data.get('id'),
            'first_name': raw_data.get('first_name'),
            'last_name': raw_data.get('last_name'),
            'specialization': raw_data.get('specialization'),
            'phone_number': raw_data.get('phone_number'),
            'years_experience' : raw_data.get('years_experience'),
            'hospital_branch': raw_data.get('hospital_branch'),
            'email': raw_data.get('email'),
            'password': raw_data.get('password')}

        return processed_data

    def process_info_nurse(self, raw_data):
        processed_data = {
            'id': raw_data.get('id'),
            'first_name': raw_data.get('first_name'),
            'last_name': raw_data.get('last_name'),
            'specialization': raw_data.get('specialization'),
            'phone_number': raw_data.get('phone_number'),
            'experience' : raw_data.get('experience'),
            'branch': raw_data.get('branch'),
            'email': raw_data.get('email'),
            'password': raw_data.get('password')}

        return processed_data

    def process_info_shift(self, raw_data):
        processed_data = {
            'id': raw_data.get('id'),
            'first_name':raw_data.get('first_name'),
            'last_name':raw_data.get('last_name'),
            'date': raw_data.get('date'),
            'start': raw_data.get('start'),
            'end': raw_data.get('end')}

        return processed_data
        
    





    
        
