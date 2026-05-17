from readerHandlers import MedReader

class Medicine:
    def __init__(self, med_id):
        self.med_id = med_id
        self.MedReader = MedReader("medicines.csv")

    def findMed(self):
        df = self.MedReader.data
        mask = (df.iloc[:, 0].astype(str).str.strip() == self.med_id)
        result = df[mask]

        if not result.empty:
            return result.iloc[0, 1]
            
        return "Unknown Medicine"