import tkinter as tk
from tkinter import ttk

from BasicInfo import BasicInfoFrame
from IncomeInfo import IncomeInfoFrame
from MenuBar import MenuBar

class App(tk.Tk):
  def __init__(self):
      tk.Tk.__init__(self)

      self.title("Wealth Manager")
      self.geometry("800x600")

      self.menubar=MenuBar(self)
      
      tabControl = ttk.Notebook(self)

      self.Basic_tab = BasicInfoFrame(tabControl)
      self.Income_tab = IncomeInfoFrame(tabControl, self.Basic_tab)
      Expense_tab = ttk.Frame(tabControl)
      Asset_tab = ttk.Frame(tabControl)
      Global_tab = ttk.Frame(tabControl)

      tabControl.add(self.Basic_tab, text="Basic Info")
      tabControl.add(self.Income_tab, text="Income")
      tabControl.add(Expense_tab, text="Expenses")
      tabControl.add(Asset_tab, text="Assets")
      tabControl.add(Global_tab, text="Global Variables")

      tabControl.pack(expand=1, fill='both')

      tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
      
      tk.Button(self, text="Submit", command=self.submit).pack()

  def submit(self):
      name=self.tk_name.get()
      print(name)

  def on_tab_change(self, event):
      tab=event.widget.tab('current')['text']
      print(tab)
      print(self.Basic_tab.status.current())
      if self.Basic_tab.status.current()==1:  #married
         if tab=="Income":
            self.Income_tab.show_spouse_frame()
      elif self.Basic_tab.status==0:
         if tab == "Income":
            self.Income_tab.hide_spouse_frame()

if __name__ == '__main__':
   _app=App()
   _app.mainloop()
