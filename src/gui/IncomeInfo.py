import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk, font

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry
from FloatEntry import FloatEntry

class BoldLabel(tk.Label):
  def __init__(self, master=None, **kwargs):
      super().__init__(master, **kwargs)
      bold_font = font.Font(self, self.cget("font"))
      bold_font.configure(weight="bold")
      self.configure(font=bold_font)

class IncomeInfoFrame(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)
      
      self.tk_name=[] #tk.IntVar()
      self.tk_amount=[] #tk.IntVar()
      self.tk_pct_change=[] #taxable=tk.IntVar()
      self.tk_start_age=[]
      self.tk_end_age=[]
      
      tk.Button(self, text="Add Row", command=self.add_row).grid(row=0, column=0, sticky='n')
      
      ttk.Separator().grid(row=2, sticky='ew')
      
      tk.Label(self, text="Income Information").grid(row=3, column=0, columnspan=2, sticky='w')
      
      ttk.Separator().grid(row=4, sticky='ew')
      
      BoldLabel(self, text="Name:").grid(row=5, column=0, sticky='w')
      BoldLabel(self, text="Annual\nAmount").grid(row=5, column=1, sticky='w')
      BoldLabel(self, text="Annual %\nChange").grid(row=5, column=2, sticky='w')
      BoldLabel(self, text="Start\nAge").grid(row=5, column=3, sticky='w')
      BoldLabel(self, text="End\nAge").grid(row=5, column=4, sticky='w')

      self.length=0
      self.add_row()


  def add_row(self):    
      self.tk_name.append(tk.StringVar())
      self.tk_amount.append(tk.IntVar())
      self.tk_pct_change.append(tk.IntVar())
      self.tk_start_age.append(tk.IntVar())
      self.tk_end_age.append(tk.IntVar())
      
      _row=self.length+6
      tk.Entry(self, textvariable=self.tk_name[self.length]).grid(row=_row, column=0)
      IntegerEntry(self, length=5, textvariable=self.tk_amount[self.length], width=5).grid(row=_row, column=1)
      FloatEntry(self, length=3, textvariable=self.tk_pct_change[self.length], width=3).grid(row=_row, column=2)
      IntegerEntry(self, length=2, textvariable=self.tk_start_age[self.length], width=2).grid(row=_row, column=3)
      IntegerEntry(self, length=2, textvariable=self.tk_end_age[self.length], width=2).grid(row=_row, column=4)
      
      self.length+=1