import customtkinter as ctk
import sys
import os
 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from uc_3.controllers import InvMgMainMenuController

if __name__=="__main__":
    app = ctk.CTk()
    app.geometry("1000x750")
    # init main menu controller
    search = InvMgMainMenuController(app)
    app.mainloop()
