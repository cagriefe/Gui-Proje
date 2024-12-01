import tkinter as tk 
from gui import FinanceApp
#entry point of the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()