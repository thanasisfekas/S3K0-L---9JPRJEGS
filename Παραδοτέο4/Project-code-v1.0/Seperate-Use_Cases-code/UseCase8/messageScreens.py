from tkinter import messagebox
import tkinter as tk

class PrescriptionSearchFailureScreen:
    def __init__(self):
        self.displayMessage()

    def displayMessage(self):
        messagebox.showerror("Error!", "There aren't any prescriptions for this patient \nTry again...")
        return 

class DrugShortageScreen:
    def __init__(self, message):
        self.message = message
        self.displayMessage()

    def displayMessage(self):
        messagebox.showerror("Error!", self.message)
        return 

class SuccessScreen:
    def __init__(self):
        self.displayMessage()

    def displayMessage(self):
        messagebox.showinfo("Prescription Completed!", "All medicines in this prescription have been successfully processed.")
        return 
