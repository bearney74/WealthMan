from datetime import datetime, date

from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot

from .Account import TraditionalIRA, RothIRA, Brokerage, ContributionClass
from .DataVariables import DataVariables
from .EnumTypes import (
    AccountType,
    AccountOwnerType,
    IncomeSourceType,
    PersonType,
    RelationStatusType,
)

from .Expense import Expense
from .FederalPovertyLevel import FederalPovertyLevel
from .FederalTax import FederalTax
from .IncomeSources import IncomeSource, SocialSecurity
from .MiscLibs import PeriodValidator
from .Person import Person
from .ProvisionalIncome import SocialSecurityTaxes
from .RequiredMinimalDistributions import RMDTable, RMDCalcs
from .SurplusAccount import SurplusAccount
from .TransferAsset import TransferAssets
from .WithdrawStrategy import WithdrawStrategy

import logging

logger = logging.getLogger(__name__)


def todays_amount(amount: int, inflation: int, years: int) -> int:
    """calculate the $ amount to purchase something x years in the future if it
    is valued at amount dollars today, use negative inflation to see
    values in the past"""
    return round(amount * pow(1.0 + inflation / 100.0, years))


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


class DataItem:
    def __init__(
        self, header: str, format: str = "${:,}", default_data: [float, int] = 0
    ):
        self._header = header
        self._format = format
        self._data = default_data

    @property
    def header(self):
        return self._header

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __str__(self):
        if self._data is None:
            return ""
        return self._format.format(self._data)


class PercentDataItem(DataItem):
    def __init__(self, header: str, format="{:.1f}%", default_data: float = None):
        super(PercentDataItem, self).__init__(
            header, format=format, default_data=default_data
        )


class ProjectionYearData:
    def __init__(self, year: int):
        """This is a single years projection data"""
        assert isinstance(year, int)
        self.projectionYear: DataItem = DataItem("Year", "{}", year)

        self.clientAge: int = None
        self.clientIsAlive: bool = None
        self.spouseAge: int = None
        self.spouseIsAlive: bool = None

        self.incomeSources = []
        self.incomeTotal: DataItem = DataItem("Income Total")
        self.activeIncomeTotal: DataItem = DataItem("Active Income Total")

        self.ssIncomeTotal: DataItem = DataItem("SS Income Total")  # int = 0
        self.ssTaxableIncome: DataItem = DataItem("SS Taxable Income")  # int = 0
        self.ssTaxRate: DataItem = PercentDataItem("SS Tax Rate")
        self.taxableIncomeTotal: DataItem = DataItem("Total Taxable Income")

        self.expenseSources = []
        self.expenseTotal: DataItem = DataItem("Expense Total")  # int = 0

        self.netIncome: DataItem = DataItem("Net Income")
        self.federalTaxFilingStatus: DataItem = DataItem(
            "Federal Tax Filing Status", "{.value}", None
        )
        self.thisYearsFederalTaxes: DataItem = DataItem("This Years Federal Taxes")
        self.lastYearsFederalTaxes: DataItem = DataItem("Last Years Federal Taxes")

        self.federalEffectiveTaxRate: DataItem = PercentDataItem(
            "Federal Effective Tax Rate"
        )
        self.federalMarginalTaxRate: DataItem = PercentDataItem(
            "Federal Marginal Tax Rate"
        )

        # self.longTermCapitalGainsTaxes: DataItem = DataItem("LTCG Taxes")  # int = 0

        self.assetTotalBalance = DataItem("Total Asset Balance")
        self.assetTotalDeposits = DataItem("Total Asset Deposits")
        self.assetTotalWithdraws = DataItem("Total Asset Withdraws")
        self.assetTotalReturns = DataItem("Total Asset Returns")
        self.assetTotalContributions = DataItem("Total Asset Contributions")
        self.assetTotalNetDeposits = DataItem(
            "Total Asset Net Deposits"
        )  # deposits - withdraws
        self.assetTotalCashFlow = DataItem("Total Asset Cash Flow")

        self.assetTaxDeferredWithdraws = DataItem(
            "Total Tax Deferred Withdraws"
        )  # counts as regular income
        self.assetTaxFreeWithdraws = DataItem("Total Tax Free Withdraws")
        self.assetRegularReturns = DataItem(
            "Total Regular Returns"
        )  # counts as regular income

        # how much we had to pull from assets because expenses > income

        # self.surplus_deficit: int = 0

        self.assetSources = []

        self.transfersTotal: DataItem = DataItem("Total Transfers")  # int = 0

        # required Minimal distributions
        self.clientRMD: DataItem = DataItem("Client RMDs")  # int = 0
        self.clientRMDPercent: DataItem = PercentDataItem("% Client RMDs")

        self.spouseRMD: DataItem = DataItem("Spouse RMDs")  # int = 0
        self.spouseRMDPercent: DataItem = PercentDataItem("% Spouse RMDs")

        self.totalRMD: DataItem = DataItem("Total RMDs")  # int = 0
        self.totalRMDPercent: DataItem = PercentDataItem("% Total RMDs")

        # surplus account
        self.surplusBalance: DataItem = DataItem("Surplus Acct. Balance")  # int = 0
        self.surplusWithdraw: DataItem = DataItem("Surplus Acct. Withdraw")  # int = 0

        self.FPL: DataItem = PercentDataItem("FPL", default_data=0.0)
        self.AW: DataItem = DataItem(
            "Total Asset Drawdown"
        )  # TAD = Total Asset Drawdown
        self.AWR: DataItem = PercentDataItem("Asset DrawDown Rate")


