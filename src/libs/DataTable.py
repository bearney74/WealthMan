class DataElement:
    def __init__(self, Category: str, Name: str, Year: int, Value: str):
        self.Category = Category
        self.Name = Name
        self.Year = Year
        self.Value = Value


class DataTable:
    def __init__(self, BeginYear: int, EndYear: int, Data: list):
        self.BeginYear = BeginYear
        self.EndYear = EndYear
        self.Data = Data

        self.Categories = []

    # def analyze(self):
    #    for element in self.data:
    #        if element.Category not in self.Categories:
    #           self.Categories.append(element.Category)

    def get_data_sheet(self):
        # if len(self.Categories) == 0:
        #   self.analyze()

        _header = ["Year", "Age(s)"]
        _data = []

        for _year in range(self.BeginYear, self.EndYear + 1):
            # get year header (year, age1, age2)
            _list = []
            for _de in self.Data:
                if _de.Year == _year:
                    if _de.Category == "Header":
                        if _de.Name in ("Year", "Age"):
                            _list.append(_de.Value)

            for _category in ("Income", "Taxes", "Expense", "Cash Flow",
                              "Pulled from Assets", "Asset"):
                for _de in self.Data:
                    if _de.Year == _year and _category == _de.Category:
                        if _year == self.BeginYear:
                            if _de.Name == "Total":
                                _header.append("%s Total" % _category)
                            else:
                                _header.append(_de.Name)
                        _list.append("%s" % _de.Value)
                        # print(_de.Value)

            _data.append(_list)
        # print(_data)
        return _header, _data

    def get_asset_data(self):
        _list = []
        for _de in self.Data:
            if _de.Category == "Asset" and _de.Name not in ("Total", "RMD", "RMD %"):
                _list.append(_de)

        return _list

    def get_totals_data(self):
        _list = []
        for _de in self.Data:
            if _de.Name == "Total":
                _list.append(_de)

        return _list
