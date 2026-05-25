import tkinter as tk
from tkinter import ttk

class MemberResultSearchScreen:
    def __init__(self, parent, data, controller):
        self.controller = controller
        self.data = data 
        
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame, 
            text="Search Stuff Member", 
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        self.create_results_table()

    def create_results_table(self):

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("first_name", "last_name", "specialization")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("first_name", text="First Name")
        self.tree.heading("last_name", text="Last Name")
        self.tree.heading("specialization", text="Property")

        self.tree.column("first_name", width=150, anchor="w")
        self.tree.column("last_name", width=150, anchor="w")
        self.tree.column("specialization", width=200, anchor="w")

        self.tree.bind("<Double-1>", self.getResponse)
        self.tree.pack(side="left", fill="both", expand=True)

        self.display_data()


    def display_data(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        display_list = [self.data] if isinstance(self.data, dict) else self.data

        for item in self.data:
            row_values = (
                item.get('first_name', ''),
                item.get('last_name', ''),
                item.get('specialization', ''),
                item.get('id', ''),
                item.get('phone_number',''),
                item.get('hospital_branch',''),
                item.get('email',''))

            self.tree.insert("", "end", values=row_values)
            

    def getResponse(self, event):
        member_item = self.tree.focus() 
        if not member_item:
            return

        values = self.tree.item(member_item, 'values') 
        if values:
            self.member_details = values

        self.main_frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemberResultSearchScreen(root)
    root.mainloop()