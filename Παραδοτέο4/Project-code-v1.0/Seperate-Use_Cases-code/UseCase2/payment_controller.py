from pathlib import Path
from datetime import datetime

from MenuControllers.Reader.readerHandlers import (
    BillingReader
)
from .payment_methods_screen import PaymentMethodSelectScreen
from .payment_form_screen import PaymentFormScreen
from .payment_completion_screen import PaymentCompletionScreen
from .payment_error_screen import PaymentErrorScreen


class PaymentController:
    def __init__(self, root, bill_management_controller):
        self.root = root
        self.bill_management_controller = bill_management_controller
        self.selected_bill_id = None
        self.selected_amount = None
        self.selected_payment_method = None

    def startPayment(self, bill_id, amount):
        self.selected_bill_id = bill_id
        self.selected_amount = amount
        self.displayPaymentMethodSelectScreen()

    def getPaymentMethods(self):
        return ["Debit", "Credit"]
    
    def displayPaymentMethodSelectScreen(self):
        self._clear_screen()
        methods = self.getPaymentMethods()
        self.current_screen = PaymentMethodSelectScreen(self.root, methods, on_select=self.setPaymentMethod, back_command=self.bill_management_controller.displayBillDetailScreen)

        return self.current_screen

    def setPaymentMethod(self, method):
        self.selected_payment_method = method
        self.getPaymentForm()

    def getPaymentForm(self):
        self.displayPaymentFormScreen()

    def displayPaymentFormScreen(self):
        self._clear_screen()
        self.current_screen = PaymentFormScreen(self.root, self.selected_payment_method, self.selected_amount, on_submit=self.processPaymentData, back_command=self.displayPaymentMethodSelectScreen)

        return self.current_screen
    
    # payment data validation logic
    def processPaymentData(self, payment_data):
        success = self.validatePayment(payment_data)

        # alt 2
        if success:
            self.updateBillStatus()
            receipt = self.createPaymentReceipt()
            self.addPaymentReceipt(receipt)
            self.displayPaymentCompletionScreen(receipt)

        else:
            self.displayPaymentErrorScreen()

    def validatePayment(self, payment_data):
        card_number = payment_data.get("card_number")
        cvv = payment_data.get("cvv")
        if (card_number and len(card_number) == 16 and card_number.isdigit() and cvv and len(cvv) == 3 and cvv.isdigit()):
            return True
        return False

    def updateBillStatus(self):
        path = Path(__file__).resolve().parents[2] / "Data" / "billing.csv"
        reader = BillingReader(str(path))
        reader.markBillPaid(self.selected_bill_id)

    def createPaymentReceipt(self):
        return {"bill_id": self.selected_bill_id, "amount": self.selected_amount, "method": self.selected_payment_method, "date": datetime.now().strftime("%Y-%m-%d")}

    def addPaymentReceipt(self, receipt):
        # placeholder for persistence
        return receipt
    
    def displayPaymentCompletionScreen(self, receipt):
        self._clear_screen()
        self.current_screen = PaymentCompletionScreen(self.root, receipt, close_command=self.bill_management_controller.returnToBillList)

        return self.current_screen

    def displayPaymentErrorScreen(self):
        self._clear_screen()
        self.current_screen = PaymentErrorScreen(self.root, message="Invalid card details. Payment Cacnelled.", close_command=self.cancelPayment)
        return self.current_screen

    def cancelPayment(self):
        self.bill_management_controller.returnToBillList()

    # helper
    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()



