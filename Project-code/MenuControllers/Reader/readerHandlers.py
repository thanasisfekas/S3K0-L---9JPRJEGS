from .file_reader import File_reader
import pandas as pd

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
    
    def getDoctorsBySpecialty(self, specialty):
        filtered = self.data[self.getDoctorSpecialization() == specialty].copy()
        return filtered.sort_values(by=["last_name", "first_name"])
    
    def getDoctorFullName(self, doctor_id):
        row = self.data[self.data["doctor_id"] == doctor_id].iloc[0]
        return f"Dr. {row['first_name']} {row['last_name']}"

class DoctorSpecialtyReader(File_reader):
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def getSpecialtyId(self) -> pd.Series:
        return self.data.iloc[:,0]

    def getSpecialtyName(self) -> pd.Series:
        return self.data.iloc[:,1]

class DoctorAppointmentTimeSlotsReader(File_reader):
    def __init__(self, file: str) -> None:
        super().__init__(file)

    def getDoctorId(self) -> pd.Series:
        return self.data.iloc[:,0]

    def getAvailableDate(self) -> pd.Series:
        return self.data.iloc[:,1]

    def getAvailableTime(self) -> pd.Series:
        return self.data.iloc[:,2]
    
    def getAvailableSlots(self, doctor_id, date):
        slots = self.data[(self.data["doctor_id"] == doctor_id) & (self.data["available_date"] == date)]["available_time"]
        return pd.to_datetime(slots, format="%H:%M:%S").sort_values().dt.strftime("%H:%M:%S").tolist()
    
    def removeSlot(self, doctor_id, date, time):
        self.data = self.data[~((self.data["doctor_id"] == doctor_id) & (self.data["available_date"] == date) & (self.data["available_time"] == time))]
        self.data.to_csv(self.file, index=False)

    def restoreSlot(self, doctor_id, date, time):
        new_row = {"doctor_id": doctor_id, "available_date": date, "available_time": time}
        self.data.loc[len(self.data)] = new_row
        self.data.to_csv(self.file, index=False)

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
    
    def createAppointment(self, patient_id, doctor_id, date, time):
        last_num = self.getAppointmentId().str.replace("A", "").astype(int).max()
        new_id = f"A{last_num+1:03}"
        new_row = {
            "appointment_id": new_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": date,
            "appointment_time": time,
            "reason_for_visit": "General Consultation",
            "status": "Booked"
        }
        self.data.loc[len(self.data)] = new_row
        self.data.to_csv(self.file, index=False)
    

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
    
    def getBillsByPatient(self, patient_id):
        bills = self.data[self.getPatientId() == patient_id].copy()
        pending = bills[bills["payment_status"] == "Pending"]
        paid = bills[bills["payment_status"] == "Paid"]
        return pd.concat([pending, paid])
    
    def markBillPaid(self, bill_id):
        self.data.loc[self.getBillId() == bill_id, "payment_status"] = "Paid"
        self.data.to_csv(self.file, index=False)
    
    
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
    
    def getTreatmentDescriptionById(self, treatment_id):
        row = self.data[self.getTreatmentId() == treatment_id].iloc[0]
        return f"{row['treatment_type']}: {row['description']}"
    
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
        


class MedReader(File_reader):
        def __init__(self, file:str):
            super().__init__(file)

        def getMedId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getMedName(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getMedCategory(self) ->pd.Series:
            return self.data.iloc[:,2]
    
        def getMedStock(self) ->pd.Series:
            return self.data.iloc[:,3]
    
        def getMedExpires(self) ->pd.Series:
            return self.data.iloc[:,4]
    
        def getMedPrice(self) ->pd.Series:
            return self.data.iloc[:,5]

class EquipReader(File_reader):
        def __init__(self, file:str):
            super().__init__(file)

        def getEquipId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getEquipName(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getEquipType(self) ->pd.Series:
            return self.data.iloc[:,2]
    
        def getEquipStock(self) ->pd.Series:
            return self.data.iloc[:,3]
        

class WardReader(File_reader):
    def __init__(self, file:str):
        super().__init__(file)

        def getWardId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getWardName(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getWardAvailability(self) ->pd.Series:
            return self.data.iloc[:,2]
        
class LabTestRequestReader(File_reader):
    def __init__(self, file:str):
        super().__init__(file)

        def getReqId(self) ->pd.Series:
            return self.data.iloc[:,0]
    
        def getReqPatientId(self) ->pd.Series:
            return self.data.iloc[:,1]
    
        def getFolderId(self) ->pd.Series:
            return self.data.iloc[:,2]
        
        def getReqDocId(self) ->pd.Series:
            return self.data.iloc[:,2]
                                  
        def getTestName(self) ->pd.Series:
            return self.data.iloc[:,3]
        
        def getReqReason(self) ->pd.Series:
            return self.data.iloc[:,4]
        
        def getReqStatus(self) ->pd.Series:
            return self.data.iloc[:,5]
        
        def getReqDate(self) ->pd.Series:
            return self.data.iloc[:,6]
        
        # def submitLabtest(self,req):
        #     pass