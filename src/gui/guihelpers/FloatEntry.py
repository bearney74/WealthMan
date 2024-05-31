from tkinter import Tk, Button, Entry

class FloatEntry(Entry):
  def __init__(self, *args, **kwargs):
      self.length=None
      if 'length' in kwargs:
          self.length=kwargs['length']
          del kwargs['length']
          
      super().__init__(*args, **kwargs)
      vcmd = (self.register(self.validate),'%P')
      self.config(validate="all", validatecommand=vcmd)

  def validate(self, text):
      if self.length is not None:
         if len(text) > self.length:
             return False
      
      return (all(char in "0123456789.-" for char in text) and  # all characters are valid
              "-" not in text[1:] and # "-" is the first character or not present
              text.count(".") <= 1) # only 0 or 1 periods