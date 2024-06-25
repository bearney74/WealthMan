from datetime import datetime, date

from .Account import Account
from .IncomeSources import IncomeSource
from .Expense import Expense
from .RequiredMinimalDistributions import RMD
from .EnumTypes import (
    AccountType,
    AccountOwnerType,
    AmountPeriodType,
    FederalTaxStatusType,
    IncomeType,
)
from .FederalTax import FederalTax

from .Person import Person
from .DataVariables import DataVariables
from .WithdrawStrategy import WithdrawStrategy


import logging

logger = logging.getLogger(__name__)


class ProjectionYearData:
    def __init__(self, year: int):
        """This is a single years projection data"""
        assert isinstance(year, int)
        self.projectionYear: int = year

        self.clientAge: int = None
        self.clientIsAlive: bool = None
        self.spouseAge: int = None
        self.spouseIsAlive: bool = None

        self.incomeSources: dict = {}  # key is Name, #value is income value
        self.incomeTotal: int = 0

        self.expenseSources: dict = {}
        self.expenseTotal: int = 0

        self.federalTaxes: int = 0

        # cash flow is just incometotal-expenseTotal - federaltaxes

        # how much we had to pull from assets because expenses > income
        self.assetWithdraw: int = 0
        self.deficit:int = 0

        self.assetSources: dict = {}
        self.assetTotal: int = 0

        # required Minimal distributions
        self.clientRMD: int = 0
        self.clientRMDPercent: float = 0.0

        self.spouseRMD: int = 0
        self.spouseRMDPercent: float = 0.0
        
        self.totalRMD:int =0
        self.totalRMDPercent:float = 0.0


