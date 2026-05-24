import csv
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Order:
    def __init__(self, item_data , amount, more_info):
        self.amount = amount
        self.more_info = more_info
        self.name =  item_data[1]
        self.id = item_data[0]

    def getOrder(self):
        return [self.name,self.id,self.amount,self.more_info]
    
class OrderLog:
    def __init__(self, file):
        self.order_fl = file

    def generate_id(self):
        with open(self.order_fl , 'r' , newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                id = row["ORDER_ID"]
            new_id = f"O{int(id.lstrip('O')) + 1:03d}"
            return new_id

    def submitOrder(self,order):
        header = ["ORDER_ID","NAME","ID","AMOUNT","MORE_INFO"]

        fl_exist= os.path.isfile(self.order_fl)

        with open(self.order_fl,'a' , newline='') as file:
            writer = csv.writer(file)
            if not fl_exist:
                writer.writerow(header)
            writer.writerow([self.generate_id()]+order)

class Inventory:
    def __init__(self,available_inv):
        self.inventory = available_inv

    def searchInvItem(self, item_id):
        if (re.match(r"^M[0-9]+",item_id.strip())):
            med =self.inventory.iloc[0,0] 
            item_info = med[med["medicine_id"] == item_id.strip()]

            return  item_info if not item_info.empty else None 
        
        elif (re.match(r"^E[0-9]+",item_id)):
            equip = self.inventory.iloc[0,1]
            item_info = equip[equip["equipment_id"] == item_id.strip()]

            return  item_info if not item_info.empty else None 