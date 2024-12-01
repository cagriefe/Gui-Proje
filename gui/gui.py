import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import cursor, conn

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.create_main_window()

    def create_main_window(self):
        self.clear_window()
        tk.Label(self.root, text="Personal Finance Manager", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.root, text="Add Income", command=self.add_income_window, width=20).pack(pady=5)
        tk.Button(self.root, text="Add Expense", command=self.add_expense_window, width=20).pack(pady=5)
        tk.Button(self.root, text="View Transactions", command=self.view_transactions_window, width=20).pack(pady=5)
        tk.Button(self.root, text="Generate Reports", command=self.generate_reports_window, width=20).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit, width=20).pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_income_window(self):
        self.clear_window()
        tk.Label(self.root, text="Add Income", font=("Helvetica", 14)).pack(pady=10)
        self.transaction_form('Income')

    def add_expense_window(self):
        self.clear_window()
        tk.Label(self.root, text="Add Expense", font=("Helvetica", 14)).pack(pady=10)
        self.transaction_form('Expense')

    def transaction_form(self, trans_type):
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.description_var = tk.StringVar()

        tk.Label(self.root, text="Amount:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.amount_var).pack(pady=5)
        tk.Label(self.root, text="Category:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.category_var).pack(pady=5)
        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.date_var).pack(pady=5)
        tk.Label(self.root, text="Description:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.description_var).pack(pady=5)
        tk.Button(self.root, text=f"Add {trans_type}", command=lambda: self.add_transaction(trans_type)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_window).pack(pady=10)

    def add_transaction(self, trans_type):
        amount = self.amount_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        description = self.description_var.get()

        if not amount or not category or not date:
            messagebox.showerror("Input Error", "All fields except description are required.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return

        cursor.execute('''
            INSERT INTO transactions (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (trans_type, amount, category, date, description))
        conn.commit()
        messagebox.showinfo("Success", f"{trans_type} added successfully.")
        self.create_main_window()

    def view_transactions_window(self):
        # Implementation for viewing transactions
        pass

    def generate_reports_window(self):
        # Implementation for generating reports
        pass