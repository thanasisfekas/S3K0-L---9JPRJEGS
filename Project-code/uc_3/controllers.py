import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MenuControllers.Reader.readerHandlers import MedReader,EquipReader
from uc_3.models import Inventory,OrderLog,Order
from uc_3.screens import InvSearchScreen,SearchResultScreen,MessageScreen,OrderScreen,OrderConfirmationScreen,SuccessScreen

class InvMgMainMenuController:
    def __init__(self,parent):
        self.parent = parent

        # init inventory search controller
        self.searchController = InvSearchController(self.parent)

class InvSearchController:
    def __init__(self,parent):
        self.parent = parent
        self.inventory = Inventory(pd.DataFrame({"Medicines": [MedReader("../Data/medicines.csv").data] , "Equipment": [EquipReader("../Data/equipment.csv").data]}))
        self.available_inv = self.inventory.inventory
        self.searchScreen = InvSearchScreen(self.parent,self)
        self.searchScreen.display()
        self.searchScreen.showResults()
        self.SearchResultScreen = SearchResultScreen(self.parent,self)
        self.OrderController = OrderController(self.parent,self)

    def getInvItem(self):
        self.searched_item = self.searchScreen.search_entry.get()
        self.res = self.inventory.searchInvItem(self.searched_item)

        if self.res is None:
            messageScreen = MessageScreen(self.parent)
            messageScreen.dispError("No Item Found")
        else :
            # messagebox.showinfo("","Item Found")
            self.SearchResultScreen.display()
            self.SearchResultScreen.displayResults(self.res)

class OrderController:
    def __init__(self,parent,controller):
        self.parent = parent
        self.search_controller= controller
        self.orderScreen = OrderScreen(self.parent,self)
        self.orderLog = OrderLog("order_log.csv")

    def startOrder(self,data):
        self.data = data
        self.orderScreen.showOrderForm(self.data)

    def setFormDetails(self):
        self.order_amount = self.orderScreen.orderAmountMenu.get()
        self.more_info = self.orderScreen.displayBox.get("1.0", "end-1c")
        self.checkFormIntegrity()

    def checkFormIntegrity(self):
        if not self.order_amount:
            messageScreen = MessageScreen("Form is not filled")
            messageScreen.dispError()
        else:
            self.order = Order(self.data , self.order_amount , self.more_info)
            self.conf_screen = OrderConfirmationScreen("Submit Order ?")
            self.conf_screen.displayConfirmationMessage()
            self.orderLog.submitOrder(self.order.getOrder())
            self.successScreen = SuccessScreen("Order Submitted to OrderLog")
            self.successScreen.showSuccMsg()
            # return to search screen after submit
            self.orderScreen.pack_forget()
            self.search_controller.SearchResultScreen.pack_forget()
            self.search_controller.searchScreen.display()
