

from tkinter import *
from tkinter import ttk

import sys
sys.path.append("guihelpers")
from IntegerEntry import IntegerEntry

def on_select(event):
    selected_index=_status.current()
    if selected_index >= 0:
       print(f'Selected object: {selected_index}')

  
_app=Tk()
_app.title("Wealth Manager")

tabControl = ttk.Notebook(_app)

Basic_tab = ttk.Frame(tabControl)
Income_tab = ttk.Frame(tabControl)
Expense_tab = ttk.Frame(tabControl)
Asset_tab = ttk.Frame(tabControl)

tabControl.add(Basic_tab, text="Basic Info")
tabControl.add(Income_tab, text="Income")
tabControl.add(Expense_tab, text="Expenses")
tabControl.add(Asset_tab, text="Assets")

tabControl.pack(expand=1, fill='both')

tk_name1=StringVar()
tk_age1=IntVar()

def submit():
    name=tk_name1.get()
    print(name)

#_frm=ttk.Frame(_app, padding=10)
#_frm.grid()

ttk.Label(Basic_tab, text="Marriage Status:").grid(row=0, column=0)
_status=ttk.Combobox(Basic_tab, values=['Single', 'Married'])
_status.grid(row=0, column=1)
_status.bind("<<ComboboxSelected>>", on_select)


ttk.Label(Basic_tab, text="Person 1 Name").grid(row=1, column=0)
ttk.Entry(Basic_tab, textvariable=tk_name1).grid(row=1, column=1)

ttk.Label(Basic_tab, text="Person 1 Age:").grid(row=1, column=0)
IntegerEntry(Basic_tab, length=2).grid(row=1, column=1)

Button(Basic_tab, text="Submit", command=submit).grid(row=2, column=1)
_app.mainloop()