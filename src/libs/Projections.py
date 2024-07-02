from datetime import datetime, date

from .Account import Account
from .IncomeSources import IncomeSource, SocialSecurity
from .Expense import Expense
from .RequiredMinimalDistributions import RMD
from .EnumTypes import (
    AccountType,
    AccountOwnerType,
    AmountPeriodType,
    FederalTaxStatusType,
    IncomeSourceType,
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

        self.thisYearsFederalTaxes: int = 0
        self.lastYearsFederalTaxes: int = 0

        # cash flow is just incometotal-expenseTotal - federaltaxes

        # how much we had to pull from assets because expenses > income
        self.assetWithdraw: int = 0
        self.surplus_deficit: int = 0

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


class Projections:
    def __init__(self, dv: DataVariables):
        # can set this to see todays dollars
        self.InTodaysDollars = dv.inTodaysDollars

        if dv.inTodaysDollars:
            self._inflation = dv.inflation
        else:
            self._inflation = 0

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
        if dv.relationStatus == "Married":
            self._spouse = Person(
                name=dv.spouseName,
                birthDate=dv.spouseBirthDate,
                retirementAge=dv.spouseRetirementAge,
                lifeSpanAge=dv.spouseLifeSpanAge,
            )

        self._IncomeSources = []
        # do SS and pensions...
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
        if dv.relationStatus == "Married":
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
            # print("pension2Name='%s'" % dv.pension2Name)
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

            if _record.begin_age is None:
                _record.begin_age = 0

            if _record.amount is not None:
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

            if _record.begin_age is None:
                _record.begin_age = 0
            if _record.amount is not None:
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
                if _record.begin_age is None:
                    logger.Error(
                        "Expense '%s' not used since begin date not set" % _record.descr
                    )
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
        # TODO fix me
        self._federal_tax_status = FederalTaxStatusType.MarriedJointly
        # self._federal_tax_status = self._vars["GlobalVars"].FederalTaxStatus

    def execute(self):
        _projection_data = []
        # _data = []
        _clientRMD = RMD(self._client, self._spouse)
        _spouseRMD = None
        if self._spouse is not None:
            _spouseRMD = RMD(self._spouse, self._client)

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

            if not _clientIsAlive:
                if self._client.relationship == "Single":
                    _projection_data.append(_pyd)
                    continue
                elif not _spouseIsAlive:
                    _projection_data.append(_pyd)
                    continue

            # at least one person is still alive...  do the projection for that year...
            _income_total = 0
            for _src in self._IncomeSources:
                _income = _src.calc_balance_by_year(_year)

                _pyd.incomeSources[_src.Name] = _income

                _income_total += _income  # _src.calc_income_by_year(_year)

            _pyd.incomeTotal = _income_total

           
            _expense_total = 0
            for _src in self._Expenses:
                _expense = _src.calc_balance_by_year(_year)
                _pyd.expenseSources[_src.Name] = _expense

                _expense_total += _expense
            _pyd.expenseTotal = _expense_total

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

            #    _total += _balance

            # _pyd.assetTotal = _total

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

            # ??? should we include TotalRMD as part of cashflow?
            _cash_flow = _income_total - _expense_total - _lastYearsFederalTaxes

            # print(_income_total, _expense_total, _income_total - _expense_total, _pyd.totalRMD)
            if _cash_flow < 0:
                _pyd.assetWithdraw = max(abs(_cash_flow), _pyd.totalRMD)
            else:
                _pyd.assetWithdraw = 0

            if _pyd.assetWithdraw == 0:
                # _pyd.assetWithdraw = 0
                _pyd.surplus_deficit = _cash_flow
            else:
                # we need to pull money from Assets..
                # define a new class that takes care of this logic, etc
                # print(_cash_flow, _pyd.totalRMD, max(abs(_cash_flow), _pyd.totalRMD))
                _ws = WithdrawStrategy(
                    self._withdrawOrder,
                    _clientage,
                    _clientIsAlive,
                    _spouseage,
                    _spouseIsAlive,
                    self._Assets,
                )
                # _pyd.assetWithdraw = max(abs(_cash_flow), _pyd.totalRMD)
                _deficit = _ws.reconcile_required_withdraw(_pyd.assetWithdraw)
                # if _deficit > 0.. we have run out of money...
                if _deficit > 0:
                    _pyd.surplus_deficit = -_deficit
                else:
                    _pyd.surplus_deficit = _pyd.assetWithdraw + _cash_flow
                
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

            # federal taxes
            _ft = FederalTax(self._federal_tax_status, 2024)
            _taxable_income = max(
                _pyd.assetWithdraw + _income_total - _ft.StandardDeduction, 0
            )
            _pyd.taxableIncome = _taxable_income
            _pyd.thisYearsFederalTaxes = _ft.calc_taxes(_taxable_income)

            _pyd.lastYearsFederalTaxes = _lastYearsFederalTaxes
            _lastYearsFederalTaxes = _pyd.thisYearsFederalTaxes

            _pyd.federalEffectiveTaxRate = _ft.effective_tax_rate(
                _taxable_income, _pyd.incomeTotal + _pyd.assetWithdraw
            )
            _pyd.federalMarginalTaxRate = _ft.marginal_tax_rate(
                _pyd.incomeTotal + _pyd.assetWithdraw
            )

            _projection_data.append(_pyd)

        return _projection_data
