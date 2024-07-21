from datetime import datetime, date

from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot

from .Account import Account
from .DataVariables import DataVariables
from .EnumTypes import (
    AccountType,
    AccountOwnerType,
    AmountPeriodType,
    FederalTaxStatusType,
    IncomeSourceType,
)
from .Expense import Expense
from .FederalPovertyLevel import FederalPovertyLevel
from .FederalTax import FederalTax
from .IncomeSources import IncomeSource, SocialSecurity
from .Person import Person
from .ProvisionalIncome import ProvisionalIncome
from .RequiredMinimalDistributions import RMD
from .SurplusAccount import SurplusAccount
from .WithdrawStrategy import WithdrawStrategy

import logging

logger = logging.getLogger(__name__)


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class ProjectionYearData:
    def __init__(self, year: int):
        """This is a single years projection data"""
        assert isinstance(year, int)
        self.projectionYear: int = year

        self.clientAge: int = None
        self.clientIsAlive: bool = None
        self.spouseAge: int = None
        self.spouseIsAlive: bool = None

        self.incomeSources: dict = {}  # key is Name, #value is income
        self.incomeTotal: int = 0
        self.FPL: float = 0.0

        self.ssIncomeTotal: int = 0
        self.ssTaxableIncome: int = 0

        self.expenseSources: dict = {}
        self.expenseTotal: int = 0

        self.cashFlow: int = 0  # income total - expense total - - lastYearsFederal Taxes - asset contributions
        self.surplusDeficit: int = 0  # cashFlow - assetWithdraws

        self.federalTaxFilingStatus: FederalTaxStatusType = None
        self.thisYearsFederalTaxes: int = 0
        self.lastYearsFederalTaxes: int = 0

        self.longTermCapitalGainsTaxes: int = 0

        # cash flow is just incometotal-expenseTotal - federaltaxes

        # how much we had to pull from assets because expenses > income
        self.assetWithdraw: int = 0
        self.assetTaxDeferredWithdraw: int = 0
        self.assetRegularWithdraw: int = 0
        self.assetTaxFreeWithdraw: int = 0

        # self.surplus_deficit: int = 0

        self.assetSources: dict = {}
        self.assetContributions: dict = {}
        self.assetTotal: int = 0

        # required Minimal distributions
        self.clientRMD: int = 0
        self.clientRMDPercent: float = 0.0

        self.spouseRMD: int = 0
        self.spouseRMDPercent: float = 0.0

        self.totalRMD: int = 0
        self.totalRMDPercent: float = 0.0

        # surplus account
        self.surplusBalance: int = 0
        self.surplusWithdraw: int = 0

        self.AW: int = 0  # TAD = Total Asset Drawdown
        self.AWR: float = 0


