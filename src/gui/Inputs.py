import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

from BasicInfo import BasicInfoFrame
from IncomeInfo import IncomeInfoFrame
from AssetInfo import AssetInfoFrame

class Inputs(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)

      #self.rowconfigure(0, weight=1)
      #self.columnconfigure(0, weight=1)
      style = ttk.Style(self)
      style.configure('lefttab.TNotebook', tabposition='ws')
      
      tabControl = ttk.Notebook(self, style='lefttab.TNotebook')

      self.Basic_tab = BasicInfoFrame(tabControl)
      self.Income_tab = IncomeInfoFrame(tabControl)
      Expense_tab = ttk.Frame(tabControl)
      self.Asset_tab = AssetInfoFrame(tabControl, self.Basic_tab)
      Global_tab = ttk.Frame(tabControl)

      tabControl.add(self.Basic_tab, text="Basic Info")
      tabControl.add(self.Income_tab, text="Income")
      tabControl.add(Expense_tab, text="Expenses")
      tabControl.add(self.Asset_tab, text="Assets")
      tabControl.add(Global_tab, text="Global Variables")

      tabControl.grid(row=0, column=0, sticky='nsew') #.pack(expand=1, fill='both')

      tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)

  def submit(self):
      name=self.tk_name.get()

  def on_tab_change(self, event):
      if self.Basic_tab.status.current()==1:  #married
         self.Asset_tab.show_spouse_frame()
      elif self.Basic_tab.status.current()==0:
         self.Asset_tab.hide_spouse_frame()
