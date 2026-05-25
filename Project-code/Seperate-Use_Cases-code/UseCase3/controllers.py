import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MenuControllers.Reader.readerHandlers import MedReader,EquipReader
from UseCase3.models import Inventory,OrderLog,Order
from UseCase3.screens import InvSearchScreen,SearchResultScreen,MessageScreen,OrderScreen,OrderConfirmationScreen,SuccessScreen
from data_paths import data_path

class InvMgMainMenuController:
    def __init__(self,parent):
        self.parent = parent
        self.searchController = InvSearchController(self.parent)

class InvSearchController:
    def __init__(self,parent):
        self.parent = parent
        self.inventory = Inventory(pd.DataFrame({"Medicines": [MedReader(data_path("medicines.csv")).data] , "Equipment": [EquipReader(data_path("equipment.csv")).data]}))
        self.available_inv = self.inventory.inventory
        self.searchScreen = InvSearchScreen(self.parent,self)
        self.searchScreen.display()
        self.searchScreen.showResults()

    # get user input(item id) from search screen
    def getInvItem(self):
        self.searched_item = self.searchScreen.search_entry.get()
        # seach requested item
        self.res = self.inventory.searchInvItem(self.searched_item)

        # alt 2 check if searched patient exists
        if self.res is None:
            #alternative
            messageScreen = MessageScreen("No Item Found")
            messageScreen.dispError()
        else :
            # main flow
            self.SearchResultScreen = SearchResultScreen(self.parent,self)
            self.SearchResultScreen.display()
            self.SearchResultScreen.displayResults(self.res)
            self.OrderController = OrderController(self.parent,self)

class OrderController:
    def __init__(self,parent,controller):
        self.parent = parent
        self.search_controller= controller
        self.orderScreen = OrderScreen(self.parent,self)
        self.orderLog = OrderLog(data_path("order_log.csv"))

    def startOrder(self,data):
        self.data = data
        self.orderScreen.showOrderForm(self.data)

    # on click event for submit button in order screen
    def setFormDetails(self):
        self.order_amount = self.orderScreen.orderAmountMenu.get()
        self.more_info = self.orderScreen.displayBox.get("1.0", "end-1c")
        self.checkFormIntegrity()

    def checkFormIntegrity(self):
        # alt 1 check if amount of the item is missing
        if not self.order_amount:
            #alternative flow
            messageScreen = MessageScreen("Form is not filled")
            messageScreen.dispError()
        else:
            # main flow
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
