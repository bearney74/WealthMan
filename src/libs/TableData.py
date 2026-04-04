from .Projections import ProjectionYearData, DataItem


class TableData:
    def __init__(
        self, Data: [ProjectionYearData], UseSurplusAccount: bool, InTodaysDollars: bool
    ):
        assert Data is not None
        self.projectionData = Data

        self.vheader = None
        self.data = None
        self.InTodaysDollars = InTodaysDollars
        self.UseSurplusAccount = UseSurplusAccount

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

            for _dataItem in _record.expenseSources:
                _list.append(_dataItem)

            # also add this years taxes, since this is technically an expense for this year..
            # _list.append(_record.thisYearsFederalTaxes)
            _list.append(_record.lastYearsFederalTaxes)

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

            for _dataItem in _record.incomeSources:
                _list.append(_dataItem)

            _list.append(_record.ssIncomeTotal)
            _list.append(_record.activeIncomeTotal)

            _list.append(_record.assetRegularReturns)
            _list.append(_record.incomeTotal)

            _list.append(_record.assetTaxDeferredWithdraws)
            _list.append(_record.taxableIncomeTotal)

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

            for _dataItem in _record.assetSources:
                _list.append(_dataItem)

            if self.UseSurplusAccount:
                _list.append(_record.surplusBalance)
                _list.append(_record.surplusWithdraw)

            _list.append(_record.assetTotalDeposits)
            _list.append(_record.assetTotalWithdraws)
            _list.append(_record.assetTotalNetDeposits)  # deposits - withdraws

            _list.append(_record.assetTotalReturns)
            _list.append(_record.assetTotalContributions)
            _list.append(_record.assetTotalCashFlow)
            _list.append(_record.assetTotalBalance)

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

            # _list.append(_record.longTermCapitalGainsTaxes)

            _list.append(_record.federalEffectiveTaxRate)
            _list.append(_record.federalMarginalTaxRate)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data

    def get_chart_data(self):
        _data = []
        for _record in self.projectionData:
            _dict = {}
            for _key, _attr in _record.__dict__.items():
                if isinstance(_attr, DataItem):
                    _dict[_key] = _attr
            _data.append(_dict)

        return _data

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

            for _attr in _record.__dict__:
                _obj = getattr(_record, _attr)
                if isinstance(_obj, DataItem):
                    _list.append(_obj)
                elif isinstance(_obj, list):
                    for _item in _obj:
                        if isinstance(_item, DataItem):
                            _list.append(_item)

            _data.append(_list)

        _header = [var.header for var in _data[0]]
        return _header, _vheader, _data
