import os
import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Surgery_Appoint.Screens.surgery_request_screen import SurgeryRequestScreen
from surgery_search_controller import SurgerySearchController
from data_paths import data_path


class SurgeryRequestController:
    def __init__(self, root, on_back_click, search_controller):
        self.root = root
        self.on_back_click = on_back_click
        self.search_controller = search_controller

        self.csv_path = data_path("surgery_requests.csv")

    def get_surgery_requests(self):
        """ Safely reads surgical data rows from your final_billing layout reference files """
        if not os.path.exists(self.csv_path):
            return []

        try:
            df = pd.read_csv(self.csv_path)
            # Flatten rows out into clean string tuples matching your display table format
            return [tuple(x) for x in df.to_numpy()]
        except Exception as e:
            print(f"Error querying surgery requests layout columns: {e}")
            return []

    def display_surgery_requests(self):
        """ Clears visual widgets and displays the main list queue screen """
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initializes screen passing self as controller injection reference
        return SurgeryRequestScreen(
            root=self.root,
            controller=self,
            on_back_click=self.on_back_click
        )

    def display_surgery_form(self, request_id, specialty_needed):
        print(f"[Bridge]: Forwarding execution to SurgerySearchController...")

        # DIRECT CONNECTION: This immediately changes your screen to the doctor view!
        self.search_controller.display_doctors(request_id, specialty_needed)


def go_back_dashboard():
    """Fallback navigation loop when clicking the 'Back' button"""
    print("[Navigation]: Returning safely back to Main System Dashboard Hub...")
    root.quit()

if __name__ == "__main__":
    # 1. Initialize the master window container
    root = tk.Tk()
    root.title("Healthcare Administrative Management System")
    root.geometry("900x600")

    # 2. Configure a basic clean theme structure style
    style = ttk.Style()
    style.theme_use("clam")

    # 3. Instantiate the controller and pass down root + back callback parameters
    #controller = SurgeryRequestController(root=root, on_back_click=go_back_dashboard)

    # 4. Clear frames and render the request queue treeview dashboard layout
    #controller.display_surgery_requests()

    search_ctrl = SurgerySearchController(root=root, on_back_click=None)

    # 2. Instantiate the Request Controller and give it the search_ctrl instance
    request_ctrl = SurgeryRequestController(root=root, on_back_click=go_back_dashboard, search_controller=search_ctrl)

    search_ctrl.on_back_click = request_ctrl.display_surgery_requests

    request_ctrl.display_surgery_requests()
    # 5. Drop into the active runtime window main loop
    root.mainloop()
