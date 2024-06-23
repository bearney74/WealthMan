from datetime import date

from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QStyledItemDelegate,
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor

import pickle

from libs.Account import Account
from libs.IncomeSources import IncomeSource
from libs.Expense import Expense
from libs.DataTable import DataElement, DataTable
from libs.RequiredMinimalDistributions import RMD
from libs.EnumTypes import AccountType, AmountPeriodType, FederalTaxStatusType
from libs.FederalTax import FederalTax

from libs.Person import Person

import logging

logger = logging.getLogger(__name__)


class Forecast:
    def __init__(self, xml_file, begin_year: int = 2024):
        with open(xml_file, "rb") as fp:
            dv = pickle.load(fp)

        # _i = Import(xml)
        # self._vars = _i.get_data()
        self._begin_year = begin_year

        self._client = Person(
            dv._clientName, dv._clientBirthDate, Relationship=dv._relationStatus
        )
        self._client.set_LifeExpectancy_by_age(dv._clientLifeSpanAge)
        self._client.set_Retirement_by_age(dv._clientRetirementAge)

        self._spouse = None
        if dv._relationStatus == "Married":
            self._spouse = Person(dv._spouseName, dv._spouseBirthDate)
            self._spouse.set_LifeExpectancy_by_age(dv._spouseLifeSpanAge)
            self._spouse.set_Retirement_by_age(dv._spouseRetirementAge)

        self._IncomeSources = []
        for _record in dv._incomes:
            _birthdate = self._client.BirthDate
            if _record._owner == "2":
                _birthdate = self._spouse.BirthDate

            if _record._begin_age is not None and _record._amount is not None:
                if _record._end_age is None:
                    _record._end_age = 99
                if _record._COLA is None:
                    _record._COLA = 0.0
                _is = IncomeSource(
                    _record._descr,
                    None,
                    _record._amount,
                    AmountPeriodType.Annual,
                    _record._owner,
                    BeginDate=date(
                        _birthdate.year + _record._begin_age,
                        _birthdate.month,
                        _birthdate.day,
                    ),
                    EndDate=date(
                        _birthdate.year + _record._end_age,
                        _birthdate.month,
                        _birthdate.day,
                    ),
                    Taxable=True,
                    COLA=_record._COLA,
                )

                self._IncomeSources.append(_is)
            else:
                if _record._begin_age is None:
                    logger.Error(
                        "Income Source '%s' not used since begin date not set"
                        % _record._descr
                    )
                if _record._amount is None:
                    logger.Error(
                        "Income Source '%s' not used since amount not set"
                        % _record._descr
                    )

        self._Expenses = []
        for _record in dv._expenses:
            _birthdate = self._client.BirthDate
            if _record._owner == "2":
                _birthdate = self._spouse.BirthDate

            if _record._begin_age is not None and _record._amount is not None:
                if _record._end_age is None:
                    _record._end_age = 99
                if _record._COLA is None:
                    _record._COLA = 0.0

                _e = Expense(
                    _record._descr,
                    _record._amount,
                    AmountPeriodType.Annual,
                    BeginDate=date(
                        _birthdate.year + _record._begin_age,
                        _birthdate.month,
                        _birthdate.day,
                    ),
                    EndDate=date(
                        _birthdate.year + _record._end_age,
                        _birthdate.month,
                        _birthdate.day,
                    ),
                    COLA=_record._COLA,
                )

                self._Expenses.append(_e)
            else:
                if _record._begin_age is None:
                    logger.Error(
                        "Expense '%s' not used since begin date not set"
                        % _record._descr
                    )
                if _record._amount is None:
                    logger.Error(
                        "Expense '%s' not used since amount not set" % _record._descr
                    )

        _cola = 7.0  # TODO fix me..
        self._Assets = []
        if dv._clientIRA is not None:
            self._Assets.append(
                Account(
                    "Client IRA", AccountType.TaxDeferred, "1", dv._clientIRA, _cola
                )
            )
        if dv._clientRothIRA is not None:
            self._Assets.append(
                Account(
                    "Client Roth IRA",
                    AccountType.TaxFree,
                    "1",
                    dv._clientRothIRA,
                    _cola,
                )
            )

        if dv._Regular is not None:
            self._Assets.append(
                Account("Regular Account", AccountType.Regular, "1", dv._Regular, _cola)
            )

        if dv._spouseIRA is not None:
            self._Assets.append(
                Account(
                    "Spouse IRA", AccountType.TaxDeferred, "2", dv._spouseIRA, _cola
                )
            )

        if dv._spouseRothIRA is not None:
            self._Assets.append(
                Account(
                    "Spouse Roth IRA",
                    AccountType.TaxFree,
                    "1",
                    dv._spouseRothIRA,
                    _cola,
                )
            )

        self._end_year = begin_year + dv._forecastYears
        # TODO fix me
        self._federal_tax_status = FederalTaxStatusType.MarriedJointly
        # self._federal_tax_status = self._vars["GlobalVars"].FederalTaxStatus

    def execute(self):
        _data = []
        _rmd = RMD(self._client, self._spouse)
        for _year in range(self._begin_year, self._end_year + 1):
            _data.append(DataElement("Header", "Year", _year, "%s" % _year))

            _age1 = self._client.calc_age_by_year(_year)
            if self._spouse is not None:
                _age2 = self._spouse.calc_age_by_year(_year)
                _data.append(
                    DataElement("Header", "Age", _year, "%s/%s" % (_age1, _age2))
                )
            else:
                _data.append(DataElement("Header", "Age", _year, "%s" % (_age1)))

            _income_total = 0
            for _src in self._IncomeSources:
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
            for _src in self._Expenses:
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
            for _src in self._Assets:
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


class InitialDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.nDecimals = decimals

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = (
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        try:
            text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
            if "%" in text:
                option.text = text
            else:
                number = int(text)
                if number < 0:
                    option.text = f"(${number:,d})"
                else:
                    option.text = f"${number:,d}"
        except Exception as e:
            logger.error(e)
            # print(index.model().data(index, Qt.ItemDataRole.DisplayRole))
            # pass


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
        self.table.setItemDelegate(InitialDelegate(self.table))
        self.table.setItemDelegateForColumn(0, QStyledItemDelegate(self.table))
        self.table.setItemDelegateForColumn(1, QStyledItemDelegate(self.table))
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
                _value = QTableWidgetItem(_col)
                try:
                    if _col.strip().startswith("-"):
                        # _col=int(_col)
                        # if _col < 0:
                        _value.setForeground(QBrush(QColor(255, 0, 0)))
                except Exception as e:
                    print(e)
                self.table.setItem(_i, _j, _value)
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

    _f = Forecast("../test.wmd")
    # _f = Forecast("../tests/TestCases/ChuckJaneSmith.xml")
    _dt = _f.execute()

    app = QApplication(sys.argv)
    w = App(_dt)
    w.show()
    sys.exit(app.exec())
