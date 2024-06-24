from datetime import datetime, date
#from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from libs.Account import Account
from libs.IncomeSources import IncomeSource
from libs.Expense import Expense
from libs.TableData import DataElement, TableData
from libs.RequiredMinimalDistributions import RMD
from libs.EnumTypes import AccountType, AmountPeriodType, FederalTaxStatusType
from libs.FederalTax import FederalTax

# from imports.Import import Import
from libs.Person import Person
from libs.DataVariables import DataVariables
from libs.WithdrawStrategy import WithdrawStrategy


import logging
logger = logging.getLogger(__name__)

class ProjectionYearData:
    """ This is a single years projection data """
  self.__init__(self, year:int):
      assert isinstance(year int)
      self.projectionYear:int=year

      self.clientAge:int=None
      self.clientIsAlive:bool=None
      self.spouseAge:int=None
      self.spouseIsAlive:bool=None
      
      self.incomeSources:dict={}    #key is Name, #value is income value
      self.incomeTotal:int=0
      
      self.expenseSources:dict={}
      self.expenseTotal:int=0
      
      self.federalTaxes:int=0
      
      #cash flow is just incometotal-expenseTotal - federaltaxes
      
      #how much we had to pull from assets because expenses > income
      self.assetWithdraw:int=0
      
      self.assetSources:dict={}


      #required Minimal distributions
      self.RMD:int=0
      self.RMDPercent:float=0.0

      

class Projections:
    def __init__(self, dv: DataVariables):
        self._begin_year = datetime.now().year

        self._withdrawOrder = dv._withdrawOrder

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

            if _record._begin_age is None:
                _record._begin_age=0
                
            if _record._amount is not None:
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

            if _record._begin_age is None:
                _record._begin_age = 0
            if _record._amount is not None:
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
                Account("Regular", AccountType.Regular, "1", dv._Regular, _cola)
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

        self._end_year = self._begin_year + dv._forecastYears
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
            # _data.append(DataElement("Cash Flow", "Total", _year, _cash_flow))
            # TODO: if _income - _expense is negative, we need to pull resources from savings...

            if _cash_flow >= 0:
                _data.append(DataElement("Pulled from Assets", "Total", _year, 0))
            else:
                _beginning_cash_flow = abs(_cash_flow)
                # _data.append(DataElement("Pulled from Assets", "Total", _year, ))
                # we need to pull money from Assets..
                # define a new class that takes care of this logic, etc
                _ws = WithdrawStrategy(self._withdrawOrder, self._Assets)
                _cash_flow = _ws.reconcile_deficit(abs(_cash_flow))

                _data.append(
                    DataElement(
                        "Pulled from Assets",
                        "Total",
                        _year,
                        _beginning_cash_flow - _cash_flow,
                    )
                )
                _cash_flow = -_cash_flow  # needs to be negative

            _data.append(DataElement("Cash Flow", "Total", _year, _cash_flow))

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

        _dt = TableData(BeginYear=self._begin_year, EndYear=self._end_year, Data=_data)
        return _dt
