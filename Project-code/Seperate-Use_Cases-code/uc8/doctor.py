from readerHandlers import DocReader

class Doctor:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.DocReader = DocReader("doctors.csv")

    def findDoc(self):
        df = self.DocReader.data
        mask = (df.iloc[:, 0].astype(str).str.strip() == str(self.doc_id).strip())
        result = df[mask]

        if not result.empty:
            name = result.iloc[0, 1]
            lastname = result.iloc[0, 2]
            return f"{name} {lastname}"
            
        return "Unknown Doctor"