import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize Database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT
    )
''')
conn.commit()

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

        tk.Button(self.root, text="Submit", command=lambda: self.submit_transaction(trans_type)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_window).pack(pady=5)

    def submit_transaction(self, trans_type):
        amount = self.amount_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        description = self.description_var.get()

        # Data Validation
        if not amount or not category or not date:
            messagebox.showerror("Validation Error", "Please fill all required fields.")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid positive number for amount.")
            return
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid date in YYYY-MM-DD format.")
            return

        # Insert into Database
        cursor.execute('''
            INSERT INTO transactions (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (trans_type, amount, category, date, description))
        conn.commit()
        messagebox.showinfo("Success", f"{trans_type} added successfully!")
        self.create_main_window()

    def view_transactions_window(self):
        self.clear_window()
        tk.Label(self.root, text="Transactions", font=("Helvetica", 14)).pack(pady=10)

        cols = ('ID', 'Type', 'Amount', 'Category', 'Date', 'Description')
        self.listBox = ttk.Treeview(self.root, columns=cols, show='headings')

        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col, minwidth=0, width=100)

        self.load_transactions()
        self.listBox.pack(pady=10)

        tk.Button(self.root, text="Edit Transaction", command=self.edit_transaction_window).pack(pady=5)
        tk.Button(self.root, text="Delete Transaction", command=self.delete_transaction).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_window).pack(pady=5)

    def load_transactions(self):
        for row in self.listBox.get_children():
            self.listBox.delete(row)
        cursor.execute("SELECT * FROM transactions")
        for transaction in cursor.fetchall():
            self.listBox.insert("", "end", values=transaction)

    def edit_transaction_window(self):
        selected_item = self.listBox.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a transaction to edit.")
            return
        values = self.listBox.item(selected_item, 'values')
        trans_id = values[0]

        self.clear_window()
        tk.Label(self.root, text="Edit Transaction", font=("Helvetica", 14)).pack(pady=10)

        self.amount_var = tk.StringVar(value=values[2])
        self.category_var = tk.StringVar(value=values[3])
        self.date_var = tk.StringVar(value=values[4])
        self.description_var = tk.StringVar(value=values[5])

        tk.Label(self.root, text="Amount:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.amount_var).pack(pady=5)

        tk.Label(self.root, text="Category:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.category_var).pack(pady=5)

        tk.Label(self.root, text="Date (YYYY-MM-DD):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.date_var).pack(pady=5)

        tk.Label(self.root, text="Description:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.description_var).pack(pady=5)

        tk.Button(self.root, text="Update", command=lambda: self.update_transaction(trans_id)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.view_transactions_window).pack(pady=5)

    def update_transaction(self, trans_id):
        amount = self.amount_var.get()
        category = self.category_var.get()
        date = self.date_var.get()
        description = self.description_var.get()

        # Data Validation
        if not amount or not category or not date:
            messagebox.showerror("Validation Error", "Please fill all required fields.")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid positive number for amount.")
            return
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid date in YYYY-MM-DD format.")
            return

        # Update Database
        cursor.execute('''
            UPDATE transactions
            SET amount = ?, category = ?, date = ?, description = ?
            WHERE id = ?
        ''', (amount, category, date, description, trans_id))
        conn.commit()
        messagebox.showinfo("Success", "Transaction updated successfully!")
        self.view_transactions_window()

    def delete_transaction(self):
        selected_item = self.listBox.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a transaction to delete.")
            return
        values = self.listBox.item(selected_item, 'values')
        trans_id = values[0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")
        if confirm:
            cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
            conn.commit()
            self.load_transactions()
            messagebox.showinfo("Success", "Transaction deleted successfully!")

    def generate_reports_window(self):
        self.clear_window()
        tk.Label(self.root, text="Generate Reports", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Income vs Expenses", command=self.plot_income_vs_expenses).pack(pady=5)
        tk.Button(self.root, text="Expenses by Category", command=self.plot_expenses_by_category).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_window).pack(pady=20)

    def plot_income_vs_expenses(self):
        cursor.execute('''
            SELECT date, SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS expense
            FROM transactions GROUP BY date ORDER BY date
        ''')
        data = cursor.fetchall()
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
        income = [row[1] for row in data]
        expense = [row[2] for row in data]

        plt.figure(figsize=(10,5))
        plt.plot(dates, income, label='Income', marker='o')
        plt.plot(dates, expense, label='Expenses', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Income vs Expenses Over Time')
        plt.legend()
        plt.show()

    def plot_expenses_by_category(self):
        cursor.execute('''
            SELECT category, SUM(amount) FROM transactions
            WHERE type = 'Expense' GROUP BY category
        ''')
        data = cursor.fetchall()
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(8,8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.show()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
    conn.close()

if __name__ == '__main__':
    main()