class Projections(QRunnable):
    def __init__(self, dv: DataVariables):
        super(Projections, self).__init__()

        self.signals = WorkerSignals()
        # can set this to see todays dollars
        self.InTodaysDollars = dv.inTodaysDollars

        self.InputVariables = dv  # these are the variables from the input form.

        if dv.inTodaysDollars:
            self._inflation = dv.inflation
        else:  # think about removing this.. it doesn't make sense to look at things in future dollars
            self._inflation = 0

        self.UseSurplusAccount = dv.SurplusAccount
        self.SurplusAccountInterestRate = dv.SurplusAccountInterestRate

        _is_married = dv.relationStatus == RelationStatusType.MARRIED

        self._begin_year = (
            dv.start_year if dv.start_year is not None else datetime.now().year
        )

        self._end_year = self._begin_year + dv.forecastYears

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
                Person=self._client,
                FRAAmount=dv.clientSSAmount,
                Owner=PersonType.CLIENT,
                BirthDate=dv.clientBirthDate,
                BeginAge=dv.clientSSBeginAge,
                LifeSpanAge=dv.clientLifeSpanAge,
                COLA=dv.ssCola,
            )
            self._IncomeSources.append(_client_ss)

        if _is_married:
            if dv.spouseSSAmount is not None:
                _spouse_ss = SocialSecurity(
                    Name="Spouse Social Security",
                    Person=self._spouse,
                    FRAAmount=dv.spouseSSAmount,
                    Owner=PersonType.SPOUSE,
                    BirthDate=dv.spouseBirthDate,
                    BeginAge=dv.spouseSSBeginAge,
                    LifeSpanAge=dv.spouseLifeSpanAge,
                    COLA=dv.ssCola,
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
            if dv.pension1Owner == PersonType.SPOUSE:
                _birthdate = dv.spouseBirthDate
                _lifespan = dv.spouseLifeSpanAge

            _period = PeriodValidator(
                _birthdate.year, dv.pension1BeginAge, min(_lifespan, dv.pension1EndAge)
            )

            _is = IncomeSource(
                Name=dv.pension1Name,
                IncomeType=IncomeSourceType.PENSION,
                Owner=dv.pension1Owner,
                Amount=dv.pension1Amount,
                Period=_period,
                # SurvivorPercent=dv.pension1SurvivorBenefits,
                COLA=dv.pension1Cola,
            )

            self._IncomeSources.append(_is)

        if dv.pension2Name is not None and dv.pension2Name.strip() != "":
            _birthdate = dv.clientBirthDate
            _lifespan = dv.clientLifeSpanAge
            if dv.pension2Owner == PersonType.SPOUSE:
                _birthdate = dv.spouseBirthDate
                _lifespan = dv.spouseLifeSpanAge

            _period = PeriodValidator(
                _birthdate.year, dv.pension2BeginAge, min(_lifespan, dv.pension2EndAge)
            )

            _is = IncomeSource(
                Name=dv.pension2Name,
                IncomeType=IncomeSourceType.PENSION,
                Owner=dv.pension2Owner,
                Amount=dv.pension2Amount,
                Period=_period,
                # SurvivorPercent=dv.pension2SurvivorBenefits,
                COLA=dv.pension2Cola,
            )

            self._IncomeSources.append(_is)

        for _record in dv.otherIncomes:
            _birthdate = dv.clientBirthDate
            if _record.owner == PersonType.SPOUSE:
                _birthdate = dv.spouseBirthDate

            if _record.amount is not None:
                _period = PeriodValidator(
                    _birthdate.year, _record.begin_age, _record.end_age
                )

                _is = IncomeSource(
                    Name=_record.descr,
                    IncomeType=IncomeSourceType.EMPLOYMENT,
                    Amount=_record.amount,
                    Owner=_record.owner,
                    Period=_period,
                    COLA=_record.COLA,
                )
                self._IncomeSources.append(_is)
            else:
                logger.Error(
                    "Income Source '%s' not used since amount not set" % _record.descr
                )

        self._Expenses = []
        for _record in dv.expenses:
            _birthdate = dv.clientBirthDate
            # make sure to check that expense owner is client if we select single (on basic info tab)
            # instead of married after we populate expenses in reference to spouse info (ie, birthdate).
            if _record.owner == PersonType.SPOUSE:
                _birthdate = dv.spouseBirthDate

            if _record.amount is not None:
                _period = PeriodValidator(
                    _birthdate.year, _record.begin_age, _record.end_age
                )

                _e = Expense(
                    _record.descr,
                    _record.amount,
                    Period=_period,
                    COLA=_record.COLA,
                )

                self._Expenses.append(_e)
            else:
                if _record.amount is None:
                    logger.Error(
                        "Expense '%s' not used since amount not set" % _record._descr
                    )

        self._Assets = []

        # create all basic accounts.. even if they have a zero balance. Someone may
        # transfer money into an account with zero balance

        _con = ContributionClass(
            dv.clientIRAContribution,
            dv.clientBirthDate.year,
            dv.clientIRAContributionBeginAge,
            dv.clientIRAContributionEndAge,
        )
        self._Assets.append(
            TraditionalIRA(
                Name="Client Trad IRA",
                Owner=AccountOwnerType.CLIENT,
                Balance=dv.clientIRABalance,
                InterestRate=dv.clientIRACola,
                ContributionObj=_con,
            )
        )

        _con = ContributionClass(
            dv.clientRothContribution,
            dv.clientBirthDate.year,
            dv.clientRothContributionBeginAge,
            dv.clientRothContributionEndAge,
        )

        self._Assets.append(
            RothIRA(
                Name="Client Roth IRA",
                Owner=AccountOwnerType.CLIENT,
                Balance=dv.clientRothBalance,
                InterestRate=dv.clientRothCola,
            )
        )

        if _is_married:
            _con = ContributionClass(
                dv.spouseIRAContribution,
                dv.spouseBirthDate.year,
                dv.spouseIRAContributionBeginAge,
                dv.spouseIRAContributionEndAge,
            )

            self._Assets.append(
                TraditionalIRA(
                    Name="Spouse Trad IRA",
                    Owner=AccountOwnerType.SPOUSE,
                    Balance=dv.spouseIRABalance,
                    InterestRate=dv.spouseIRACola,
                    ContributionObj=_con,
                )
            )

            _con = ContributionClass(
                dv.spouseRothContribution,
                dv.spouseBirthDate.year,
                dv.spouseRothContributionBeginAge,
                dv.spouseRothContributionEndAge,
            )

            self._Assets.append(
                RothIRA(
                    Name="Spouse Roth IRA",
                    Owner=AccountOwnerType.SPOUSE,
                    Balance=dv.spouseRothBalance,
                    InterestRate=dv.spouseRothCola,
                    ContributionObj=_con,
                )
            )

        _con = ContributionClass(
            dv.regularContribution,
            dv.clientBirthDate.year,
            dv.regularContributionBeginAge,
            dv.regularContributionEndAge,
        )

        self._Assets.append(
            Brokerage(
                Name="Regular Taxable",
                Owner=AccountOwnerType.BOTH,
                Balance=dv.regularBalance,
                InterestRate=dv.regularCola,
                ContributionObj=_con,
            )
        )

        # put transfer stuff here.. if an account does not exist, create it and add it to the
        # self._Assets variable...
        self._Transfers = []
        for _transfer in dv.transfers:
            # identify the source and target assets.
            # make sure the source and target assets are in the self._Assets list, if not, create
            # the asset there with a balance of 0.  #what COLA (interest rate) should we use?
            _src_acct = None
            _tgt_acct = None
            for _asset in self._Assets:
                if _asset.Name == _transfer.src_acct:
                    _src_acct = _asset
                elif _asset.Name == _transfer.tgt_acct:
                    _tgt_acct = _asset

            assert _src_acct is not None
            assert _tgt_acct is not None

            # create a transfer object, which contains the source and target assets as well as
            # the amount to transfer, interest, and the begin and end years.
            # maybe look at adding a variable to see if we should do the transfer at the beginning
            # of the period or at the end. (I don't know if this really makes a difference).

            if _transfer.person == PersonType.CLIENT:
                _person = self._client
            elif _transfer.person == PersonType.SPOUSE:
                _person = self._spouse

            self._Transfers.append(
                TransferAssets(
                    _transfer.descr,
                    _src_acct,
                    _tgt_acct,
                    _transfer.amount,
                    _transfer.COLA,
                    _person,
                    _transfer.beginAge,
                    _transfer.endAge,
                )
            )

        self._federal_tax_status = dv.federalFilingStatus
        self._federal_tax_status_once_widowed = dv.federalFilingStatusOnceWidowed

    @pyqtSlot()
    def run(self):
        _projection_data = []

        _regularAccount = self._retrieve_asset_object(
            AccountOwnerType.BOTH, AccountType.REGULAR
        )
        # _surplusAccount=None
        if self.UseSurplusAccount:
            _surplusAccount = SurplusAccount(0, self.SurplusAccountInterestRate)
        else:  # use brokerage as surplus account
            _surplusAccount = _regularAccount

        if _surplusAccount is None:
            print("Surplus Account is None")

        _clientRMD = RMDTable(self._client, self._spouse)
        _spouseRMD = None
        if self._spouse is not None:
            _spouseRMD = RMDTable(self._spouse, self._client)

        _client_ira = self._retrieve_asset_object(
            AccountOwnerType.CLIENT, AccountType.TAXDEFERRED
        )
        if _client_ira is None:
            print("Error! Client IRA Account not found...")

        _rmd_client = RMDCalcs(_client_ira, _surplusAccount)

        _spouse_ira = self._retrieve_asset_object(
            AccountOwnerType.SPOUSE, AccountType.TAXDEFERRED
        )
        if _spouse_ira is not None:
            _rmd_spouse = RMDCalcs(_spouse_ira, _surplusAccount)
        # else:
        #    print("Error! Spouse IRA Account not found...")

        _lastYearsFederalTaxes = 0
        for _year in range(self._begin_year, self._end_year):
            _number_of_years = _year - self._begin_year
            # reset some asset variables (deposits, withdraws, taxable_income, ltcg_income, etc)
            for _asset in self._Assets:
                _asset.beginning_of_year_bookkeeping()

            if self.UseSurplusAccount:
                _surplusAccount.beginning_of_year_bookkeeping()

            _pyd = ProjectionYearData(_year)
            _pyd.lastYearsFederalTaxes.data = _lastYearsFederalTaxes
            # fix me
            _last_day_of_year = date(
                _year, 12, 31
            )  # used for rmds.. (should year by least year (year-1)?

            _clientage = self._client.calc_age_by_year(_year)
            _clientIsAlive = _clientage <= self._client.lifeSpanAge
            _pyd.clientAge = _clientage
            _pyd.clientIsAlive = _clientIsAlive

            if _clientage == self._client.lifeSpanAge + 1:
                # should set client RMD to spouse
                _clientRMD.death_event(self._client)

            _spouseage = None
            _spouseIsAlive = False
            if self._spouse is not None:
                _spouseage = self._spouse.calc_age_by_year(_year)
                _spouseIsAlive = _spouseage <= self._spouse.lifeSpanAge
                _pyd.spouseAge = _spouseage
                _pyd.spouseIsAlive = _spouseIsAlive

                if _spouseage == self._spouse.lifeSpanAge + 1:
                    _spouseRMD.death_event(self._spouse)

            # check to see if client (and spouse) are dead...
            # if both client (and spouse) are dead, we don't need to calcuate things further for this year
            if not _clientIsAlive:
                if self._client.relationship == RelationStatusType.SINGLE:
                    _projection_data.append(_pyd)
                    continue
                elif not _spouseIsAlive:
                    _projection_data.append(_pyd)
                    continue

            # at least one person is still alive...  do the projection for that year...
            if not _clientIsAlive or not _spouseIsAlive:
                _pyd.federalTaxFilingStatus.data = self._federal_tax_status_once_widowed
            else:
                _pyd.federalTaxFilingStatus.data = self._federal_tax_status

            _taxable_income_total = 0
            _income_total = 0
            _ss_income_total = 0
            for _src in self._IncomeSources:
                _income = _src.calc_income_by_year(_year, self._inflation)
                _ss_income_total += _src.ss_income
                _pyd.incomeSources.append(DataItem(_src.Name, "${:,}", _income))

                _income_total += _income  # _src.calc_income_by_year(_year)
                _taxable_income_total += _src.taxable_income

            _pyd.activeIncomeTotal.data = _income_total
            _pyd.ssIncomeTotal.data = _ss_income_total

            _pyd.expenseTotal.data = 0
            for _src in self._Expenses:
                _expense = _src.calc_balance_by_year(_year, self._inflation)
                _pyd.expenseSources.append(DataItem(_src.Name, "${:,}", _expense))

                _pyd.expenseTotal.data += _expense

            _pyd.expenseTotal.data += _pyd.lastYearsFederalTaxes.data

            _pyd.netIncome.data = (
                _pyd.activeIncomeTotal.data
                + _pyd.ssIncomeTotal.data
                - _pyd.expenseTotal.data
            )

            # do transfers between accounts
            # print("Transfers")
            for _tran in self._Transfers:
                _tran.do_transfer(_year)
                _pyd.transfersTotal.data += _tran.transferred_amount
                _taxable_income_total += _tran.taxable_income
                # print(_tran._descr, _tran.taxable_income)

            # maybe call it RMD amount needed??? RMCCalcs?
            # all of this RMD stuff should be its own class (figure out which vars are needed, etc)
            # _pyd.clientRMDPercent.data = 0
            # _pyd.clientRMD.data = 0
            # _client_boy_balance=0

            # _client_ira=_retrieve_asset_object(AccountOwner.CLIENT, AccountType.TAXDEFERRED)
            # _rmd_client=RMDCalcs(_client_ira)
            _rmd_pct = _clientRMD.calcPercent(_last_day_of_year)
            _pyd.clientRMD.data, _pyd.clientRMDPercent.data, _client_boy_balance = (
                _rmd_client.calcRequiredAmount(_rmd_pct)
            )
            _rmd_client.do_transfer_if_necessary()

            if _spouseRMD is not None:
                _rmd_pct = _spouseRMD.calcPercent(_last_day_of_year)
                _pyd.spouseRMD.data, _pyd.spouseRMDPercent.data, _spouse_boy_balance = (
                    _rmd_spouse.calcRequiredAmount(_rmd_pct)
                )
                _rmd_spouse.do_transfer_if_necessary()
            else:
                _pyd.spouseRMD.data = 0
                _pyd.spouseRMDPercent.data = 0
                _spouse_boy_balance = 0

            _pyd.totalRMD.data = _pyd.clientRMD.data + _pyd.spouseRMD.data
            if _client_boy_balance + _spouse_boy_balance == 0:
                _pyd.totalRMDPercent.data = 0.0
            else:
                _pyd.totalRMDPercent.data = (
                    100.0
                    * _pyd.totalRMD.data
                    / (_client_boy_balance + _spouse_boy_balance)
                )

            # contributions..
            _contribution_total = 0
            for _src in self._Assets:
                # running this does the contributions for all accounts in self._Assets
                _contribution_total += _src.do_contribution(
                    _year, _number_of_years, self._inflation
                )

            if _contribution_total > 0:  # need to pull this money somewhere...
                if _pyd.netIncome.data >= _contribution_total:
                    _pyd.netIncome.data -= _contribution_total
                elif _pyd.netIncome.data > 0:
                    _contribution_total -= _pyd.netIncome.data
                    _pyd.netIncome.data = 0

                if _contribution_total > 0:  # we still need to pull from wherewhere...
                    if self.UseSurplusAccount:
                        _contribution_total = _surplusAccount.withdraw(
                            _contribution_total
                        )

                    # earney
                    _contribution_total = _regularAccount.withdraw(_contribution_total)
                    assert _contribution_total == 0

            # fix this mess..
            if _pyd.netIncome.data < 0:
                # we need to withdraw money from assets to make up for the cash flow deficit
                _ws = WithdrawStrategy(
                    self._withdrawOrder,
                    _clientage,
                    _clientIsAlive,
                    _spouseage,
                    _spouseIsAlive,
                    self._Assets,
                )
                _neededAssetWithdraw = abs(_pyd.netIncome.data)
                _deficit = _ws.reconcile_required_withdraw(_neededAssetWithdraw)

                if _deficit < 0:
                    # we need to take the deficit from somewhere ..
                    _deficit = _surplusAccount.withdraw(-_deficit)
                    assert _deficit == 0

            for _src in self._Assets:
                _src.calc_interest(self._inflation)
                _src.end_of_year_bookkeeping()

                _pyd.assetTotalBalance.data += _src.balance
                _pyd.assetTotalDeposits.data += _src.totalDeposits
                _pyd.assetTotalWithdraws.data += _src.totalWithdraws
                _pyd.assetTotalReturns.data += _src.interest
                _pyd.assetTotalContributions.data += _src.contributions

                _pyd.assetSources.append(DataItem(_src.Name, "${:,}", _src.balance))

                match _src.Type:
                    case AccountType.TAXDEFERRED:
                        _pyd.assetTaxDeferredWithdraws.data += _src.totalWithdraws
                    case AccountType.TAXFREE:
                        _pyd.assetTaxFreeWithdraws.data += _src.totalWithdraws
                    case AccountType.REGULAR:
                        _pyd.assetRegularReturns.data += _src.interest
                    case _:
                        print("Error invalid AccountType %s" % (_src.Type))

            _pyd.assetTotalNetDeposits.data = _pyd.assetTotalDeposits.data
            _pyd.assetTotalNetDeposits.data -= _pyd.assetTotalWithdraws.data

            _pyd.assetTotalCashFlow.data = _pyd.assetTotalNetDeposits.data
            _pyd.assetTotalCashFlow.data += _pyd.assetTotalContributions.data
            _pyd.assetTotalCashFlow.data += _pyd.assetTotalReturns.data

            _pyd.incomeTotal.data = _income_total + _pyd.assetRegularReturns.data

            _pyd.taxableIncomeTotal.data = (
                _pyd.incomeTotal.data + _pyd.assetTaxDeferredWithdraws.data
            )

            # this is where we figure out the SS Taxes based on our total income for the year
            if _pyd.ssIncomeTotal.data > 0:
                if self.InTodaysDollars:
                    _num = _pyd.projectionYear.data - _year
                    _inflation = self.InputVariables.ssCola
                else:
                    # we don't need to adjust the values since they are already
                    # in the dollars amounts for the given year.
                    _num = 0
                    _inflation = 0
                # just a note, the taxableIncomeTotal value is usually a combination
                # of income from different sources, a job, social security,
                # account interest, etc..  Should we use the same inflation
                # value for all these different income sources??  The solution
                # for this maybe to create a variable with this years real dollar
                # amount that takes the different sources of income inflation
                # into consideration.. For now, just use the SS cola for this.
                # SS Cola and inflation should be about the same.
                _sst = SocialSecurityTaxes(
                    todays_amount(_pyd.taxableIncomeTotal.data, _inflation, _num),
                    todays_amount(_pyd.ssIncomeTotal.data, _inflation, _num),
                    _pyd.federalTaxFilingStatus.data,
                )
                _pyd.ssTaxRate.data = _sst.percent_taxable()
                _pyd.ssTaxableIncome.data = todays_amount(
                    _sst.taxable(), -_inflation, _num
                )
            else:
                _pyd.ssTaxableIncome.data = 0
                _pyd.ssTaxRate.data = 0.0

            # federal poverty level...
            _fpl = FederalPovertyLevel(2 if _spouseIsAlive else 1)
            _pyd.FPL.data = _fpl.calc_percent(
                _pyd.incomeTotal.data
            )  # + _pyd.assetTaxDeferredWithdraw)

            # federal taxes
            # fix me!
            _ft = FederalTax(_pyd.federalTaxFilingStatus.data)
            _pyd.thisYearsFederalTaxes.data = _ft.calc_taxes(
                max(_pyd.taxableIncomeTotal.data - _ft.StandardDeduction, 0)
            )

            # fix me!  I don't think long term capital gains is calculated this way..
            # I believe it is calculated on top of your income..
            # _pyd.longTermCapitalGainsTaxes.data = _ft.calc_ltcg_taxes(
            #    _withdraw_dict[AccountType.REGULAR] + _pyd.surplusWithdraw.data
            # )
            # _pyd.thisYearsFederalTaxes.data = (
            #    _pyd.thisYearsFederalTaxes.data + _pyd.longTermCapitalGainsTaxes.data
            # )

            _pyd.federalEffectiveTaxRate.data = _ft.effective_tax_rate(
                _pyd.thisYearsFederalTaxes.data, _pyd.taxableIncomeTotal.data
            )

            _pyd.federalMarginalTaxRate.data = _ft.marginal_tax_rate(
                _pyd.taxableIncomeTotal.data
            )

            if self.UseSurplusAccount:
                # calculate interest??
                _surplusAccount.calc_interest(self._inflation)

            _pyd.AW.data = -_pyd.assetTotalNetDeposits.data

            if _pyd.assetTotalBalance.data == 0:
                _pyd.AWR.data = 0.0
            else:
                _pyd.AWR.data = 100.0 * _pyd.AW.data / _pyd.assetTotalBalance.data

            _lastYearsFederalTaxes = _pyd.thisYearsFederalTaxes.data

            _projection_data.append(_pyd)

        self.signals.result.emit(_projection_data)

    def _retrieve_asset_object(self, owner: AccountOwnerType, accountType: AccountType):
        for _src in self._Assets:
            if _src.Owner == owner and _src.Type == accountType:
                return _src

        # cannot find Account.. returning None
        return None
