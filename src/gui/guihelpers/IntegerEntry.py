from tkinter import *
from tkinter import ttk

class IntegerEntry(ttk.Entry):
  def __init__(self, master=None, length=None, **kwargs):
      if length is None:
         self.length=99
      else:
         self.length=length
            
      self.kwargs_textvariable=None
      if 'textvariable' in kwargs:
         self.kwargs_textvariable=kwargs['textvariable']
         del kwargs['textvariable']
            
      self.var = StringVar(master)
      ttk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
      self.var.trace('w', self.validate)

  def validate(self, *args):
      #if not self.var.get().isdigit():
      corrected = ''.join(filter(str.isdigit, self.var.get()))
      corrected = corrected[: min(len(corrected), self.length)]
      #print(corrected)
      self.var.set(corrected)
      if self.kwargs_textvariable is not None:
         self.kwargs_textvariable.set(corrected)