class Projections:
    def __init__(self, dv: DataVariables):
        self._begin_year = datetime.now().year

        self._withdrawOrder = dv._withdrawOrder

        self._client = Person(
            name=dv._clientName,
            birthDate=dv._clientBirthDate,
            lifeSpanAge=dv._clientLifeSpanAge,
            retirementAge=dv._clientRetirementAge,
            relationship=dv._relationStatus,
        )

        self._spouse = None
        if dv._relationStatus == "Married":
            self._spouse = Person(
                name=dv._spouseName,
                birthDate=dv._spouseBirthDate,
                retirementAge=dv._spouseRetirementAge,
                lifeSpanAge=dv._spouseLifeSpanAge,
            )

        self._IncomeSources = []
        for _record in dv._incomes:
            _birthdate = self._client.birthDate
            if _record._owner == AccountOwnerType.Spouse:
                _birthdate = self._spouse.birthDate

            if _record._begin_age is None:
                _record._begin_age = 0

            if _record._amount is not None:
                if _record._end_age is None:
                    _record._end_age = 99
                if _record._COLA is None:
                    _record._COLA = 0.0
                _is = IncomeSource(
                    _record._descr,
                    IncomeType.Employment,  #todo Fix me..  SS, pension
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
            _birthdate = self._client.birthDate
            if _record._owner == AccountOwnerType.Spouse:
                _birthdate = self._spouse.birthDate

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
                    "Client IRA",
                    AccountType.TaxDeferred,
                    AccountOwnerType.Client,
                    dv._clientIRA,
                    _cola,
                )
            )
        if dv._clientRothIRA is not None:
            self._Assets.append(
                Account(
                    "Client Roth IRA",
                    AccountType.TaxFree,
                    AccountOwnerType.Client,
                    dv._clientRothIRA,
                    _cola,
                )
            )

        if dv._Regular is not None:
            self._Assets.append(
                Account(
                    "Regular",
                    AccountType.Regular,
                    AccountOwnerType.Both,
                    dv._Regular,
                    _cola,
                )
            )

        if dv._spouseIRA is not None:
            self._Assets.append(
                Account(
                    "Spouse IRA",
                    AccountType.TaxDeferred,
                    AccountOwnerType.Spouse,
                    dv._spouseIRA,
                    _cola,
                )
            )

        if dv._spouseRothIRA is not None:
            self._Assets.append(
                Account(
                    "Spouse Roth IRA",
                    AccountType.TaxFree,
                    AccountOwnerType.Spouse,
                    dv._spouseRothIRA,
                    _cola,
                )
            )

        self._end_year = self._begin_year + dv._forecastYears
        # TODO fix me
        self._federal_tax_status = FederalTaxStatusType.MarriedJointly
        # self._federal_tax_status = self._vars["GlobalVars"].FederalTaxStatus

    def execute(self):
        _projection_data = []
        # _data = []
        _clientRMD = RMD(self._client, self._spouse)
        _spouseRMD=None
        if self._spouse is not None:
           _spouseRMD = RMD(self._spouse, self._client)
           
        for _year in range(self._begin_year, self._end_year + 1):
            _pyd = ProjectionYearData(_year)

            _clientage = self._client.calc_age_by_year(_year)
            _clientIsAlive = _clientage <= self._client.lifeSpanAge
            _pyd.clientAge = _clientage
            _pyd.clientIsAlive = _clientIsAlive
            
                   
            _spouseage = None
            _spouseIsAlive = None
            if self._spouse is not None:
                _spouseage = self._spouse.calc_age_by_year(_year)
                _spouseIsAlive = _spouseage <= self._spouse.lifeSpanAge
                _pyd.spouseAge = _spouseage
                _pyd.spouseIsAlive = _spouseIsAlive

            if not _clientIsAlive:
                if self._client.relationship == "Single":
                   _projection_data.append(_pyd)
                   continue
                elif not _spouseIsAlive:
                    _projection_data.append(_pyd)
                    continue
                    
            #at least one person is still alive...  do the projection for that year...
            _income_total = 0
            for _src in self._IncomeSources:
                _income = _src.calc_balance_by_year(_year)
                _pyd.incomeSources[_src.Name] = _income

                _income_total += _income  # _src.calc_income_by_year(_year)

            _pyd.incomeTotal = _income_total

            # federal taxes
            _ft = FederalTax(self._federal_tax_status, 2024)
            _taxable_income = max(_income_total - _ft.StandardDeduction, 0)
            _taxes = _ft.calc_taxes(_taxable_income)
            _pyd.federalTaxes = _taxes

            _expense_total = 0
            for _src in self._Expenses:
                _expense = _src.calc_balance_by_year(_year)
                _pyd.expenseSources[_src.Name] = _expense

                _expense_total += _expense
            _pyd.expenseTotal = _expense_total

            _cash_flow = _income_total - _expense_total - _taxes


            #_total = 0
            _client_ira_total = 0
            _spouse_ira_total = 0
            for _src in self._Assets:
            #    _balance = _src.calc_balance_by_year(_year)
            #    #_pyd.assetSources[_src.Name] = _balance
                if _src.Type == AccountType.TaxDeferred:
                    if _src.Owner == AccountOwnerType.Client:
                       _client_ira_total += _src.Balance
                    elif _src.Owner == AccountOwnerType.Spouse:
                        _spouse_ira_total += _src.Balance

            #    _total += _balance

            #_pyd.assetTotal = _total

            #do RMD calcs
            _rmd_pct = _clientRMD.calc(date(_year, 12, 31))
            _pyd.clientRMDPercent = _rmd_pct
            _pyd.clientRMD = int(_rmd_pct / 100.0 * _client_ira_total)
            
            if self._spouse is not None:
               _rmd_pct = _spouseRMD.calc(date(_year, 12, 31))
               _pyd.spouseRMDPercent = _rmd_pct
               _pyd.spouseRMD = int(_rmd_pct / 100.0 * _spouse_ira_total)
            
            _pyd.totalRMD= _pyd.clientRMD + _pyd.spouseRMD
            _pyd.totalRMDPercent = 100.0 * _pyd.totalRMD/(_client_ira_total + _spouse_ira_total) 
            

            if _cash_flow >= 0 and _pyd.totalRMD == 0:
                _pyd.assetWithdraw = 0
            else:
                #_beginning_cash_flow = abs(_cash_flow)
                # we need to pull money from Assets..
                # define a new class that takes care of this logic, etc
                #print(_cash_flow, _pyd.totalRMD, max(abs(_cash_flow), _pyd.totalRMD))
                _ws = WithdrawStrategy(
                    self._withdrawOrder,
                    _clientage,
                    _clientIsAlive,
                    _spouseage,
                    _spouseIsAlive,
                    self._Assets,
                )
                _pyd.assetWithdraw = max(abs(_cash_flow), _pyd.totalRMD)
                _resulting_deficit = _ws.reconcile_deficit(_pyd.assetWithdraw)
                _pyd.deficit=_resulting_deficit
                #print(_resulting_deficit)
                #_resulting deficit should be zero, unless client does not have the funds available..
                
                #_pyd.assetWithdraw = _beginning_cash_flow - _cash_flow
                #_pyd.assetWidthdraw = _cash_flow
                #_cash_flow = -_cash_flow  # needs to be negative

            _total = 0
            _client_ira_total = 0
            _spouse_ira_total = 0
            for _src in self._Assets:
                _balance = _src.calc_balance_by_year(_year)
                _pyd.assetSources[_src.Name] = _balance
                if _src.Type == AccountType.TaxDeferred:
                    if _src.Owner == AccountOwnerType.Client:
                       _client_ira_total += _balance
                    elif _src.Owner == AccountOwnerType.Spouse:
                        _spouse_ira_total += _balance

                _total += _balance

            _pyd.assetTotal = _total
 
            _projection_data.append(_pyd)

        return _projection_data
