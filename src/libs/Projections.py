from datetime import datetime, date

from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot

from .Account import TraditionalIRA, RothIRA, Brokerage
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
from .Person import Person
from .ProvisionalIncome import SocialSecurityTaxes
from .RequiredMinimalDistributions import RMD
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
        return self._format.format(self._data)


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
        self.taxableIncomeTotal: DataItem = DataItem("Taxable Income Total")
        self.incomeTotal: DataItem = DataItem("Income Total")
        self.activeIncomeTotal: DataItem = DataItem("Active Income Total")
        self.FPL: DataItem = DataItem("FPL", "{:.1f}%", 0.0)  # float = 0.0

        self.ssIncomeTotal: DataItem = DataItem("SS Income Total")  # int = 0
        self.ssTaxableIncome: DataItem = DataItem("SS Taxable Income")  # int = 0
        self.ssTaxRate: DataItem = DataItem("SS Tax Rate", "{:.1f}%")

        self.expenseSources = []
        self.expenseTotal: DataItem = DataItem("Expense Total")  # int = 0

        self.cashFlow: DataItem = DataItem(
            "Cash Flow"
        )  # int = 0  # income total - expense total - - lastYearsFederal Taxes - asset contributions
        self.surplusDeficit: DataItem = DataItem(
            "Surplus Deficit"
        )  # int = 0  # cashFlow - assetWithdraws

        # todo format of output for this needs to be fixed. (see Tax Table output)
        self.federalTaxFilingStatus: DataItem = DataItem(
            "Federal Tax Filing Status", "{.value}", None
        )
        # FederalTaxStatusType = None
        self.thisYearsFederalTaxes: DataItem = DataItem(
            "This Years Federal Taxes"
        )  # int = 0
        self.lastYearsFederalTaxes: DataItem = DataItem(
            "Last Years Federal Taxes"
        )  # int = 0

        self.federalEffectiveTaxRate: DataItem = DataItem(
            "Federal Effective Tax Rate", "{:.1f}%"
        )
        self.federalMarginalTaxRate: DataItem = DataItem(
            "Federal Marginal Tax Rate", "{:.1f}%"
        )

        self.longTermCapitalGainsTaxes: DataItem = DataItem("LTCG Taxes")  # int = 0

        # cash flow is just incometotal-expenseTotal - federaltaxes

        # how much we had to pull from assets because expenses > income
        self.assetWithdraw: DataItem = DataItem("Total Asset Withdraws")  # int = 0
        self.assetTaxDeferredWithdraw: DataItem = DataItem(
            "Tax Deferred Asset Withdraws"
        )  # int = 0
        self.assetRegularWithdraw: DataItem = DataItem(
            "Regular Asset Withdraws"
        )  # int = 0
        self.assetTaxFreeWithdraw: DataItem = DataItem(
            "Tax Free Asset Withdraws"
        )  # int = 0

        # self.surplus_deficit: int = 0

        self.assetSources = []
        self.assetContributions = []

        self.assetTotal: DataItem = DataItem("Total Assets")  # int = 0
        self.assetContributionTotal: DataItem = DataItem("Total Asset Contributions")

        self.transfersTotal: DataItem = DataItem("Total Transfers")  # int = 0

        # required Minimal distributions
        self.clientRMD: DataItem = DataItem("Client RMDs")  # int = 0
        self.clientRMDPercent: DataItem = DataItem(
            "% Client RMDs", "{:.1f}%"
        )  # float = 0.0

        self.spouseRMD: DataItem = DataItem("Spouse RMDs")  # int = 0
        self.spouseRMDPercent: DataItem = DataItem(
            "% Spouse RMDs", "{:.1f}%"
        )  # float = 0.0

        self.totalRMD: DataItem = DataItem("Total RMDs")  # int = 0
        self.totalRMDPercent: DataItem = DataItem(
            "% Total RMDs", "{:.1f}%"
        )  # float = 0.0

        # surplus account
        self.surplusBalance: DataItem = DataItem("Surplus Account")  # int = 0
        self.surplusWithdraw: DataItem = DataItem("Surplus Withdraw")  # int = 0

        self.AW: DataItem = DataItem(
            "Total Asset Drawdown"
        )  # int = 0  # TAD = Total Asset Drawdown
        self.AWR: DataItem = DataItem("Asset DrawDown Rate", "{:.1f}%")  # float = 0


