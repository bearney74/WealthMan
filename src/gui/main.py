

from tkinter import *
from tkinter import ttk

def on_select(event):
    selected_index=_status.current()
    if selected_index >= 0:
       print(f'Selected object: {selected_index}')

_app=Tk()

#_frm=ttk.Frame(_app, padding=10)
#_frm.grid()
ttk.Label(_app, text="Person 1 Name").grid(column=0, row=0)
_status=ttk.Combobox(_app, values=['Single', 'Married'])
_status.grid(column=1, row=0)
_status.bind("<<ComboboxSelected>>", on_select)

_app.mainloop()