class Projections(QRunnable):
    def __init__(self, dv: DataVariables):
        super(Projections, self).__init__()

        self.signals = WorkerSignals()
        # can set this to see todays dollars
        self.InTodaysDollars = dv.inTodaysDollars

        if dv.inTodaysDollars:
            self._inflation = dv.inflation
        else:
            self._inflation = 0

        self.UseSurplusAccount = dv.SurplusAccount
        # print(self.UseSurplusAccount)
        self.SurplusAccountInterestRate = dv.SurplusAccountInterestRate

        _is_married = dv.relationStatus == "Married"

        self._begin_year = datetime.now().year

        self._withdrawOrder = dv.withdrawOrder

        self._client = Person(
            name=dv.clientName,
            birthDate=dv.clientBirthDate,
            lifeSpanAge=dv.clientLifeSpanAge,
            retirementAge=dv.clientRetirementAge,
            relationship=dv.relationStatus,
        )

        self._spouse = None
        if _is_married:
            self._spouse = Person(
                name=dv.spouseName,
                birthDate=dv.spouseBirthDate,
                retirementAge=dv.spouseRetirementAge,
                lifeSpanAge=dv.spouseLifeSpanAge,
            )

        self._IncomeSources = []
        # do SS and pensions...
        if dv.clientSSAmount is not None:
            _client_ss = SocialSecurity(
                Name="Client Social Security",
                BirthDate=dv.clientBirthDate,
                FRAAmount=dv.clientSSAmount,
                Owner=AccountOwnerType.Client,
                BeginAge=dv.clientSSBeginAge,
                LifeSpanAge=dv.clientLifeSpanAge,
                COLA=dv.clientSSCola - self._inflation,
            )
            self._IncomeSources.append(_client_ss)

        if _is_married:
            if dv.spouseSSAmount is not None:
                _spouse_ss = SocialSecurity(
                    Name="Spouse Social Security",
                    BirthDate=dv.spouseBirthDate,
                    FRAAmount=dv.spouseSSAmount,
                    Owner=AccountOwnerType.Spouse,
                    BeginAge=dv.spouseSSBeginAge,
                    LifeSpanAge=dv.spouseLifeSpanAge,
                    COLA=dv.spouseSSCola - self._inflation,
                )
                self._IncomeSources.append(_spouse_ss)

                # these are needed for comparing spouses ss benefits when
                # spouse dies so that living spouse gets the greater benefit of the
                # two
                _spouse_ss.set_SpouseSS(_client_ss)
                _client_ss.set_SpouseSS(_spouse_ss)

        # pensions..
        if dv.pension1Name is not None and dv.pension1Name.strip() != "":
            _birthdate = dv.clientBirthDate
            _lifespan = dv.clientLifeSpanAge
            if dv.pension1Owner == AccountOwnerType.Spouse:
                _birthdate = dv.spouseBirthDate
                _lifespan = dv.spouseLifeSpanAge

            _is = IncomeSource(
                Name=dv.pension1Name,
                IncomeType=IncomeSourceType.Pension,
                Owner=dv.pension1Owner,
                Amount=dv.pension1Amount,
                AmountPeriod=AmountPeriodType.Annual,
                BirthDate=_birthdate,
                BeginAge=dv.pension1BeginAge,
                LifeSpanAge=_lifespan,
                SurvivorPercent=dv.pension1SurvivorBenefits,
                COLA=dv.pension1Cola - self._inflation,
            )
            self._IncomeSources.append(_is)

        if dv.pension2Name is not None and dv.pension2Name.strip() != "":
            _birthdate = dv.clientBirthDate
            _lifespan = dv.clientLifeSpanAge
            if dv.pension2Owner == AccountOwnerType.Spouse:
                _birthdate = dv.spouseBirthDate
                _lifespan = dv.spouseLifeSpanAge

            _is = IncomeSource(
                Name=dv.pension2Name,
                IncomeType=IncomeSourceType.Pension,
                Owner=dv.pension2Owner,
                Amount=dv.pension2Amount,
                AmountPeriod=AmountPeriodType.Annual,
                BirthDate=_birthdate,
                BeginAge=dv.pension2BeginAge,
                SurvivorPercent=dv.pension2SurvivorBenefits,
                COLA=dv.pension2Cola - self._inflation,
            )
            self._IncomeSources.append(_is)

        for _record in dv.otherIncomes:
            _birthdate = dv.clientBirthDate
            if _record.owner == AccountOwnerType.Spouse:
                _birthdate = dv.spouseBirthDate

            if _record.amount is not None:
                if _record.begin_age is None:
                    _record.begin_age = 0
                if _record.end_age is None:
                    _record.end_age = 99
                if _record.COLA is None:
                    _record.COLA = 0.0
                _is = IncomeSource(
                    _record.descr,
                    IncomeSourceType.Employment,
                    _record.amount,
                    AmountPeriodType.Annual,
                    _record.owner,
                    BirthDate=_birthdate,
                    BeginAge=_record.begin_age,
                    EndAge=_record.end_age,
                    Taxable=True,
                    COLA=_record.COLA - self._inflation,
                )

                self._IncomeSources.append(_is)
            else:
                if _record.amount is None:
                    logger.Error(
                        "Income Source '%s' not used since amount not set"
                        % _record.descr
                    )

        self._Expenses = []
        for _record in dv.expenses:
            _birthdate = dv.clientBirthDate
            if _record.owner == AccountOwnerType.Spouse:
                _birthdate = dv.spouseBirthDate

            if _record.amount is not None:
                if _record.begin_age is None:
                    _record.begin_age = 0
                if _record.end_age is None:
                    _record.end_age = 99
                if _record.COLA is None:
                    _record.COLA = 0.0

                _e = Expense(
                    _record.descr,
                    _record.amount,
                    AmountPeriodType.Annual,
                    BirthDate=_birthdate,
                    BeginAge=_record.begin_age,
                    EndAge=_record.end_age,
                    COLA=_record.COLA - self._inflation,
                )

                self._Expenses.append(_e)
            else:
                if _record.amount is None:
                    logger.Error(
                        "Expense '%s' not used since amount not set" % _record._descr
                    )

        self._Assets = []
        if dv.clientIRABalance is not None:
            self._Assets.append(
                Account(
                    Name="Client IRA",
                    Type=AccountType.TaxDeferred,
                    Owner=AccountOwnerType.Client,
                    BirthDate=dv.clientBirthDate,
                    Balance=dv.clientIRABalance,
                    COLA=dv.clientIRACola - self._inflation,
                    Contribution=dv.clientIRAContribution,
                    ContributionBeginAge=dv.clientIRAContributionBeginAge,
                    ContributionEndAge=dv.clientIRAContributionEndAge,
                )
            )
        if dv.clientRothIRABalance is not None:
            self._Assets.append(
                Account(
                    Name="Client Roth IRA",
                    Type=AccountType.TaxFree,
                    Owner=AccountOwnerType.Client,
                    BirthDate=dv.clientBirthDate,
                    Balance=dv.clientRothIRABalance,
                    COLA=dv.clientRothIRACola - self._inflation,
                    Contribution=dv.clientRothIRAContribution,
                    ContributionBeginAge=dv.clientRothIRAContributionBeginAge,
                    ContributionEndAge=dv.clientRothIRAContributionEndAge,
                )
            )

        if dv.regularBalance is not None:
            self._Assets.append(
                Account(
                    Name="Regular",
                    Type=AccountType.Regular,
                    Owner=AccountOwnerType.Both,
                    BirthDate=dv.clientBirthDate,
                    Balance=dv.regularBalance,
                    COLA=dv.regularCola - self._inflation,
                    Contribution=dv.regularContribution,
                    ContributionBeginAge=dv.regularContributionBeginAge,
                    ContributionEndAge=dv.regularContributionEndAge,
                )
            )

        if dv.spouseIRABalance is not None:
            self._Assets.append(
                Account(
                    Name="Spouse IRA",
                    Type=AccountType.TaxDeferred,
                    Owner=AccountOwnerType.Spouse,
                    Balance=dv.spouseIRABalance,
                    BirthDate=dv.spouseBirthDate,
                    COLA=dv.spouseIRACola - self._inflation,
                    Contribution=dv.spouseIRAContribution,
                    ContributionBeginAge=dv.spouseIRAContributionBeginAge,
                    ContributionEndAge=dv.spouseIRAContributionEndAge,
                )
            )

        if dv.spouseRothIRABalance is not None:
            self._Assets.append(
                Account(
                    Name="Spouse Roth IRA",
                    Type=AccountType.TaxFree,
                    Owner=AccountOwnerType.Spouse,
                    BirthDate=dv.spouseBirthDate,
                    Balance=dv.spouseRothIRABalance,
                    COLA=dv.spouseRothIRACola - self._inflation,
                    Contribution=dv.spouseRothIRAContribution,
                    ContributionBeginAge=dv.spouseRothIRAContributionBeginAge,
                    ContributionEndAge=dv.spouseRothIRAContributionEndAge,
                )
            )

        self._end_year = self._begin_year + dv.forecastYears
        self._federal_tax_status = dv.federalFilingStatus
        self._federal_tax_status_once_widowed = dv.federalFilingStatusOnceWidowed

    @pyqtSlot()
    def run(self):
        _projection_data = []

        _clientRMD = RMD(self._client, self._spouse)
        _spouseRMD = None
        if self._spouse is not None:
            _spouseRMD = RMD(self._spouse, self._client)

        # _surplusBalance = 0
        # _surplusInterestRate = self.SurplusAccountInterestRate
        _surplusAccount = SurplusAccount(0, self.SurplusAccountInterestRate)

        _lastYearsFederalTaxes = 0
        for _year in range(self._begin_year, self._end_year + 1):
            _pyd = ProjectionYearData(_year)

            _clientage = self._client.calc_age_by_year(_year)
            _clientIsAlive = _clientage <= self._client.lifeSpanAge
            _pyd.clientAge = _clientage
            _pyd.clientIsAlive = _clientIsAlive

            if _clientage == self._client.lifeSpanAge + 1:
                # should set client RMD to spouse
                _clientRMD.death_event(self._client)

            _spouseage = None
            _spouseIsAlive = None
            if self._spouse is not None:
                _spouseage = self._spouse.calc_age_by_year(_year)
                _spouseIsAlive = _spouseage <= self._spouse.lifeSpanAge
                _pyd.spouseAge = _spouseage
                _pyd.spouseIsAlive = _spouseIsAlive

                if _spouseage == self._spouse.lifeSpanAge + 1:
                    _spouseRMD.death_event(self._spouse)

            # check to see if client (and spouse) are dead...
            if not _clientIsAlive:
                if self._client.relationship == "Single":
                    _projection_data.append(_pyd)
                    continue
                elif not _spouseIsAlive:
                    _projection_data.append(_pyd)
                    continue

            # at least one person is still alive...  do the projection for that year...

            if not _clientIsAlive or not _spouseIsAlive:
                _pyd.federalTaxFilingStatus = self._federal_tax_status_once_widowed
            else:
                _pyd.federalTaxFilingStatus = self._federal_tax_status

            _income_total = 0
            _ss_income_total = 0
            for _src in self._IncomeSources:
                # _income = _src.calc_balance_by_year(_year)
                if _src.IncomeType == IncomeSourceType.SocialSecurity:
                    _income = _src.calc_balance_by_year(_year)
                    _ss_income_total += _income
                else:
                    _income = _src.calc_balance_by_year(_year)

                _pyd.incomeSources[_src.Name] = _income

                _income_total += _income  # _src.calc_income_by_year(_year)

            # _pyd.incomeTotal = _income_total
            _pyd.ssIncomeTotal = _ss_income_total

            _expense_total = 0
            for _src in self._Expenses:
                _expense = _src.calc_balance_by_year(_year)
                _pyd.expenseSources[_src.Name] = _expense

                _expense_total += _expense
            _pyd.expenseTotal = _expense_total

            _total = 0
            _client_ira_total = 0
            _spouse_ira_total = 0
            _contribution_total = 0
            for _src in self._Assets:
                _src.calc_balance()
                if (
                    _src.ContributionBeginDate.year <= _year
                    and _src.ContributionEndDate.year >= _year
                ):
                    _src.deposit(_src.Contribution)
                    _pyd.assetContributions[_src.Name] = _src.Contribution
                    _contribution_total += _src.Contribution
                else:
                    _pyd.assetContributions[_src.Name] = 0

                _pyd.assetSources[_src.Name] = _src.Balance

                if _src.Type == AccountType.TaxDeferred:
                    if _src.Owner == AccountOwnerType.Client:
                        _client_ira_total += _src.Balance
                    elif _src.Owner == AccountOwnerType.Spouse:
                        _spouse_ira_total += _src.Balance

                _total += _src.Balance

            _pyd.assetTotal = _total
            _pyd.assetContributionTotal = _contribution_total

            # _cash_flow = _income_total - _expense_total - _taxes

            # _total = 0
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

            # do RMD calcs
            _rmd_pct = _clientRMD.calc(date(_year, 12, 31))
            _pyd.clientRMDPercent = _rmd_pct
            _pyd.clientRMD = int(_rmd_pct / 100.0 * _client_ira_total)

            if self._spouse is not None:
                _rmd_pct = _spouseRMD.calc(date(_year, 12, 31))
                _pyd.spouseRMDPercent = _rmd_pct
                _pyd.spouseRMD = int(_rmd_pct / 100.0 * _spouse_ira_total)

            _pyd.totalRMD = _pyd.clientRMD + _pyd.spouseRMD
            if _client_ira_total + _spouse_ira_total == 0:
                _pyd.totalRMDPercent = 0.0
            else:
                _pyd.totalRMDPercent = (
                    100.0 * _pyd.totalRMD / (_client_ira_total + _spouse_ira_total)
                )

            _pyd.cashFlow = (
                _income_total
                - _expense_total
                - _lastYearsFederalTaxes
                - _contribution_total
            )

            if _pyd.cashFlow < 0 or _pyd.totalRMD > 0:
                # we need to withdraw money from assets to make up for the cash flow deficit
                _ws = WithdrawStrategy(
                    self._withdrawOrder,
                    _clientage,
                    _clientIsAlive,
                    _spouseage,
                    _spouseIsAlive,
                    self._Assets,
                )
                _neededAssetWithdraw = max(abs(_pyd.cashFlow), _pyd.totalRMD)
                _deficit, _withdraw_dict = _ws.reconcile_required_withdraw(
                    _neededAssetWithdraw
                )

                _pyd.assetWithdraw = 0
                _pyd.assetTaxDeferredWithdraw = _withdraw_dict[AccountType.TaxDeferred]
                _pyd.assetRegularWithdraw = _withdraw_dict[AccountType.Regular]
                _pyd.assetTaxFreeWithdraw = _withdraw_dict[AccountType.TaxFree]

                for _asset_type, _amount in _withdraw_dict.items():
                    _pyd.assetWithdraw += _amount
                    if (
                        _asset_type == AccountType.TaxDeferred
                    ):  # these withdraws are seen as regular income
                        _income_total += _amount
                        # print(_amount)

                # _pyd.surplusDeficit = _pyd.cashFlow + _pyd.assetWithdraw - _deficit
            else:
                _pyd.assetWithdraw = 0
                _pyd.assetTaxDeferredWithdraw = 0
                _pyd.assetRegularWithdraw = 0
                _pyd.assetTaxFreeWithdraw = 0

                _deficit = 0
                # _pyd.surplusDeficit = _pyd.cashFlow
                _withdraw_dict = {
                    AccountType.Regular: 0,
                    AccountType.TaxDeferred: 0,
                }  # no withdraws...
                # _income_total = 0

            _pyd.incomeTotal = _income_total

            # _pyd.assetWithdraw=0
            # for _asset_type, _amount in _withdraw_dict.items():
            #    _pyd.assetWithdraw+=_amount
            #    if (
            #        _asset_type == AccountType.TaxDeferred
            #    ):  # these withdraws are seen as regular income
            #        _income_total += _amount

            """
            _total = 0
            _client_ira_total = 0
            _spouse_ira_total = 0
            _contribution_total = 0
            for _src in self._Assets:
                _src.calc_balance()
                if (
                    _src.ContributionBeginDate.year <= _year
                    and _src.ContributionEndDate.year >= _year
                ):
                    _src.deposit(_src.Contribution)
                    _pyd.assetContributions[_src.Name] = _src.Contribution
                    _contribution_total += _src.Contribution
                else:
                    _pyd.assetContributions[_src.Name] = 0

                _pyd.assetSources[_src.Name] = _src.Balance

                if _src.Type == AccountType.TaxDeferred:
                    if _src.Owner == AccountOwnerType.Client:
                        _client_ira_total += _src.Balance
                    elif _src.Owner == AccountOwnerType.Spouse:
                        _spouse_ira_total += _src.Balance

                _total += _src.Balance

            _pyd.assetTotal = _total
            _pyd.assetContributionTotal = _contribution_total
            """

            # _pyd.cashFlow -= _pyd.assetContributionTotal
            _pyd.surplusDeficit = _pyd.cashFlow + _pyd.assetWithdraw  # - _deficit

            # _pyd.cashFlow -= _contribution_total
            # _pyd.surplusDeficit -= _contribution_total

            if _pyd.ssIncomeTotal > 0:
                # if we are calculating in todays dollars, we need to deflate the value of provisional income amounts for rates
                if self.InTodaysDollars:
                    _cpi = pow(1 - self._inflation / 100.0, _year - self._begin_year)
                else:
                    _cpi = 1
                _pi = ProvisionalIncome(_pyd.federalTaxFilingStatus, _cpi)
                _pyd.ssTaxRate = _pi.get_rate(
                    _income_total - _ss_income_total,
                    _ss_income_total,
                )
                _pyd.ssTaxableIncome = _pi.calc_ss_taxable(
                    _income_total
                    - _ss_income_total,  # + _pyd.assetWithdraw, to we need to add in Regular Brockerage withdraws?
                    _ss_income_total,
                )
                # print(_year, _cpi, _income_total - _ss_income_total, _pyd.ssTaxRate, _pyd.ssTaxableIncome)
            else:
                _pyd.ssTaxableIncome = 0
                _pyd.ssTaxRate = 0.0

            # _surplusWithdraw = 0
            if self.UseSurplusAccount:
                _surplusAccount.add_interest()
                # should we calculate this years interest after deposits/withdraws or before?
                # does it really matter?

                if _pyd.surplusDeficit < 0:
                    _pyd.surplusWithdraw, _pyd.surplusDeficit = (
                        _surplusAccount.withdraw(abs(_pyd.surplusDeficit))
                    )
                    _pyd.assetWithdraw += _pyd.surplusWithdraw
                else:
                    _surplusAccount.deposit(_pyd.surplusDeficit)
                    _pyd.surplusWithdraw = 0

                """
                if _surplusBalance > 0:  #only add in interest if balance is positive..  #todo when balance is negative.
                   _surplusBalance = int(
                      _surplusBalance * (1.0 + self.SurplusAccountInterestRate / 100.0)
                   )
                   if _pyd.surplusDeficit < 0:  # we have a deficit, so let us take it from the surplus account
                      if (
                        _surplusBalance >= abs(_pyd.surplusDeficit)
                      ):  # we have enough to take care of the full deficit
                        _surplusWithdraw = abs(_pyd.surplusDeficit)
                        _surplusBalance -= _surplusWithdraw
                        _pyd.surplusDeficit = 0
                        _pyd.surplusBalance = _surplusBalance
                      else:
                        _surplusWithdraw = _surplusBalance
                        _pyd.surplusDeficit -= _surplusWithdraw
                        # _surplusWithdraw = _surplusBalance
                        _pyd.surplusBalance = _surplusBalance = _pyd.surplusDeficit
                        _pyd.surplusWithdraw= _surplusWithdraw
                    #else:
                 
                
                if _pyd.surplusDeficit > 0:  # we have no deficit, and possibly a surplus...
                   _surplusBalance += _pyd.surplusDeficit
                   _pyd.surplusWithdraw=_surplusWithdraw = 0
                   _pyd.surplusBalance = _surplusBalance
                
                """
                _pyd.surplusBalance = _surplusAccount.balance
                _pyd.assetTotal += _pyd.surplusBalance

            # federal poverty level...
            _fpl = FederalPovertyLevel(2 if _spouseIsAlive else 1)
            _pyd.FPL = _fpl.calc_percent(
                _pyd.incomeTotal
            )  # + _pyd.assetTaxDeferredWithdraw)

            # federal taxes
            _ft = FederalTax(_pyd.federalTaxFilingStatus, 2024)
            _taxable_income = (
                _income_total - _ss_income_total + _pyd.ssTaxableIncome
            )  # + _surplusWithdraw

            # print(_year, _income_total, _ss_income_total, _pyd.ssTaxableIncome) #, _surplusWithdraw)
            _pyd.taxableIncome = _taxable_income

            _pyd.thisYearsIncomeTaxes = _ft.calc_taxes(
                max(_taxable_income - _ft.StandardDeduction, 0)
            )
            _pyd.longTermCapitalGainsTaxes = _ft.calc_ltcg_taxes(
                _withdraw_dict[AccountType.Regular] + _pyd.surplusWithdraw
            )
            _pyd.thisYearsFederalTaxes = (
                _pyd.thisYearsIncomeTaxes + _pyd.longTermCapitalGainsTaxes
            )

            _pyd.lastYearsFederalTaxes = _lastYearsFederalTaxes
            _lastYearsFederalTaxes = _pyd.thisYearsFederalTaxes

            _pyd.federalEffectiveTaxRate = _ft.effective_tax_rate(
                _pyd.thisYearsIncomeTaxes,
                _income_total,
            )

            # print(_pyd.federalEffectiveTaxRate, _pyd.thisYearsIncomeTaxes, _pyd.incomeTotal)

            _pyd.federalMarginalTaxRate = _ft.marginal_tax_rate(_pyd.taxableIncome)

            # print(_pyd.taxableIncome, _pyd.federalMarginalTaxRate)

            # asset withdraw rate  (AWR)
            if self.UseSurplusAccount:
                _pyd.AW = -_pyd.cashFlow
            else:
                _pyd.AW = _pyd.assetWithdraw

            if _pyd.assetTotal == 0:
                _pyd.AWR = 0.0
            else:
                _pyd.AWR = 100.0 * _pyd.AW / _pyd.assetTotal

            _projection_data.append(_pyd)

        self.signals.result.emit(_projection_data)
