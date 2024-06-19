from datetime import date

from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
)

# from PyQt6.QtGui import QStandardItemModel

from libs.DataTable import DataElement, DataTable
from libs.RequiredMinimalDistributions import RMD
from libs.EnumTypes import AccountType
from libs.FederalTax import FederalTax

from imports.Import import Import


class Forecast:
    def __init__(self, xml_file, begin_year: int = 2024):
        with open(xml_file, "r") as fp:
            xml = fp.read()

        _i = Import(xml)
        self._vars = _i.get_data()
        self._begin_year = begin_year

        self._end_year = begin_year + self._vars["GlobalVars"].YearsToForecast
        self._federal_tax_status = self._vars["GlobalVars"].FederalTaxStatus

    def execute(self):
        _person1 = self._vars["Persons"]["1"]
        _person2 = self._vars["Persons"]["2"]

        _data = []
        _rmd = RMD(_person1, _person2)
        for _year in range(self._begin_year, self._end_year + 1):
            _data.append(DataElement("Header", "Year", _year, "%s" % _year))

            _age1 = _person1.calc_age_by_year(_year)
            if _person2 is not None:
                _age2 = _person2.calc_age_by_year(_year)
                _data.append(
                    DataElement("Header", "Age", _year, "%s/%s" % (_age1, _age2))
                )
            else:
                _data.append(DataElement("Header", "Age", _year, "%s" % (_age1)))

            _income_total = 0
            for _src in self._vars["IncomeSources"]:
                _income = _src.calc_balance_by_year(_year)
                _data.append(DataElement("Income", _src.Name, _year, _income))

                _income_total += _income  # _src.calc_income_by_year(_year)
            _data.append(DataElement("Income", "Total", _year, _income_total))

            # federal taxes
            _ft = FederalTax(self._federal_tax_status, 2024)
            _taxable_income = max(_income_total - _ft.StandardDeduction, 0)
            _taxes = _ft.calc_taxes(_taxable_income)
            _data.append(DataElement("Taxes", "Federal Taxes", _year, _taxes))

            _expense_total = 0
            for _src in self._vars["Expenses"]:
                _expense = _src.calc_balance_by_year(_year)
                _data.append(DataElement("Expense", _src.Name, _year, _expense))

                _expense_total += _expense
            _data.append(DataElement("Expense", "Total", _year, _expense_total))

            _cash_flow = _income_total - _expense_total - _taxes
            _data.append(DataElement("Cash Flow", "Total", _year, _cash_flow))
            # TODO: if _income - _expense is negative, we need to pull resources from savings...

            if _cash_flow < 0:
                # we need to pull money from Assets..
                # define a new class that takes care of this logic, etc
                pass

            _total = 0
            _ira_total = 0
            for _src in self._vars["Assets"]:
                _balance = _src.calc_balance_by_year(_year)
                _data.append(DataElement("Asset", _src.Name, _year, _balance))
                if _src.Type == AccountType.TaxDeferred:
                    _ira_total += _balance

                _total += _balance

            _rmd_pct = _rmd.calc(date(_year, 12, 31))
            _data.append(DataElement("Asset", "RMD %", _year, "%3.2f%%" % _rmd_pct))
            _data.append(
                DataElement("Asset", "RMD", _year, int(_rmd_pct / 100.0 * _ira_total))
            )
            _data.append(DataElement("Asset", "Total", _year, _total))

        _dt = DataTable(BeginYear=self._begin_year, EndYear=self._end_year, Data=_data)
        return _dt


class App(QMainWindow):
    def __init__(self, datatable):
        super().__init__()
        self.title = "PyQt5 - QTableWidget"
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table = QTableWidget()
        self.createTable(datatable)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    # Create table
    def createTable(self, datatable):
        _header, _data = datatable.get_data_sheet()

        self.table.setRowCount(len(_data))
        self.table.setColumnCount(len(_data[0]))

        _i = 0
        for _row in _data:
            _j = 0
            for _col in _row:
                # print(_i, _j, _col)
                self.table.setItem(_i, _j, QTableWidgetItem(_col))
                _j += 1
            _i += 1

        # have to put data in table before setting the header, (or header won't display)
        self.table.setHorizontalHeaderLabels(_header)
        # Table will fit the screen horizontally
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    _f = Forecast("../tests/TestCases/JohnJaneDoe.xml")
    # _f = Forecast("../tests/TestCases/ChuckJaneSmith.xml")
    _dt = _f.execute()

    app = QApplication(sys.argv)
    w = App(_dt)
    w.show()
    sys.exit(app.exec())
