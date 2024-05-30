import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry


class BasicInfoFrame(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)

      self.tk_name=tk.StringVar()
      self.tk_age=tk.IntVar()
      self.tk_retirement_age=tk.IntVar()
      self.tk_lifespan=tk.IntVar()
      self.tk_lifespan.set(90)  #set default lifespan to 90

      _row=0
      tk.Label(self, text="Name:").grid(row=_row, column=0)
      tk.Entry(self, textvariable=self.tk_name).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Age:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_age, width=3).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Retirement Age:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_retirement_age, width=3).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Lifespan:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_lifespan, width=3).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Marriage Status:").grid(row=_row, column=0)
      self.status=ttk.Combobox(self, values=['Single', 'Married'])
      self.status.grid(row=_row, column=1)
      self.status.bind("<<ComboboxSelected>>", self.on_select)

      _row+=1
      ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=_row, column=0, columnspan=2, sticky="ew")
      
      _row+=1
      self.spouse_frame_row=_row
      self.spouse_frame=BasicInfoSpouseFrame(self)

      _row+=1
      tk.Button(self, text="Submit", command=self.submit).grid(row=_row, column=1)

  def on_select(self, event):
      selected_index=self.status.current()
      print(selected_index)
      if selected_index == 1:
         if 1: #not self.winfo_manager():
            print("grid")
            self.spouse_frame.grid(row=self.spouse_frame_row, column=0, columnspan=2)
      elif selected_index == 0:
         if self.winfo_manager(): 
            self.spouse_frame.grid_forget()
       
  def submit(self):
      name=self.tk_name.get()
      print(name)


class BasicInfoSpouseFrame(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)

      self.tk_name=tk.StringVar()
      self.tk_age=tk.IntVar()
      self.tk_retirement_age=tk.IntVar()
      self.tk_lifespan=tk.IntVar()  # lifespan in age (90)
      self.tk_lifespan.set("90")

      _row=0
      tk.Label(self, text="Spouse Information").grid(row=_row, column=0, columnspan=2, sticky='w')
      
      _row+=1
      tk.Label(self, text="Name:").grid(row=_row, column=0)
      tk.Entry(self, textvariable=self.tk_name).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Age:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_age, width=3).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Retirement Age:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_lifespan, width=3).grid(row=_row, column=1, sticky='w')

      _row+=1
      tk.Label(self, text="Lifespan:").grid(row=_row, column=0)
      IntegerEntry(self, length=2, textvariable=self.tk_lifespan, width=3).grid(row=_row, column=1, sticky='w')