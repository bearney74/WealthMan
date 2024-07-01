import xml.etree.ElementTree as ET

from .EnumTypes import FederalTaxStatusType
from imports.ImportHelper import ImportHelper


class FederalTax(ImportHelper):
    def __init__(self, FileStatus: FederalTaxStatusType, Year: int):
        # ImportHelper.__init__(self)
        self.FileStatus = FileStatus
        self.Year = Year

        self.Brackets = None
        self.StandardDeduction=None
        
        self._import_data()

        # if things were imported correctly from the xml, the vars below should be dicts..
        assert isinstance(self.Brackets, dict)

        # sort the values by keys to guarantee that we know that the lowest brackets are first..
        self.Brackets = dict(sorted(self.Brackets.items()))

    def _import_data(self):
        _xml = ET.parse("../../data/FederalTaxBrackets.xml")
        self._root = _xml.getroot()

        assert self._root.tag == "xml"
        assert self._root.attrib["Year"] == "%s" % self.Year

        assert self._root.attrib["Data"] == "Federal Tax Brackets"

        _sd = self._root.findall("./StandardDeductions")
        assert len(_sd) == 1

        _files = _sd[0].findall("./File")
        assert len(_files) > 0

        for _file in _files:
            _status = _file.attrib["Status"]
            if FederalTaxStatusType[_status] == self.FileStatus:
                self.StandardDeduction = int(_file.text)

        _b = self._root.findall("./Brackets")
        assert len(_b) == 1

        _files = _b[0].findall("File")

        for _file in _files:
            _status = _file.attrib["Status"]
            if FederalTaxStatusType[_status] == self.FileStatus:
                _taxes = _file.findall("Tax")
                assert len(_taxes) > 1

                self.Brackets = {}
                for _tax in _taxes:
                    _rate = _tax.attrib["Rate"]
                    _rate = self.strpct2int(_rate)
                    _begin = _tax.attrib["Begin"]
                    _begin = self.str2int(_begin)
                    _end = _tax.attrib["End"]
                    _end = self.str2int(_end)

                    self.Brackets[_rate] = {"Begin": _begin, "End": _end}

    def calc_taxes(self, taxable_income: int) -> int:
        _total = 0
        # print(self.Brackets)
        for _rate, _dict in self.Brackets.items():
            _begin = _dict["Begin"]
            if _begin is None:
                _begin = 0
            _end = _dict["End"]

            if taxable_income >= _begin:
                if _end is None or taxable_income <= _end:
                    _total += (taxable_income - _begin) * _rate / 100.0
                elif taxable_income > _end:
                    _total += (_end - _begin) * _rate / 100.0
                # elif _taxable_income < _end:
                #   _total+=(taxable_income - _begin) * _rate

            # print(_total)

        return int(_total)

    def effective_tax_rate(self, taxable_income: int, total_income: int) -> float : 
        return 100.0 * self.calc_taxes(taxable_income)/total_income
    
    def marginal_tax_rate(self, taxable_income) -> int:
        for _rate, _dict in self.Brackets.items():
            _begin=_dict['Begin']
            _end=_dict['End']
            if _begin is None:
                _begin = 0
            if _end is None:
                _end = 999_999_999_999
            if taxable_income >= _begin and taxable_income <= _end:
                return float(_rate)
            
        return None  # we shouldn't get here..
    