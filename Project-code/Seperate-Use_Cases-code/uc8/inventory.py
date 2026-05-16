from readerHandlers import InvMedReader
import os

class Inventory:
    def __init__(self, med_id):
        self.med_id = med_id
        self.InvMedReader = InvMedReader("medicines.csv")

    def searchQuantity(self):
        med_id = str(self.med_id).strip()

        df = self.InvMedReader.data
        mask = (df.iloc[:, 0].astype(str) == med_id)
        result = df[mask]
        
        if not result.empty:
            return int(result.iloc[0, 3])
            
        return 0

    def updateInventory(self, new_quantity):
        med_id = str(self.med_id).strip()
        df = self.InvMedReader.data
        
        mask = (df.iloc[:, 0].astype(str) == med_id)
        
        if mask.any():
            df.iloc[mask, 3] = new_quantity
            
            df.to_csv("medicines.csv", index=False)
            #print("The stock has changed")



