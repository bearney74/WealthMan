from .Projections import ProjectionYearData, DataItem


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
        self.UseSurplusAccount = UseSurplusAccount

    def getCategories(self):
        if self.categories is None:
            self.categories, self.vheader, self.data = self._get_data_sheet()

        return self.categories

    def get_data_sheet(self):
        if self.data is None:
            self.categories, self.vheader, self.data = self._get_data_sheet()

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

        return DataItem("Age(s)", "{}", _ages)

    def _get_expense_data_sheet(self):
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.expenseSources.items():
                _list.append(DataItem(_name, "${:,}", _balance))

            _list.append(_record.expenseTotal)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data

    def _get_income_data_sheet(self):
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.incomeSources.items():
                _list.append(_balance)

            _list.append(_record.ssIncomeTotal)

            _list.append(_record.assetTaxDeferredWithdraw)
            _list.append(_record.assetRegularWithdraw)
            _list.append(_record.assetTaxFreeWithdraw)
            _list.append(_record.assetWithdraw)

            _list.append(_record.incomeTotal)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
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

            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            for _name, _balance in _record.assetSources.items():
                _list.append(_balance)

            if self.UseSurplusAccount:
                _list.append(_record.surplusBalance)
                _list.append(_record.surplusWithdraw)

            _list.append(_record.assetTotal)

            for _name, _contribution in _record.assetContributions.items():
                _list.append(_contribution)

            _list.append(_record.assetContributionTotal)

            _list.append(_record.assetTaxDeferredWithdraw)
            _list.append(_record.assetRegularWithdraw)
            _list.append(_record.assetTaxFreeWithdraw)
            _list.append(_record.assetWithdraw)

            _list.append(_record.transfersTotal)

            _list.append(_record.clientRMD)
            _list.append(_record.clientRMDPercent)

            if _record.spouseAge is not None:
                _list.append(_record.spouseRMD)
                _list.append(_record.spouseRMDPercent)

            _list.append(_record.totalRMD)

            _list.append(_record.totalRMDPercent)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data

    def _get_tax_data_sheet(self):
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            _list.append(_record.taxableIncomeTotal)
            _list.append(_record.ssTaxableIncome)

            _list.append(_record.ssTaxRate)

            _list.append(_record.federalTaxFilingStatus)

            _list.append(_record.lastYearsFederalTaxes)
            _list.append(_record.thisYearsFederalTaxes)

            _list.append(_record.longTermCapitalGainsTaxes)

            _list.append(_record.federalEffectiveTaxRate)
            _list.append(_record.federalMarginalTaxRate)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data

    def _get_data_sheet(self):
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            _list = [_record.projectionYear, self._calc_ages(_record)]
            _vheader.append(
                "%s:%s" % (_record.projectionYear, self._calc_ages(_record))
            )

            _list.append(_record.incomeTotal)
            _list.append(_record.FPL)
            _list.append(_record.expenseTotal)

            _list.append(_record.assetContributionTotal)
            _list.append(_record.assetWithdraw)

            _list.append(_record.cashFlow)

            _list.append(_record.surplusDeficit)

            _list.append(_record.assetTotal)

            _list.append(_record.totalRMD)
            _list.append(_record.totalRMDPercent)

            _list.append(_record.AW)
            _list.append(_record.AWR)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data
