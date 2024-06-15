import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry


class AssetInfoFrame(tk.Frame):
  def __init__(self, parent, BasicInfo):
      tk.Frame.__init__(self, parent)
      
      self.BasicInfo=BasicInfo

      self.tk_ira=tk.IntVar()
      self.tk_roth=tk.IntVar()
      self.tk_taxable=tk.IntVar()
      
      _row=0
      tk.Label(self, text="Client Information").grid(row=_row, column=0, columnspan=2, sticky='w')
      
      _row+=1
      tk.Label(self, text="IRA:").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_ira, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Roth IRA:").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_roth, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Taxable (Regular):").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_taxable, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=_row, column=0, columnspan=2, sticky="ew")
      
      _row+=1
      self.spouse_frame_row=_row
      self.spouse_frame=AssetInfoSpouseFrame(self)

  def show_spouse_frame(self):
      self.spouse_frame.grid(row=self.spouse_frame_row, column=0, columnspan=2)
      
  def hide_spouse_frame(self):
      self.spouse_frame.grid_forget()

class AssetInfoSpouseFrame(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)

      self.tk_ira=tk.IntVar()
      self.tk_roth=tk.IntVar()
      self.tk_taxable=tk.IntVar()
      
      _row=0
      tk.Label(self, text="Spouse Asset Information").grid(row=_row, column=0, columnspan=2, sticky='w')
      
      _row+=1
      tk.Label(self, text="IRA:").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_ira, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Roth IRA:").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_roth, width=7).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Taxable (Regular):").grid(row=_row, column=0, sticky='w')
      IntegerEntry(self, length=7, textvariable=self.tk_taxable, width=7).grid(row=_row, column=1, sticky='w')