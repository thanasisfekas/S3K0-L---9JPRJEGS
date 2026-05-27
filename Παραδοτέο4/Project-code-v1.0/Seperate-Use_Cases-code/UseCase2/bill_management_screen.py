import tkinter as tk
from tkinter import ttk, messagebox


def apply_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", rowheight=30)


class BillManagementScreen:
    def __init__(self, root, data, on_select=None):
        self.root = root
        self.data = data
        self.on_select = on_select

        self.root.title("Bill Management")
        self.root.geometry("900x400")
        self.root.configure(bg="white")

        # ----------------------------
        # top title
        # ----------------------------
        top_frame = tk.Frame(root, bg="white")
        top_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            top_frame,
            text="Billing History",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(side="left")

        # ----------------------------
        # table
        # ----------------------------
        columns = ("date", "bill_id", "status", "amount")

        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=10
        )

        # headings
        self.tree.heading("date", text="Date ↑")
        self.tree.heading("bill_id", text="Bill ID")
        self.tree.heading("status", text="Status")
        self.tree.heading("amount", text="Final Amount")

        # widths (important!)
        self.tree.column("date", width=100)
        self.tree.column("bill_id", width=100)
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("amount", width=120, anchor="e")

        # insert rows
        for _, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=(row["bill_date"], row["bill_id"], row["payment_status"], row["amount"]))

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # ----------------------------
        # footer
        # ----------------------------
        tk.Label(root, text=f"Showing 1 to {len(self.data)} of {len(self.data)} entries", fg="gray", bg="white").pack(side="left", padx=10)

        # double click event
        self.tree.bind("<Double-1>", self._on_double_click)

    def _on_double_click(self, event):
        item_id = self.tree.focus()
        values = self.tree.item(item_id)["values"]

        if values and self.on_select:
            bill_id = values[1]
            self.on_select(bill_id)

    def showError(self, message):
        messagebox.showinfo("Info", message)