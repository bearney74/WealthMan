from .Projections import ProjectionYearData


class TableData:
    def __init__(
        self, Data: [ProjectionYearData], UseSurplusAccount: bool, InTodaysDollars: bool
    ):
        assert Data is not None
        self.projectionData = Data

        self.categories = None
        self.vheader = None
        self.data = None
        self.InTodaysDollars = InTodaysDollars
        # print(UseSurplusAccount)
        self.UseSurplusAccount = UseSurplusAccount

    def getCategories(self):
        if self.categories is None:
            self.categories, self.vheader, self.data = self._get_data_sheet()
            # self.categories = [_x.replace("\n", " ") for _x in self.categories]

        return self.categories

    def get_data_sheet(self):
        if self.data is None:
            # self.categories, self.vheader, self.data = self._get_data_sheet()
            self.categories, self.vheader, self.data = self._get_data_sheet()
            # self.categories = [_x.replace("\n", " ") for _x in self.categories]

        return self.categories, self.vheader, self.data

    def _calc_ages(self, rec):
        _ages = ""
        if rec.clientIsAlive:
            _ages += "%s" % rec.clientAge
        else:
            _ages += "--"

        if rec.spouseAge is not None:
            _ages += "/"
            if rec.spouseIsAlive:
                _ages += "%s" % rec.spouseAge
            else:
                _ages += "--"

        return _ages

    def _get_expense_data_sheet(self):
        _header = ["Year", "Age(s)"]
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _header_flag = _data == []
            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.expenseSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if _header_flag:
                _header.append("Expenses Total")
            _list.append(_record.expenseTotal)

            _data.append(_list)
        return _header, _vheader, _data

    def _get_income_data_sheet(self):
        _header = ["Year", "Ages(s)"]
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _header_flag = _data == []
            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.incomeSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if _header_flag:
                _header.append("SS Income Total")
            _list.append(_record.ssIncomeTotal)

            if _header_flag:
                _header.append("Tax Deferred Withdraws")
            _list.append(_record.assetTaxDeferredWithdraw)

            if _header_flag:
                _header.append("Regular Withdraws")
            _list.append(_record.assetRegularWithdraw)

            if _header_flag:
                _header.append("Tax Free Withdraws")
            _list.append(_record.assetTaxFreeWithdraw)

            if _header_flag:
                _header.append("Asset Withdraw Total")
            _list.append(_record.assetWithdraw)

            if _header_flag:
                _header.append("Income Total")
            _list.append(_record.incomeTotal)

            _data.append(_list)

        return _header, _vheader, _data

    def _get_asset_data_sheet(self):
        _header = ["Year", "Age(s)"]
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _header_flag = _data == []
            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.assetSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if self.UseSurplusAccount:
                if _header_flag:
                    _header.append("Surplus Account")
                    _header.append("Surplus Withdraw")
                _list.append(_record.surplusBalance)
                _list.append(_record.surplusWithdraw)

            if _header_flag:
                _header.append("Asset Total")
            _list.append(_record.assetTotal)

            for _name, _contribution in _record.assetContributions.items():
                if _header_flag:
                    _header.append("%s Contribution" % _name)
                _list.append(_contribution)

            if _header_flag:
                _header.append("Asset Contribution Total")
            _list.append(_record.assetContributionTotal)

            if _header_flag:
                _header.append("Tax Deferred Withdraws")
            _list.append(_record.assetTaxDeferredWithdraw)

            if _header_flag:
                _header.append("Regular Withdraws")
            _list.append(_record.assetRegularWithdraw)

            if _header_flag:
                _header.append("Tax Free Withdraws")
            _list.append(_record.assetTaxFreeWithdraw)

            if _header_flag:
                _header.append("Asset Withdraw")
            _list.append(_record.assetWithdraw)

            if _header_flag:
                _header.append("Transfers Total")
            _list.append(_record.transfersTotal)

            if _header_flag:
                _header.append("Client RMD")
            _list.append(_record.clientRMD)

            if _header_flag:
                _header.append("Client RMD %")
            _list.append(_record.clientRMDPercent)

            if _record.spouseAge is not None:
                if _header_flag:
                    _header.append("Spouse RMD")
                _list.append(_record.spouseRMD)

                if _header_flag:
                    _header.append("Spouse RMD %")
                _list.append(_record.spouseRMDPercent)

            if _header_flag:
                _header.append("Total RMD")
            _list.append(_record.totalRMD)

            if _header_flag:
                _header.append("Total RMD %")
            _list.append(_record.totalRMDPercent)

            _data.append(_list)

        return _header, _vheader, _data

    def _get_tax_data_sheet(self):
        _header = ["Year", "Age(s)"]
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _header_flag = _data == []
            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            if _header_flag:
                _header.append("Taxable Income")
            _list.append(_record.taxableIncomeTotal)

            if _header_flag:
                _header.append("SS Taxable Income")
            _list.append(_record.ssTaxableIncome)

            if _header_flag:
                _header.append("SS Tax Rate")
            _list.append(_record.ssTaxRate)

            # if _header_flag:
            #    _header.append("SS Tax Rate")
            # _list.append(_record.ssTaxRate)

            # for _name, _balance in _record.expenseSources.items():
            #    if _header_flag:
            #        _header.append(_name)
            #    _list.append(_balance)

            # if _header_flag:
            #    _header.append("Expense Total")
            # _list.append(_record.expenseTotal)

            if _header_flag:
                _header.append("Federal Filing Status")
            _list.append(_record.federalTaxFilingStatus)

            if _header_flag:
                _header.append("Last Years Federal Taxes")
            _list.append(_record.lastYearsFederalTaxes)

            if _header_flag:
                _header.append("This Years Federal Taxes")
            _list.append(_record.thisYearsFederalTaxes)

            if _header_flag:
                _header.append("Taxable Income")
            _list.append(_record.taxableIncome)

            if _header_flag:
                _header.append("Long Term Capital Gains")
            _list.append(_record.longTermCapitalGainsTaxes)

            if _header_flag:
                _header.append("Federal Effective Tax Rate")
            _list.append(_record.federalEffectiveTaxRate)

            if _header_flag:
                _header.append("Federal Marginal Tax Rate")
            _list.append(_record.federalMarginalTaxRate)

            _data.append(_list)

        return _header, _vheader, _data

    def _get_data_sheet(self):
        _header = ["Year", "Age(s)"]
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _header_flag = _data == []
            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            # for _name, _balance in _record.incomeSources.items():
            #    if _header_flag:
            #        _header.append(_name)
            #    _list.append(_balance)

            if _header_flag:
                _header.append("Income Total")
            _list.append(_record.incomeTotal)

            if _header_flag:
                _header.append("FPL")
            _list.append(_record.FPL)

            # if _header_flag:
            #    _header.append("SS Income Total")
            # _list.append(_record.ssIncomeTotal)

            # if _header_flag:
            #    _header.append("SS Taxable Income")
            # _list.append(_record.ssTaxableIncome)

            # if _header_flag:
            #    _header.append("SS Tax Rate")
            # _list.append(_record.ssTaxRate)

            # for _name, _balance in _record.expenseSources.items():
            #    if _header_flag:
            #        _header.append(_name)
            #    _list.append(_balance)

            if _header_flag:
                _header.append("Expense Total")
            _list.append(_record.expenseTotal)

            # if _header_flag:
            #    _header.append("Federal Filing Status")
            # _list.append(_record.federalTaxFilingStatus)

            # if _header_flag:
            #    _header.append("Last Years Federal Taxes")
            # _list.append(_record.lastYearsFederalTaxes)

            # if _header_flag:
            #    _header.append("This Years Federal Taxes")
            # _list.append(_record.thisYearsFederalTaxes)

            # if _header_flag:
            #    _header.append("Taxable Income")
            # _list.append(_record.taxableIncome)

            # if _header_flag:
            #    _header.append("Federal Effective Tax Rate")
            # _list.append(_record.federalEffectiveTaxRate)

            # if _header_flag:
            #    _header.append("Federal Marginal Tax Rate")
            # _list.append(_record.federalMarginalTaxRate)

            # for _name, _contribution in _record.assetContributions.items():
            #    if _header_flag:
            #        _header.append("%s Contribution" % _name)
            #    _list.append(_contribution)

            if _header_flag:
                _header.append("Asset Contribution Total")
            _list.append(_record.assetContributionTotal)

            # if _header_flag:
            #    _header.append("Tax Deferred Withdraws")
            # _list.append(_record.assetTaxDeferredWithdraw)

            # if _header_flag:
            #    _header.append("Regular Withdraws")
            # _list.append(_record.assetRegularWithdraw)

            # if _header_flag:
            #    _header.append("Tax Free Withdraws")
            # _list.append(_record.assetTaxFreeWithdraw)

            if _header_flag:
                _header.append("Asset Withdraw Total")
            _list.append(_record.assetWithdraw)

            if _header_flag:
                _header.append("Cash Flow")
            _list.append(_record.cashFlow)

            # if _header_flag:
            #    _header.append("Long Term Capital Gains")
            # _list.append(_record.longTermCapitalGainsTaxes)

            if _header_flag:
                _header.append("Surplus/Deficit")
            _list.append(_record.surplusDeficit)

            # for _name, _balance in _record.assetSources.items():
            #    if _header_flag:
            #        _header.append(_name)
            #    _list.append(_balance)

            # if self.UseSurplusAccount:
            #    if _header_flag:
            #        _header.append("Surplus Withdraw")
            #        _header.append("Surplus Account")
            #    _list.append(_record.surplusWithdraw)
            #    _list.append(_record.surplusBalance)

            if _header_flag:
                _header.append("Asset Total")
            _list.append(_record.assetTotal)

            # if _header_flag:
            #    _header.append("Client RMD")
            # _list.append(_record.clientRMD)

            # if _header_flag:
            #    _header.append("Client RMD %")
            # _list.append(_record.clientRMDPercent)

            # if _record.spouseAge is not None:
            #    if _header_flag:
            #        _header.append("Spouse RMD")
            #    _list.append(_record.spouseRMD)

            #    if _header_flag:
            #        _header.append("Spouse RMD %")
            #    _list.append(_record.spouseRMDPercent)

            if _header_flag:
                _header.append("Total RMD")
            _list.append(_record.totalRMD)

            if _header_flag:
                _header.append("Total RMD %")
            _list.append(_record.totalRMDPercent)

            if _header_flag:
                _header.append("AW")
            _list.append(_record.AW)

            if _header_flag:
                _header.append("AWR")
            _list.append(_record.AWR)

            _data.append(_list)

        return _header, _vheader, _data
