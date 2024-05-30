import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry


class IncomeInfoFrame(tk.Frame):
  def __init__(self, parent, BasicInfo):
      tk.Frame.__init__(self, parent)
      
      self.BasicInfo=BasicInfo

      self.tk_name=tk.StringVar()
      self.tk_age=tk.IntVar()
      self.tk_retirement_age=tk.IntVar()
      self.tk_lifespan=tk.IntVar()
      self.tk_lifespan.set(90)  #set default lifespan to 90

      _row=0
      tk.Label(self, text="Client Information").grid(row=_row, column=0, columnspan=2, sticky='w')
      
      _row+=1
      tk.Label(self, text="IRA:").grid(row=_row, column=0)
      tk.Entry(self, textvariable=self.tk_name).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Roth IRA:").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_age, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Taxable:").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_retirement_age, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Lifespan:").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_lifespan, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      
      _row+=1
      ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=_row, column=0, columnspan=2, sticky="ew")
      
      _row+=1
      self.spouse_frame_row=_row
      self.spouse_frame=IncomeInfoSpouseFrame(self)

  def show_spouse_frame(self):
      self.spouse_frame.grid(row=self.spouse_frame_row, column=0, columnspan=2)
      
  def hide_spouse_frame(self):
      self.spouse_frame

class IncomeInfoSpouseFrame(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)

      self.tk_name=tk.StringVar()
      self.tk_age=tk.IntVar()
      self.tk_retirement_age=tk.IntVar()
      self.tk_lifespan=tk.IntVar()  # lifespan in age (90)
      self.tk_lifespan.set("90")

      _row=0
      tk.Label(self, text="Spouse Income Information").grid(row=_row, column=0, columnspan=2, sticky='w')
      
      _row+=1
      tk.Label(self, text="IRA:").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_age, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Roth IRA:").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_lifespan, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Taxable (Regular):").grid(row=_row, column=0)
      IntegerEntry(self, length=7, textvariable=self.tk_lifespan, width=7).grid(row=_row, column=1, sticky='w')