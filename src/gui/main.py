import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

from BasicInfo import BasicInfoFrame

class App(tk.Tk):
  def __init__(self):
      tk.Tk.__init__(self)

      self.title("Wealth Manager")
      self.geometry("400x300")

      tabControl = ttk.Notebook(self)

      Basic_tab = BasicInfoFrame(tabControl)
      Income_tab = ttk.Frame(tabControl)
      Expense_tab = ttk.Frame(tabControl)
      Asset_tab = ttk.Frame(tabControl)

      tabControl.add(Basic_tab, text="Basic Info")
      tabControl.add(Income_tab, text="Income")
      tabControl.add(Expense_tab, text="Expenses")
      tabControl.add(Asset_tab, text="Assets")

      tabControl.pack(expand=1, fill='both')


if __name__ == '__main__':
   _app=App()
   _app.mainloop()