class Projections(QRunnable):
    def __init__(self, dv: DataVariables):
        super(Projections, self).__init__()

        self.signals = WorkerSignals()
        # can set this to see todays dollars
        self.InTodaysDollars = dv.inTodaysDollars

        self.InputVariables = dv  # these are the variables from the input form.

        if dv.inTodaysDollars:
            self._inflation = dv.inflation
        else:
            self._inflation = 0

        self.UseSurplusAccount = dv.SurplusAccount
        # print(self.UseSurplusAccount)
        self.SurplusAccountInterestRate = dv.SurplusAccountInterestRate

        _is_married = dv.relationStatus == RelationStatusType.MARRIED

        self._begin_year = (
            dv.start_year if dv.start_year is not None else datetime.now().year
        )

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
                BirthDate=dv.clientBirthDate,
                FRAAmount=dv.clientSSAmount,
                Owner=PersonType.CLIENT,
                BeginAge=dv.clientSSBeginAge,
                LifeSpanAge=dv.clientLifeSpanAge,
                COLA=dv.ssCola - self._inflation,
            )
            self._IncomeSources.append(_client_ss)

        if _is_married:
            if dv.spouseSSAmount is not None:
                _spouse_ss = SocialSecurity(
                    Name="Spouse Social Security",
                    Person=self._spouse,
                    BirthDate=dv.spouseBirthDate,
                    FRAAmount=dv.spouseSSAmount,
                    Owner=PersonType.SPOUSE,
                    BeginAge=dv.spouseSSBeginAge,
                    LifeSpanAge=dv.spouseLifeSpanAge,
                    COLA=dv.ssCola - self._inflation,
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

            _is = IncomeSource(
                Name=dv.pension1Name,
                IncomeType=IncomeSourceType.PENSION,
                Owner=dv.pension1Owner,
                Amount=dv.pension1Amount,
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
            if dv.pension2Owner == PersonType.SPOUSE:
                _birthdate = dv.spouseBirthDate
                _lifespan = dv.spouseLifeSpanAge

            _is = IncomeSource(
                Name=dv.pension2Name,
                IncomeType=IncomeSourceType.PENSION,
                Owner=dv.pension2Owner,
                Amount=dv.pension2Amount,
                BirthDate=_birthdate,
                BeginAge=dv.pension2BeginAge,
                SurvivorPercent=dv.pension2SurvivorBenefits,
                COLA=dv.pension2Cola - self._inflation,
            )
            self._IncomeSources.append(_is)

        for _record in dv.otherIncomes:
            _birthdate = dv.clientBirthDate
            if _record.owner == PersonType.SPOUSE:
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
                    IncomeSourceType.EMPLOYMENT,
                    _record.amount,
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
            if _record.owner == PersonType.SPOUSE:
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

        if dv.clientIRACola is None:
            _interest = -self._inflation
        else:
            _interest = dv.clientIRACola - self._inflation

        self._Assets.append(
            TraditionalIRA(
                Name="Client Trad IRA",
                Owner=AccountOwnerType.CLIENT,
                BirthDate=dv.clientBirthDate,
                Balance=dv.clientIRABalance,
                InterestRate=_interest,
                Contribution=dv.clientIRAContribution,
                ContributionBeginAge=dv.clientIRAContributionBeginAge,
                ContributionEndAge=dv.clientIRAContributionEndAge,
            )
        )

        if dv.clientRothIRACola is None:
            _interest = -self._inflation
        else:
            _interest = dv.clientRothIRACola - self._inflation

        self._Assets.append(
            RothIRA(
                Name="Client Roth IRA",
                Owner=AccountOwnerType.CLIENT,
                BirthDate=dv.clientBirthDate,
                Balance=dv.clientRothIRABalance,
                InterestRate=_interest,
                Contribution=dv.clientRothContribution,
                ContributionBeginAge=dv.clientRothContributionBeginAge,
                ContributionEndAge=dv.clientRothContributionEndAge,
            )
        )

        if dv.spouseIRACola is None:
            _interest = -self._inflation
        else:
            _interest = dv.spouseIRACola - self._inflation

        self._Assets.append(
            TraditionalIRA(
                Name="Spouse Trad IRA",
                Owner=AccountOwnerType.SPOUSE,
                Balance=dv.spouseIRABalance,
                BirthDate=dv.spouseBirthDate,
                InterestRate=_interest,
                Contribution=dv.spouseIRAContribution,
                ContributionBeginAge=dv.spouseIRAContributionBeginAge,
                ContributionEndAge=dv.spouseIRAContributionEndAge,
            )
        )

        if dv.spouseRothIRACola is None:
            _interest = -self._inflation
        else:
            _interest = dv.spouseRothIRACola - self._inflation
        self._Assets.append(
            RothIRA(
                Name="Spouse Roth IRA",
                Owner=AccountOwnerType.SPOUSE,
                BirthDate=dv.spouseBirthDate,
                Balance=dv.spouseRothIRABalance,
                InterestRate=_interest,
                Contribution=dv.spouseRothContribution,
                ContributionBeginAge=dv.spouseRothContributionBeginAge,
                ContributionEndAge=dv.spouseRothContributionEndAge,
            )
        )

        if dv.regularCola is None:
            _interest = -self._inflation
        else:
            _interest = dv.regularCola - self._inflation
        self._Assets.append(
            Brokerage(
                Name="Regular Taxable",
                Owner=AccountOwnerType.BOTH,
                BirthDate=dv.clientBirthDate,
                Balance=dv.regularBalance,
                InterestRate=_interest,
                Contribution=dv.regularContribution,
                ContributionBeginAge=dv.regularContributionBeginAge,
                ContributionEndAge=dv.regularContributionEndAge,
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
                # _income = _src.calc_balance_by_year(_year)
                if _src.IncomeType == IncomeSourceType.SOCIAL_SECURITY:
                    _income = _src.calc_balance_by_year(_year)
                    _ss_income_total += _income
                else:
                    _income = _src.calc_balance_by_year(_year)

                _pyd.incomeSources.append(DataItem(_src.Name, "${:,}", _income))

                _income_total += _income  # _src.calc_income_by_year(_year)
                _taxable_income_total += _income

            _pyd.activeIncomeTotal.data = _income_total
            _pyd.ssIncomeTotal.data = _ss_income_total

            _expense_total = 0
            for _src in self._Expenses:
                _expense = _src.calc_balance_by_year(_year)
                _pyd.expenseSources.append(DataItem(_src.Name, "${:,}", _expense))

                _expense_total += _expense
            _pyd.expenseTotal.data = _expense_total

            _total = 0
            _client_ira_total = 0
            _spouse_ira_total = 0
            _contribution_total = 0
            for _src in self._Assets:
                _balance, _contribution = _src.calc_balance(year=_year)

                if _src.Contribution is not None and _src.Contribution != 0:
                    _pyd.assetContributions[_src.Name] = _contribution
                    _contribution_total += _contribution

                _pyd.assetSources.append(DataItem(_src.Name, "${:,}", _balance))

                if _src.Type == AccountType.TAXDEFERRED:
                    if _src.Owner == AccountOwnerType.CLIENT:
                        _client_ira_total += _balance
                    elif _src.Owner == AccountOwnerType.SPOUSE:
                        _spouse_ira_total += _balance

                _total += _balance

            _pyd.assetTotal.data = _total
            _pyd.assetContributionTotal.data = _contribution_total

            # do transfers between accounts
            for _tran in self._Transfers:
                _tran.do_transfer(_year)
                _pyd.transfersTotal.data = _tran.transferred_amount
                _taxable_income_total += _tran.taxable_income

            # do RMD calcs
            _last_day_of_year = date(_year, 12, 31)
            _rmd_pct = _clientRMD.calc(_last_day_of_year)
            _pyd.clientRMDPercent.data = _rmd_pct
            _pyd.clientRMD.data = int(_rmd_pct / 100.0 * _client_ira_total)

            if self._spouse is not None:
                _rmd_pct = _spouseRMD.calc(_last_day_of_year)
                _pyd.spouseRMDPercent.data = _rmd_pct
                _pyd.spouseRMD.data = int(_rmd_pct / 100.0 * _spouse_ira_total)

            _pyd.totalRMD.data = _pyd.clientRMD.data + _pyd.spouseRMD.data
            if _client_ira_total + _spouse_ira_total == 0:
                _pyd.totalRMDPercent.data = 0.0
            else:
                _pyd.totalRMDPercent.data = (
                    100.0 * _pyd.totalRMD.data / (_client_ira_total + _spouse_ira_total)
                )

            _pyd.cashFlow.data = (
                _income_total
                - _expense_total
                - _lastYearsFederalTaxes
                - _contribution_total
            )

            if _pyd.cashFlow.data < 0 or _pyd.totalRMD.data > 0:
                # we need to withdraw money from assets to make up for the cash flow deficit
                _ws = WithdrawStrategy(
                    self._withdrawOrder,
                    _clientage,
                    _clientIsAlive,
                    _spouseage,
                    _spouseIsAlive,
                    self._Assets,
                )
                _neededAssetWithdraw = max(abs(_pyd.cashFlow.data), _pyd.totalRMD.data)
                _deficit, _withdraw_dict = _ws.reconcile_required_withdraw(
                    _neededAssetWithdraw
                )

                _pyd.assetWithdraw.data = 0
                _pyd.assetTaxDeferredWithdraw.data = _withdraw_dict[
                    AccountType.TAXDEFERRED
                ]
                _pyd.assetRegularWithdraw.data = _withdraw_dict[AccountType.REGULAR]
                _pyd.assetTaxFreeWithdraw.data = _withdraw_dict[AccountType.TAXFREE]

                for _asset_type, _amount in _withdraw_dict.items():
                    _pyd.assetWithdraw.data += _amount
                    if (
                        _asset_type == AccountType.TAXDEFERRED
                    ):  # these withdraws are seen as regular income
                        _income_total += _amount
                        _taxable_income_total += _amount
                        # print(_amount)

                # _pyd.surplusDeficit = _pyd.cashFlow + _pyd.assetWithdraw - _deficit
            else:
                _pyd.assetWithdraw.data = 0
                _pyd.assetTaxDeferredWithdraw.data = 0
                _pyd.assetRegularWithdraw.data = 0
                _pyd.assetTaxFreeWithdraw.data = 0

                _deficit = 0
                # _pyd.surplusDeficit = _pyd.cashFlow
                _withdraw_dict = {
                    AccountType.REGULAR: 0,
                    AccountType.TAXDEFERRED: 0,
                }  # no withdraws...
                # _income_total = 0

            _pyd.taxableIncomeTotal.data = _taxable_income_total
            _pyd.incomeTotal.data = _income_total

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
            _pyd.surplusDeficit.data = (
                _pyd.cashFlow.data + _pyd.assetWithdraw.data
            )  # - _deficit

            # _pyd.cashFlow -= _contribution_total
            # _pyd.surplusDeficit -= _contribution_total

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

            # _surplusWithdraw = 0
            if self.UseSurplusAccount:
                _surplusAccount.add_interest()
                # should we calculate this years interest after deposits/withdraws or before?
                # does it really matter?

                if _pyd.surplusDeficit.data < 0:
                    _pyd.surplusWithdraw.data, _pyd.surplusDeficit.data = (
                        _surplusAccount.withdraw(abs(_pyd.surplusDeficit.data))
                    )
                    _pyd.assetWithdraw.data += _pyd.surplusWithdraw.data
                else:
                    _surplusAccount.deposit(_pyd.surplusDeficit.data)
                    _pyd.surplusWithdraw.data = 0

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
                _pyd.surplusBalance.data = _surplusAccount.balance
                _pyd.assetTotal.data += _pyd.surplusBalance.data

            # federal poverty level...
            _fpl = FederalPovertyLevel(2 if _spouseIsAlive else 1)
            _pyd.FPL.data = _fpl.calc_percent(
                _pyd.incomeTotal.data
            )  # + _pyd.assetTaxDeferredWithdraw)

            # federal taxes
            # fix me!
            _ft = FederalTax(_pyd.federalTaxFilingStatus.data, 2024)
            # _taxable_income = (
            #    _income_total - _ss_income_total + _pyd.ssTaxableIncome
            # )  # + _surplusWithdraw

            # print(_year, _income_total, _ss_income_total, _pyd.ssTaxableIncome) #, _surplusWithdraw)
            # _pyd.taxableIncome = _taxable_income

            _pyd.thisYearsFederalTaxes.data = _ft.calc_taxes(
                # max(_taxable_income - _ft.StandardDeduction, 0)
                max(_pyd.taxableIncomeTotal.data - _ft.StandardDeduction, 0)
            )
            _pyd.longTermCapitalGainsTaxes.data = _ft.calc_ltcg_taxes(
                _withdraw_dict[AccountType.REGULAR] + _pyd.surplusWithdraw.data
            )
            _pyd.thisYearsFederalTaxes.data = (
                _pyd.thisYearsFederalTaxes.data + _pyd.longTermCapitalGainsTaxes.data
            )

            _pyd.lastYearsFederalTaxes.data = _lastYearsFederalTaxes
            _lastYearsFederalTaxes = _pyd.thisYearsFederalTaxes.data

            _pyd.federalEffectiveTaxRate.data = _ft.effective_tax_rate(
                _pyd.thisYearsFederalTaxes.data,
                _income_total,
            )

            # print(_pyd.federalEffectiveTaxRate, _pyd.thisYearsIncomeTaxes, _pyd.incomeTotal)

            # _pyd.federalMarginalTaxRate = _ft.marginal_tax_rate(_pyd.taxableIncome)
            _pyd.federalMarginalTaxRate.data = _ft.marginal_tax_rate(
                _pyd.taxableIncomeTotal.data
            )

            # print(_pyd.taxableIncome, _pyd.federalMarginalTaxRate)

            # asset withdraw rate  (AWR)
            if self.UseSurplusAccount:
                _pyd.AW.data = -_pyd.cashFlow.data
            else:
                _pyd.AW.data = _pyd.assetWithdraw.data

            if _pyd.assetTotal.data == 0:
                _pyd.AWR.data = 0.0
            else:
                _pyd.AWR.data = 100.0 * _pyd.AW.data / _pyd.assetTotal.data

            _projection_data.append(_pyd)

        self.signals.result.emit(_projection_data)
