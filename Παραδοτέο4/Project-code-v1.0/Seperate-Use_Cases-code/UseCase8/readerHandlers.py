from file_reader import File_reader
import pandas as pd

class DocReader(File_reader):
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def getDoctorId(self) -> pd.Series:
        return self.data.iloc[:, 0]
    
    def getDoctorFirstName(self) -> pd.Series:
        return self.data.iloc[:, 1]
    
    def getDoctorLastName(self) -> pd.Series:
        return self.data.iloc[:, 2]
    
    def getDoctorSpecialization(self) -> pd.Series:
        return self.data.iloc[:, 3]
    
    def getDoctorNumber(self) -> pd.Series:  
        return self.data.iloc[:, 4]
    
    def getDoctorExperience(self) -> pd.Series:
        return self.data.iloc[:, 5]
    
    def getDoctorBranch(self) -> pd.Series:       
        return self.data.iloc[:, 6]
    
    def getDoctorEmail(self) -> pd.Series:
        return self.data.iloc[:, 7]
    
    def getDoctorPassword(self) -> pd.Series:
        return self.data.iloc[:, 8]

    def findDoc(self, doc_id):
        df = self.data
        mask = (df.iloc[:, 0].astype(str).str.strip() == str(doc_id).strip())
        result = df[mask]

        if not result.empty:
            name = result.iloc[0, 1]
            lastname = result.iloc[0, 2]
            return f"{name} {lastname}"
            
        return "Unknown Doctor"

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
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def getPatientId(self) -> pd.Series:
        return self.data.iloc[:, 0]

    def getPatientFirstName(self) -> pd.Series:
        return self.data.iloc[:, 1]

    def getPatientLastName(self) -> pd.Series:
        return self.data.iloc[:, 2]
    
    def getPatientGender(self) -> pd.Series:
        return self.data.iloc[:, 3]

    def getPatientBirth(self) -> pd.Series:
        return self.data.iloc[:, 4]

    def getPatientNumber(self) -> pd.Series:
        return self.data.iloc[:, 5]

    def getPatientAddress(self) -> pd.Series:
        return self.data.iloc[:, 6]

    def getPatientRegistrationDate(self) -> pd.Series:
        return self.data.iloc[:, 7]

    def getPatientInsuranceProvider(self) -> pd.Series:
        return self.data.iloc[:, 8]

    def getPatientInsuranceNumber(self) -> pd.Series:
        return self.data.iloc[:, 9]

    def getPatientEmail(self) -> pd.Series:
        return self.data.iloc[:, 10]
    
    def getPatientPassword(self) -> pd.Series:
        return self.data.iloc[:, 11]

    def find_patient(self, id, name, last_name):
        pat_id = str(id).strip()
        df = self.data 

        mask = (df.iloc[:, 0].astype(str) == pat_id)
        
        if name:
            mask &= (df.iloc[:, 1].astype(str).str.lower() == str(name).strip().lower())
        if last_name:
            mask &= (df.iloc[:, 2].astype(str).str.lower() == str(last_name).strip().lower())

        result = df[mask]

        if not result.empty:
            return [self.process_info_patient(row) for _, row in result.iterrows()]
        
        return None

    def process_info_patient(self, row):
        processed_data = {
            'patient_id': row.iloc[0],
            'first_name': row.iloc[1],
            'last_name': row.iloc[2],
            'gender': row.iloc[3],
            'date_of_birth': row.iloc[4]
        }
        return processed_data
    


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
        

class PrescriptionsReader(File_reader):
    def __init__(self, file: str):
        super().__init__(file)

    def getPrescriptionId(self) -> pd.Series:
        return self.data.iloc[:, 0]

    def getPatientId(self) -> pd.Series:
        return self.data.iloc[:, 1]

    def getDoctorId(self) -> pd.Series:
        return self.data.iloc[:, 2]

    def getMedicineId(self) -> pd.Series:
        return self.data.iloc[:, 3]

    def getDate(self) -> pd.Series:
        return self.data.iloc[:, 4]

    def getDosage(self) -> pd.Series:
        return self.data.iloc[:, 5]

    def getStatus(self) -> pd.Series:
        return self.data.iloc[:, 6]

    def findPrescriptions(self, patient_id):
        pat_id = str(patient_id).strip()
        df = self.data  
        
        mask = (df.iloc[:, 1].astype(str).str.strip() == pat_id)
        result = df[mask]

        if not result.empty:
            results = [self.process_prescription_info(row) for _, row in result.iterrows()]
            print(results)
            return results
        
        return None

    def process_prescription_info(self, row):
        return {
            'prescription_id': row.iloc[0],
            'patient_id': row.iloc[1],
            'doctor_id': row.iloc[2],
            'medicine_id': row.iloc[3],
            'date': row.iloc[4],
            'dosage': row.iloc[5],
            'status': row.iloc[6]}


class MedReader(File_reader):
    def __init__(self, file: str):
        super().__init__(file)

    def getMedId(self) -> pd.Series:
        return self.data.iloc[:, 0]

    def getMedName(self) -> pd.Series:
        return self.data.iloc[:, 1]

    def getMedCategory(self) -> pd.Series:
        return self.data.iloc[:, 2]

    def getMedStock(self) -> pd.Series:
        return self.data.iloc[:, 3]

    def getMedExpires(self) -> pd.Series:
        return self.data.iloc[:, 4]

    def getMedPrice(self) -> pd.Series:
        return self.data.iloc[:, 5]

    def findMed(self, med_id):
        target_id = str(med_id).strip()
        df = self.data  
        
        mask = (df.iloc[:, 0].astype(str).str.strip() == target_id)
        result = df[mask]

        if not result.empty:
            return result.iloc[0, 1]
        
        return "Unknown Medicine"


import pandas as pd

class InvMedReader(File_reader):
    def __init__(self, file: str):
        super().__init__(file)

    def getMedId(self) -> pd.Series:
        return self.data.iloc[:, 0]

    def getMedName(self) -> pd.Series:
        return self.data.iloc[:, 1]

    def getMedCategory(self) -> pd.Series:
        return self.data.iloc[:, 2]

    def getMedStock(self) -> pd.Series:
        return self.data.iloc[:, 3]

    def getMedExpires(self) -> pd.Series:
        return self.data.iloc[:, 4]

    def getMedPrice(self) -> pd.Series:
        return self.data.iloc[:, 5]

    def searchQuantity(self, med_id):
        med_id = str(med_id).strip()
        df = self.data  
        
        mask = (df.iloc[:, 0].astype(str).str.strip() == med_id)
        result = df[mask]
    
        if not result.empty:
            return int(result.iloc[0, 3])
        
        return 0

    def updateInventory(self, med_id, new_quantity):
        med_id = str(med_id).strip()
        df = self.data  
    
        mask = (df.iloc[:, 0].astype(str).str.strip() == med_id)
    
        if mask.any():
            df.iloc[mask, 3] = new_quantity
            df.to_csv(self.file, index=False) 


    
        