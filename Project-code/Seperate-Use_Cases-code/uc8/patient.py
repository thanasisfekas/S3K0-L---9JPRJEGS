from readerHandlers import PatientReader

class Patient:
    def __init__(self, id, name, last_name):
        self.PatientReader=PatientReader("patients.csv")
        self.id = id 
        self.name = name
        self.last_name= last_name

    def find_patient(self):
        pat_id = str(self.id).strip()
        results = []

        df = self.PatientReader.data
        mask = (df.iloc[:, 0].astype(str) == pat_id)
        result = df[mask]

        if not result.empty:
            results.extend([self.process_info_patient(row.to_dict()) for _, row in result.iterrows()])
        
        return results if results else None

    
    def process_info_patient(self, raw_data):
        processed_data = {'patient_id': raw_data.get('patient_id'),'first_name': raw_data.get('first_name'),'last_name': raw_data.get('last_name'),'gender': raw_data.get('gender'),'date_of_birth': raw_data.get('date_of_birth')}

        return processed_data




    
