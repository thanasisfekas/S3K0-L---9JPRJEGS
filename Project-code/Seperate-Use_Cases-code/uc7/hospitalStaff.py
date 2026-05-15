from readerHandlers import DocReader
from readerHandlers import NurseReader
from readerHandlers import ShiftReader


class HospitalStaff:

    def __init__(self):
        self.DocReader = DocReader("doctors.csv")
        self.NurseReader = NurseReader("nurses.csv")
        self.ShiftReader = ShiftReader("scheduledShifts.csv")

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
        
    




