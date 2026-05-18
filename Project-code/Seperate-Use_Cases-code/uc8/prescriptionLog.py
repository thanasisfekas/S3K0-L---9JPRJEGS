from readerHandlers import PrescriptionsReader

class PrescriptionLog:
    def __init__(self, id):
        self.id = id 
        self.PrescriptionsReader = PrescriptionsReader("prescriptions.csv")
        
    def findPrescriptions(self):
        pat_id = str(self.id).strip()
        results = []

        df = self.PrescriptionsReader.data
        
        mask = (df.iloc[:, 1].astype(str).str.strip() == pat_id)
        result = df[mask]

        if not result.empty:
            results.extend([
                row.to_dict() 
                for _, row in result.iterrows()])
        
        print(results)
        return results if results else None