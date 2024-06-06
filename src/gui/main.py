import tkinter as tk
from tkinter import ttk

from BasicInfo import BasicInfoFrame
from IncomeInfo import IncomeInfoFrame
from MenuBar import MenuBar
from Inputs import Inputs
from Logs import Logs

class App(tk.Tk):
  def __init__(self):
      tk.Tk.__init__(self)

      self.title("Wealth Manager")
      self.geometry("800x600")

      self.menubar=MenuBar(self)
      
      self.rowconfigure(0, weight=1)
      self.columnconfigure(0, weight=1)
      tabControl = ttk.Notebook(self)

      self.Inputs_tab = Inputs(tabControl)
      self.Analysis_tab = ttk.Frame(tabControl)
      self.logs_tab=Logs(tabControl)

      tabControl.add(self.Inputs_tab, text="Inputs")
      tabControl.add(self.Analysis_tab, text="Analysis")
      tabControl.add(self.logs_tab, text="Logs")

      tabControl.grid(row=0, column=0, sticky='nsew') #.pack(expand=1, fill='both')

      tabControl.bind("<<NotebookTabChanged>>", self.on_tab_change)
      
      #tk.Button(self, text="Submit", command=self.submit).pack()

  def submit(self):
      name=self.tk_name.get()
      print(name)

  def on_tab_change(self, event):
      pass
      #tab=event.widget.tab('current')['text']
      #if self.Basic_tab.status.current()==1:  #married
      #   if tab=="Income":
      #      self.Income_tab.show_spouse_frame()
      #elif self.Basic_tab.status==0:
      #   if tab == "Income":
      #      self.Income_tab.hide_spouse_frame()

    
if __name__ == '__main__':
   _app=App()
   _app.mainloop()