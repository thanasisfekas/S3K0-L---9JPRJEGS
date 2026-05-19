from readerHandlers import PrescriptionsReader, MedReader, DocReader, InvMedReader
from prescriptionsScreen import PrescriptionsScreen   
from drugScreen import DrugScreen
from medicineQuantityScreen import MedicineQuantityScreen

import tkinter as tk
from tkinter import messagebox

class PrescriptionController:
    def __init__(self, root, main_app, id):  
        self.root = root
        self.parent_controller = main_app
        self.current_controller = None
        self.current_screen = None

        self.id = id
        self.prescriptions = []  
        self.selected_prescription_id = ""
        self.processed_drugs = [] 

        self.searchPrescriptions()

    def searchPrescriptions(self):
        p = PrescriptionsReader("prescriptions.csv")
        raw_prescriptions = p.findPrescriptions(self.id)

        if raw_prescriptions: 
            grouped = {}
            for row in raw_prescriptions:
                p_id = row.get('prescription_id')
                if not p_id:
                    continue
                
                if p_id not in grouped:
                    grouped[p_id] = {
                        'prescription_id': p_id,
                        'patient_id': row.get('patient_id'),
                        'doctor_id': row.get('doctor_id'),
                        'date': row.get('date'),
                        'status': row.get('status'),
                        'medicines': []}
                
                med_id = row.get('medicine_id')
                dosage = row.get('dosage', 'No instructions provided')
                if med_id:
                    grouped[p_id]['medicines'].append({
                        'id': med_id,
                        'name': '', 
                        'dosage': dosage})

            self.prescriptions = list(grouped.values())
            self.mapMedicine()
            self.mapDoctor()
            self.displayPrescriptions()  
        else:
            messagebox.showerror("Error!", "There aren't any prescriptions for this patient \nTry again...")
            self.returnToSearchScreen()  

    def mapMedicine(self):
        m = MedReader("medicines.csv")
    
        for prescription in self.prescriptions:
            for med_item in prescription.get('medicines', []):
                clean_med_id = str(med_item['id']).strip()
            
                m_name = m.findMed(clean_med_id)  
                if m_name and m_name != "Unknown Medicine":
                    med_item['name'] = m_name
                else:
                    med_item['name'] = f"Unknown ({clean_med_id})"
        return

    def mapDoctor(self):
        for prescription in self.prescriptions:
            doc_id = prescription.get('doctor_id')
            if doc_id:
                d = DocReader("doctors.csv")
                d_name = d.findDoc(doc_id)
                prescription['doctor_id'] = d_name

    def returnToSearchScreen(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        from searchPatientController import SearchPatientController
        new_search_app = SearchPatientController(self.root)
        new_search_app.displaySearchScreen()

    def displayPrescriptions(self):
        for widget in self.root.winfo_children():
            widget.destroy() 

        self.current_screen = PrescriptionsScreen(self.root, self.prescriptions, controller=self)

    def selectPrescription(self, prescription_id):
        self.selected_prescription_id = prescription_id
        current_prescription = next((p for p in self.prescriptions if p.get('prescription_id') == prescription_id), None)
        if current_prescription:
            self.processed_drugs = []
            self.displayPrescription(current_prescription)
        else:
            messagebox.showerror("Error", "Prescription data could not be found.")

    def displayPrescription(self, current_prescription):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_screen = DrugScreen(self.root, controller=self, prescription_data=current_prescription)
        

    def getDrug(self, drug):
        med_id = drug.get('id')
    
        if med_id not in self.processed_drugs:
            self.processed_drugs.append(med_id)
            self.displayMedicineQuantityScreen(drug)


    def displayMedicineQuantityScreen(self, drug):
        self.current_screen = MedicineQuantityScreen(self.root, controller=self, drug_data=drug)
        
    def submitDrugQuantity(self, drug, quantity_requested):
        med_id = drug.get('id')
        med_name = drug.get('name')
        
    
        inv = InvMedReader("medicines.csv")
        current_stock = inv.searchQuantity(med_id)
        
        if current_stock >= quantity_requested:
            new_stock = current_stock - quantity_requested
            inv.updateInventory(med_id, new_stock)
            
            messagebox.showinfo("Success!", f"Successfully processed {quantity_requested} unit(s) of {med_name}.")
            
            current_prescription = next((p for p in self.prescriptions if p.get('prescription_id') == self.selected_prescription_id), None)
            if current_prescription:
                total_medicines = len(current_prescription.get('medicines', []))
                
                if len(self.processed_drugs) == total_medicines:
                    messagebox.showinfo("Prescription Completed!", "All medicines in this prescription have been successfully processed.")
                    self.displayPrescriptions()
                else:
                    self.displayPrescription(current_prescription)
        else:
            messagebox.showerror("Stock Error!", "Not enough stock.Try again...")
            
            if med_id in self.processed_drugs:
                self.processed_drugs.remove(med_id)
            
            current_prescription = next((p for p in self.prescriptions if p.get('prescription_id') == self.selected_prescription_id), None)
            if current_prescription:
                self.displayPrescription(current_prescription)

    def cancelDrugSelection(self, med_id):
        if med_id in self.processed_drugs:
            self.processed_drugs.remove(med_id)
            
        current_prescription = next((p for p in self.prescriptions if p.get('prescription_id') == self.selected_prescription_id), None)
        if current_prescription:
            self.displayPrescription(current_prescription)