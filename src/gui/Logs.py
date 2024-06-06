import tkinter as tk
import sys

class Logs(tk.Frame):
  def __init__(self, parent):
      tk.Frame.__init__(self, parent)
      
      self.log=tk.Text(self, wrap=tk.WORD)
      self.log.pack()
      
      self.log.insert(tk.END, "Python Version=%s\n" % sys.version)
      self.log.insert(tk.END, "Tkinter Version=%s\n" % tk.TkVersion)
      self.log.config(state=tk.DISABLED)
      
  def append(self, text):
      self.log.config(state=tk.ENABLED)
      self.log.insert(tk.END, text)
      self.log.config(state=tk.DISABLED)
      