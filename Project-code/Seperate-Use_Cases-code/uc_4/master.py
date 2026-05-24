import customtkinter as ctk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controllers import DoctorMainMenuController

if __name__=="__main__":
    app = ctk.CTk()
    app.geometry("1550x750")
    search = DoctorMainMenuController(app)
    app.mainloop()