import tkinter as tk
from tkinter import ttk, filedialog

class MenuBar:
  def __init__(self, parent):

      self.parent=parent
      menubar=tk.Menu(parent)
      filemenu = tk.Menu(menubar, tearoff=0)
      filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.file_new)
      filemenu.add_command(label="Open", command=self.openfilename)
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=parent.destroy)
      menubar.add_cascade(label="File", menu=filemenu)

      helpmenu = tk.Menu(menubar, tearoff=0)
      helpmenu.add_command(label="About", command=self.help_about)
      menubar.add_cascade(label="Help", menu=helpmenu)
      
      parent.config(menu=menubar)
         
  def openfilename(self):
      _filename=filedialog.askopenfilename(filetypes=(("XML Files", "*.xml"),))
      if _filename:
         print(Path(_filename).read_bytes())
                  
  def file_new(self):
      pass

  def help_about(self):
      """brings up a dialog window displaying information about this app"""
      
      _dialog=tk.Toplevel()
      _help = tk.Frame(_dialog)
      _help.pack(fill="both", expand=True)
      
      _text = tk.Text(_help, height=10, width=40, wrap=tk.WORD)
      _text.pack()
      
      _text.insert(tk.END, "WealthMan is a financial planning application.  It is open source.")
      _text.config(state=tk.DISABLED)
      
      _dialog.transient(self.parent)
      _dialog.geometry('300x200')
      _dialog.wait_window()
      