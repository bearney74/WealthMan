import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

from BasicInfo import BasicInfoFrame
from IncomeInfo import IncomeInfoFrame
from AssetInfo import AssetInfoFrame

class App(tk.Tk):
  def __init__(self):
      tk.Tk.__init__(self)

      self.title("Wealth Manager")
      self.geometry("800x600")


      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)
      tabControl = ttk.Notebook(self)

      self.Basic_tab = BasicInfoFrame(tabControl)
      self.Income_tab = IncomeInfoFrame(tabControl)
      Expense_tab = ttk.Frame(tabControl)
      self.Asset_tab = AssetInfoFrame(tabControl, self.Basic_tab)
      
      tabControl.add(self.Basic_tab, text="Basic Info")
      tabControl.add(self.Income_tab, text="Income")
      tabControl.add(Expense_tab, text="Expenses")
      tabControl.add(self.Asset_tab, text="Assets")

      tabControl.grid(row=0, column=0, sticky='nsew') #.pack(expand=1, fill='both')

      tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
      
      
      #tk.Button(self, text="Submit", command=self.submit).grid(row=1, column=0)

  def submit(self):
      name=self.tk_name.get()
      #print(name)

  def on_tab_change(self, event):
      #tab=event.widget.tab('current')['text']
      #print(tab)
      #print(self.Basic_tab.status.current())
      if self.Basic_tab.status.current()==1:  #married
         self.Asset_tab.show_spouse_frame()
      elif self.Basic_tab.status.current()==0:
         self.Asset_tab.hide_spouse_frame()
          

if __name__ == '__main__':
   _app=App()
   _app.mainloop()
