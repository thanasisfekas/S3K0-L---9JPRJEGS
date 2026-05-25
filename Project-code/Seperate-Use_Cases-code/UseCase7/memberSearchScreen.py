import tkinter as tk
from tkinter import messagebox

class MemberSearchScreen:
    def __init__(self, root, controller=None):
        self.root = root
        self.controller = controller

        self.root.title("Staff Member Search")
        self.root.geometry("600x400")
        self.root.configure(bg="#ffffff") 

        self.main_frame = tk.Frame(self.root, bg="#ffffff")
        self.main_frame.place(relx=0.5, rely=0.4, anchor="center")


        tk.Label(
            self.main_frame, 
            text="Staff Member Search", 
            font=("Segoe UI", 18, "bold"), 
            bg="#ffffff", 
            fg="#2c3e50").pack(pady=(0, 20))

       
        search_container = tk.Frame(self.main_frame, bg="#ffffff")
        search_container.pack(pady=10)

        tk.Label(
            search_container,
            text="Please insert Name/Surname.", 
            font=("Segoe UI", 10), 
            bg="#ffffff", 
            fg="#7f8c8d").pack(anchor="center", padx=5)

        self.search_entry = tk.Entry(
            search_container, 
            font=("Segoe UI", 14), 
            width=30, 
            bd=0, 
            highlightthickness=1, 
            highlightbackground="#bdc3c7")
        
        self.search_entry.pack(pady=5, ipady=8, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.perform_search()) 

       
        self.search_btn = tk.Button(
            self.main_frame, 
            text="Search", 
            font=("Segoe UI", 12, "bold"),
            bg="#3498db", 
            fg="white", 
            width=18, 
            bd=0, 
            cursor="hand2",
            activebackground="#2980b9", 
            activeforeground="white",
            command=self.controller.searchMember)
        
        self.search_btn.pack(pady=20)

       
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.configure(bg="#2980b9"))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.configure(bg="#3498db"))

    def getInput(self):
        query = self.search_entry.get().strip()
        return query

if __name__ == "__main__":
    root = tk.Tk()
    app = MemberSearchScreen(root)
    root.mainloop()