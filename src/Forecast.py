# look at persons and see
from datetime import date
from tksheet import Sheet  #, num2alpha
import tkinter as tk

from DataTable import DataElement, DataTable
from RequiredMinimalDistributions import RMD
from EnumTypes import AccountType
from FederalTax import FederalTax

import sys
sys.path.append("xml/Import")
from Import import Import

class Forecast:
  def __init__(self, xml_file, begin_year: int = 2024):
      with open(xml_file, 'r') as fp:
         xml=fp.read()
         
      _i = Import(xml)
      self._vars = _i.get_data()
      self._begin_year = begin_year
      
      self._end_year=begin_year+self._vars["GlobalVars"].YearsToForecast
      self._federal_tax_status=self._vars["GlobalVars"].FederalTaxStatus

  def execute(self):
      _person1 = self._vars["Persons"]["1"]
      _person2 = self._vars["Persons"]["2"]
      
      _data=[]
      _rmd=RMD(_person1, _person2)
      for _year in range(self._begin_year, self._end_year+1):
          _data.append(DataElement("Header", "Year", _year, "%s" % _year))
                                                                    
          _age1=_person1.calc_age_by_year(_year)
          if _person2 is not None:
             _age2=_person2.calc_age_by_year(_year)
             _data.append(DataElement("Header", "Age", _year, "%s/%s" % (_age1, _age2)))
          else:
             _data.append(DataElement("Header", "Age", _year, "%s" % (_age1)))

          _income_total = 0
          for _src in self._vars["IncomeSources"]:
              _income = _src.calc_balance_by_year(_year)
              _data.append(DataElement("Income", _src.Name, _year, _income))
              
              _income_total += _income  # _src.calc_income_by_year(_year)
          _data.append(DataElement("Income", "Total", _year, _income_total))    
          
          #federal taxes
          _ft=FederalTax(self._federal_tax_status, 2024)
          _taxable_income=max(_income_total - _ft.StandardDeduction, 0)
          _taxes=_ft.calc_taxes(_taxable_income)
          _data.append(DataElement("Taxes", "Federal Taxes", _year, _taxes))
          
          _expense_total = 0
          for _src in self._vars["Expenses"]:
              _expense = _src.calc_balance_by_year(_year)
              _data.append(DataElement("Expense", _src.Name, _year, _expense))
          
              _expense_total += _expense
          _data.append(DataElement("Expense", "Total", _year, _expense_total))
          
          _cash_flow=_income_total - _expense_total - _taxes
          _data.append(DataElement("Cash Flow", "Total", _year, _cash_flow))
          #TODO: if _income - _expense is negative, we need to pull resources from savings...

          if _cash_flow < 0:
              #we need to pull money from Assets..
              #define a new class that takes care of this logic, etc
              pass

          _total=0
          _ira_total=0
          for _src in self._vars["Assets"]:
              _balance = _src.calc_balance_by_year(_year)
              _data.append(DataElement("Asset", _src.Name, _year, _balance))
              if _src.Type == AccountType.TaxDeferred:
                  _ira_total+=_balance
            
              _total+=_balance
          
          _rmd_pct=_rmd.calc(date(_year, 12, 31))
          _data.append(DataElement("Asset", "RMD %", _year, "%3.2f%%" % _rmd_pct))
          _data.append(DataElement("Asset", "RMD", _year, int(_rmd_pct/100.0 * _ira_total)))
          _data.append(DataElement("Asset", "Total", _year, _total))
          
          
      _dt=DataTable(BeginYear=self._begin_year, EndYear=self._end_year, Data=_data) 
      return _dt
    
class demo(tk.Tk):
    def __init__(self, datatable):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        _header, _data=datatable.get_data_sheet()
        
        # create an instance of Sheet()
        self.sheet = Sheet(
            # set the Sheets parent widget
            self.frame,
            # optional: set the Sheets data at initialization
            #data=[[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(20)] for r in range(100)],
            theme="light blue",
            height=520,
            width=1000,
            show_header=True,
            show_row_index=False,
            headers=_header,
            align="e",
            header_font=("Arial", 11, "bold")
        )
        
        # add some new commands to the in-built right click menu
        # setting data

        self.sheet.set_sheet_data(_data)

        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")


if __name__ == "__main__":
   _f = Forecast("../tests/TestCases/JohnJaneDoe.xml")
   #_f = Forecast("../tests/TestCases/ChuckJaneSmith.xml")
   _dt=_f.execute()
   
   app=demo(_dt)
   app.mainloop()