from .Projections import ProjectionYearData


class TableData:
    def __init__(self, Data: [ProjectionYearData]):
        assert Data is not None
        self.projectionData = Data

        self.categories = None
        self.data = None

    def getCategories(self):
        if self.categories is None:
            self.categories, self.data = self._get_data_sheet()

        return self.categories

    def get_data_sheet(self):
        if self.data is None:
            self.categories, self.data = self._get_data_sheet()

        return self.categories, self.data

    def _get_data_sheet(self):
        _header = ["Year", "Age(s)"]
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
                _header.append("Federal Taxes")
            _list.append(_record.federalTaxes)

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
        return _header, _data
