from .file_reader import File_reader
import pandas as pd
import csv

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

    def findDoc(self, doc_id):
        df = self.data
        mask = df.iloc[:, 0].astype(str).str.strip() == str(doc_id).strip()
        result = df[mask]

        if not result.empty:
            name = result.iloc[0, 1]
            lastname = result.iloc[0, 2]
            return f"{name} {lastname}"

        return "Unknown Doctor"

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

    def find_patient(self, id, name, last_name):
        pat_id = str(id).strip()
        df = self.data

        mask = df.iloc[:, 0].astype(str).str.strip() == pat_id

        if name:
            mask &= df.iloc[:, 1].astype(str).str.lower() == str(name).strip().lower()
        if last_name:
            mask &= df.iloc[:, 2].astype(str).str.lower() == str(last_name).strip().lower()

        result = df[mask]

        if not result.empty:
            return [self.process_info_patient(row) for _, row in result.iterrows()]

        return None

    def process_info_patient(self, row):
        return {
            "patient_id": row.iloc[0],
            "first_name": row.iloc[1],
            "last_name": row.iloc[2],
            "gender": row.iloc[3],
            "date_of_birth": row.iloc[4],
        }

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

        def save_shift(self, id, name, surname, date, time_begin, time_end):
            new_shift = {
                "id": [id],
                "first_name": [name],
                "last_name": [surname],
                "date": [date],
                "start": [time_begin],
                "end": [time_end],
            }
            new_df = pd.DataFrame(new_shift)
            updated_df = pd.concat([self.data, new_df], ignore_index=True)
            updated_df.to_csv(self.file, index=False)
            self.data = updated_df


class HospitalStaffReader:
    def __init__(self):
        self.DocReader = DocReader("doctors.csv")
        self.NurseReader = NurseReader("nurses.csv")
        self.ShiftReader = ShiftReader("scheduledShifts.csv")

    def find_by_name_surname(self, name, surname):
        name = name.lower()
        surname = surname.lower()
        results = []

        doc_df = self.DocReader.data
        doc_mask = (doc_df.iloc[:, 1].astype(str).str.lower() == name) & (doc_df.iloc[:, 2].astype(str).str.lower() == surname)
        doc_result = doc_df[doc_mask]

        if not doc_result.empty:
            results.extend([
                self.process_info_doctor(row.to_dict())
                for _, row in doc_result.iterrows()
            ])

        nurse_df = self.NurseReader.data
        nurse_mask = (nurse_df.iloc[:, 1].astype(str).str.lower() == name) & (nurse_df.iloc[:, 2].astype(str).str.lower() == surname)
        nurse_result = nurse_df[nurse_mask]

        if not nurse_result.empty:
            results.extend([
                self.process_info_nurse(row.to_dict())
                for _, row in nurse_result.iterrows()
            ])

        return results if results else None

    def find_Shifts(self, id):
        id = str(id)
        results = []

        shift_df = self.ShiftReader.data
        shift_mask = shift_df.iloc[:, 0].astype(str) == id
        shift_result = shift_df[shift_mask]

        if not shift_result.empty:
            results.extend([
                self.process_info_shift(row.to_dict())
                for _, row in shift_result.iterrows()
            ])

        return results if results else None

    def process_info_doctor(self, raw_data):
        return {
            "id": raw_data.get("id", raw_data.get("doctor_id")),
            "first_name": raw_data.get("first_name"),
            "last_name": raw_data.get("last_name"),
            "specialization": raw_data.get("specialization", "Doctor"),
            "phone_number": raw_data.get("phone_number"),
            "years_experience": raw_data.get("years_experience"),
            "hospital_branch": raw_data.get("hospital_branch"),
            "email": raw_data.get("email"),
            "password": raw_data.get("password"),
        }

    def process_info_nurse(self, raw_data):
        return {
            "id": raw_data.get("id", raw_data.get("nurse_id")),
            "first_name": raw_data.get("first_name"),
            "last_name": raw_data.get("last_name"),
            "specialization": raw_data.get("specialization", raw_data.get("branch", "Nurse")),
            "phone_number": raw_data.get("phone_number"),
            "experience": raw_data.get("experience", raw_data.get("experience_years")),
            "branch": raw_data.get("branch"),
            "email": raw_data.get("email"),
            "password": raw_data.get("password"),
        }

    def process_info_shift(self, raw_data):
        return {
            "id": raw_data.get("id"),
            "first_name": raw_data.get("first_name"),
            "last_name": raw_data.get("last_name"),
            "date": raw_data.get("date"),
            "start": raw_data.get("start"),
            "begin": raw_data.get("start"),
            "end": raw_data.get("end"),
        }
        


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

        def findMed(self, med_id):
            target_id = str(med_id).strip()
            df = self.data

            mask = df.iloc[:, 0].astype(str).str.strip() == target_id
            result = df[mask]

            if not result.empty:
                return result.iloc[0, 1]

            return "Unknown Medicine"


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

        mask = df.iloc[:, 1].astype(str).str.strip() == pat_id
        result = df[mask]

        if not result.empty:
            return [self.process_prescription_info(row) for _, row in result.iterrows()]

        return None

    def process_prescription_info(self, row):
        return {
            "prescription_id": row.iloc[0],
            "patient_id": row.iloc[1],
            "doctor_id": row.iloc[2],
            "medicine_id": row.iloc[3],
            "date": row.iloc[4],
            "dosage": row.iloc[5],
            "status": row.iloc[6],
        }


class InvMedReader(MedReader):
    def searchQuantity(self, med_id):
        med_id = str(med_id).strip()
        df = self.data

        mask = df.iloc[:, 0].astype(str).str.strip() == med_id
        result = df[mask]

        if not result.empty:
            return int(result.iloc[0, 3])

        return 0

    def updateInventory(self, med_id, new_quantity):
        med_id = str(med_id).strip()
        mask = self.data.iloc[:, 0].astype(str).str.strip() == med_id

        if mask.any():
            self.data.loc[mask, self.data.columns[3]] = new_quantity
            self.data.to_csv(self.file, index=False)

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
        return self.data.iloc[:,3]
        
    def getReqStatus(self) ->pd.Series:
        return self.data.iloc[:,4]
        
    def getReqDate(self) ->pd.Series:
        return self.data.iloc[:,5]
        
    def submitLabtest(self,req):
        with open(self.file, 'a', newline='') as file:
            writer = csv.DictWriter(file,fieldnames=["request_id","patient_id","folder_id","doctor_id","status","request_date"])
            writer.writerow(req)

    def generate_req_id(self):
        with open(self.file , 'r' , newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row["request_id"]
            new_id = f"LTR{int(id.lstrip('LTR')) + 1:03d}"
        return new_id

class PatientFolderReader(File_reader):
    def __init__(self, file):
        super().__init__(file)


class PatientAdmissionReader(File_reader):
    def __init__(self, file):
        super().__init__(file)

    def submitAdmission(self,admission):
        with open(self.file, 'a', newline='') as file:
            writer = csv.DictWriter(file,fieldnames=["admission_id","patient_id","doctor_id","reason","status","admission_date"])
            writer.writerow(admission)

    def generate_adm_id(self):
        with open(self.file , 'r' , newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row["admission_id"]
            new_id = f"ADM{int(id.lstrip('ADM')) + 1:03d}"
        return new_id