from .Projections import ProjectionYearData


class TableData:
    def __init__(self, Data: [ProjectionYearData], InTodaysDollars:bool):
        assert Data is not None
        self.projectionData = Data

        self.categories = None
        self.vheader=None
        self.data = None
        self.InTodaysDollars=InTodaysDollars

    def getCategories(self):
        if self.categories is None:
            _categories, self.vheader, self.data = self._get_data_sheet()
            self.categories=[_x.replace('\n', ' ') for _x in _categories]

        return self.categories

    def get_data_sheet(self):
        if self.data is None:
            _categories, self.vheader, self.data = self._get_data_sheet()
            self.categories=[_x.replace('\n', ' ') for _x in _categories]

        return self.categories, self.vheader, self.data

    def _get_data_sheet(self):
        # _header = ["Year", "Age(s)"]
        _header = []
        _vheader = []
        _data = []

        for _record in self.projectionData:
            if not _record.clientIsAlive:
                if _record.spouseAge is None:
                    continue
                if not _record.spouseIsAlive:
                    continue

            # print("got here for year ", _record.projectionYear)
            _header_flag = _data == []
            # get year header (year, age1, age2)
            _list = [_record.projectionYear]
            #_list = []
            if _header_flag:
                _header.append("Year")
                
            _ages = ""
            if _record.clientIsAlive:
                _ages += "%s" % _record.clientAge
            else:
                _ages += "--"

            if _record.spouseAge is not None:
                _ages += "/"
                if _record.spouseIsAlive:
                    _ages += "%s" % _record.spouseAge
                else:
                    _ages += "--"
            _list.append(_ages)
            if _header_flag:
                _header.append("Age(s)")
                
            _vheader.append("%s: %s" % (_record.projectionYear, _ages))

            for _name, _balance in _record.incomeSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if _header_flag:
                _header.append("Income Total")
            _list.append(_record.incomeTotal)

            for _name, _balance in _record.expenseSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if _header_flag:
                _header.append("Expense Total")
            _list.append(_record.expenseTotal)

            if _header_flag:
                _header.append("Last Years\nFederal Taxes")
            _list.append(_record.lastYearsFederalTaxes)

            if _header_flag:
                _header.append("This Years\nFederal Taxes")
            _list.append(_record.thisYearsFederalTaxes)

            if _header_flag:
                _header.append("Taxable Income")
            _list.append(_record.taxableIncome)
            
            if _header_flag:
                _header.append("Federal Effective\nTax Rate")
            _list.append(_record.federalEffectiveTaxRate)

            if _header_flag:
                _header.append("Federal Marginal\nTax Rate")
            _list.append(_record.federalMarginalTaxRate)
            
            for _name, _contribution in _record.assetContributions.items():
                if _header_flag:
                    _header.append("%s\nContribution" % _name)
                _list.append(_contribution)

            if _header_flag:
                _header.append("Asset\nContribution Total")
            _list.append(_record.assetContributionTotal)

            if _header_flag:
                _header.append("Asset Withdraw")
            _list.append(_record.assetWithdraw)

            if _header_flag:
                _header.append("Surplus/Deficit")
            _list.append(_record.surplus_deficit)

            for _name, _balance in _record.assetSources.items():
                if _header_flag:
                    _header.append(_name)
                _list.append(_balance)

            if _header_flag:
                _header.append("AssetTotal")
            _list.append(_record.assetTotal)

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
        # print(_data)
        return _header, _vheader, _data
