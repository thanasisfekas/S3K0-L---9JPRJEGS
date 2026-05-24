import tkinter as tk
from tkinter import messagebox

class NotFoundMemberScreen:
    def __init__(self):
        self.displayMessage()

    def displayMessage(self):
        messagebox.showinfo("Warning!", "Staff Member not found. \n Try again...")
        return 

class ShiftAvailabilityFailureScreen:
    def __init__(self, message):
        self.message = message
        self.displayMessage()
        
    def displayMessage(self):
        messagebox.showinfo("Warning!", self.message)
        return

class ShiftBoundariesFailureScreen:
    def __init__(self, message):
        self.message = message
        self.displayMessage()
        
    def displayMessage(self):
        messagebox.showinfo("Warning, Violation of Boundaries!", self.message)
        return

class SuccessRegistrationShiftScreen:
    def __init__(self):
        self.displayMessage()
    
    def displayMessage(self):
        messagebox.showinfo("Success!", "Shift registered successfully!")
        return