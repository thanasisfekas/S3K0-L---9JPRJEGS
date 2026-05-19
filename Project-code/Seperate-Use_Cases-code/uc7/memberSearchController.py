from memberSearchScreen import MemberSearchScreen
from readerHandlers import HospitalStaffReader
from memberResultSearchScreen import MemberResultSearchScreen
from memberDetailsScreen import MemberDetailsScreen
from shiftFormController import ShiftFormController
import tkinter as tk
from tkinter import messagebox

class MemberSearchController:
    def __init__(self,root):
        self.root = root
        self.current_screen = None
        self.HospitalStaff = HospitalStaffReader()
        self.input_data = {}
        self.current_controller = None
    
    def displaySearchScreen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.current_screen = MemberSearchScreen(self.root, controller = self)

    def checkInput(self, input):
        input = input.strip()
    
        if  input.replace(" ", "").isalpha() and " " in input:
            name, surname = input.lower().split(" ", 1)
            return True , name, surname

        else:
            messagebox.showwarning("Warning!", "Non Valid Input! Re-enter Name and Surname.")
            return False, None , None


    def searchMember(self):
        flag = False
        name = None
        surname = None 

        input = self.current_screen.getInput()

        if not input:
            messagebox.showwarning("Warning!", "Enter Name and Surname.")
            return None

        flag, name, surname = self.checkInput(input)

        if flag :
            results = self.HospitalStaff.find_by_name_surname(name, surname)
            if results:
                self.displaySearchResults(results)

            else:
                messagebox.showinfo("Warning!", "Staff Member not found. \n Try again...")   
        else:
            messagebox.showerror("Error!", "Non valid data.")
        
            

    def displaySearchResults(self, results):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        processed_results = []

        for item in results:
            if isinstance(item, dict):
                member_dict = {
                    'id': item.get('id'),
                    'first_name': item.get('first_name'),
                    'last_name': item.get('last_name'),
                    'specialization': item.get('specialization'),
                    'phone_number': item.get('phone_number'),
                    'hospital_branch': item.get('hospital_branch'),
                    'email':item.get('email')}


            else:
                member_dict = {
                    'id':item[0],
                    'first_name': item[1],
                    'last_name': item[2],
                    'specialization': item[3],
                    'phone_number':item[4],
                    'hospital_branch':item[5],
                    'email':item[6]}

            processed_results.append(member_dict)

        self.current_screen = MemberResultSearchScreen(self.root, processed_results, self)
        self.current_screen.main_frame.pack(fill="both", expand=True)
        self.root.wait_window(self.current_screen.main_frame)

        member_details = getattr(self.current_screen, "member_details", None)
        print(member_details)

        self.displayMemberDetails(member_details)



    def displayMemberDetails(self, details):
        self.current_screen = MemberDetailsScreen(self.root, details, self)
        self.input_data = details

    def createShiftController(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.current_controller = ShiftFormController(self.root, self.input_data, self)
    


if __name__ == "__main__":
    root = tk.Tk()
    controller = MemberSearchController(root)
    controller.displaySearchScreen()
    root.mainloop() 

    










    
