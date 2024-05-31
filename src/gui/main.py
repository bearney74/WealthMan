import tkinter as tk
#from tkinter import Tk, StringVar, IntVar, Button
from tkinter import ttk

from Inputs import Inputs

class App(tk.Tk):
  def __init__(self):
      tk.Tk.__init__(self)

      self.title("Wealth Manager")
      self.geometry("800x600")

      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)
      tabControl = ttk.Notebook(self)

      self.Inputs_tab = Inputs(tabControl)
      self.Analysis_tab = ttk.Frame(tabControl)

      tabControl.add(self.Inputs_tab, text="Inputs")
      tabControl.add(self.Analysis_tab, text="Analysis")

      tabControl.grid(row=0, column=0, sticky='nsew') #.pack(expand=1, fill='both')

      #tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)

  
  
if __name__ == '__main__':
   _app=App()
   _app.mainloop()
