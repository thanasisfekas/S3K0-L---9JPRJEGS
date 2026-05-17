from pathlib import Path
import pandas as pd

from MenuControllers.Reader.readerHandlers import (
    BillingReader,
    TreatmentReader
)
from .bill_management_screen import BillManagementScreen
from .bill_management_screen import apply_style
from .bill_details_screen import BillDetailScreen
from .payment_controller import PaymentController

class BillManagementController:
    def __init__(self, patient_id, root):
        self.patient_id = patient_id
        self.root = root
        self.patient_bills = None
        self.selected_bill = None
        # loop control until the actor chooses an unpaid bill
        self.billUnpaidFlag = False
        # initialize payment controller
        self.payment_controller = PaymentController(self.root, self)

    def getPatientBills(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "final_billing.csv"
        reader = BillingReader(str(path))
        self.patient_bills = reader.getBillsByPatient(self.patient_id)
        return self.patient_bills
    

    def displayBillManagementScreen(self):
        self._clear_screen()
        bills = self.getPatientBills()

        pending = bills[bills["payment_status"] == "Pending"]
        paid = bills[bills["payment_status"] == "Paid"]

        bills = pd.concat([pending, paid])
        self.current_screen = BillManagementScreen(self.root, bills, on_select=self.getBillDetails)
        return self.current_screen
    
    def getBillDetails(self, bill_id):
        self.selected_bill = self.patient_bills[self.patient_bills["bill_id"] == bill_id].iloc[0]
        self.checkBillUnpaid()
        # alt 1
        if self.billUnpaidFlag:
            self.displayBillDetailScreen()
        else:
            self.current_screen.showError("This bill is already paid.")

    def checkBillUnpaid(self):
        status = self.selected_bill["payment_status"]
        if status.lower() == "pending":
            self.billUnpaidFlag = True
        else:
            self.billUnpaidFlag = False

    def displayBillDetailScreen(self):
        self._clear_screen()

        bill_id = self.selected_bill["bill_id"]
        amount = self.selected_bill["amount"]
        date = self.selected_bill["bill_date"]
        treatment_description = self._getTreatmentDescription(self.selected_bill["treatment_id"])
        self.current_screen = BillDetailScreen(self.root, amount=amount, date=date, treatment=treatment_description, bill_id=bill_id, pay_command=self.initializePayment, back_command=self.displayBillManagementScreen)

        return self.current_screen
    
    def initializePayment(self):
        self.payment_controller.startPayment(self.selected_bill["bill_id"], self.selected_bill["amount"])

    # called from PaymentController
    def returnToBillList(self):
        self.displayBillManagementScreen()

    # helpers
    def _getTreatmentDescription(self, treatment_id):
        path = Path(__file__).resolve().parents[2] / "Data" / "final_treatments.csv"
        reader = TreatmentReader(str(path))
        return reader.getTreatmentDescriptionById(treatment_id)

    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()



if __name__ == "__main__":
    import tkinter as tk
    from .bill_management_screen import apply_style

    app_root = tk.Tk()
    app_root.title("Healthcare Billing System")
    app_root.geometry("900x600")

    # apply global ttk styling
    apply_style()

    # test patient id
    controller = BillManagementController(
        patient_id="P036",
        root=app_root
    )

    # launch use case
    controller.displayBillManagementScreen()

    app_root.mainloop()

