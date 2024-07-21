import os
import xml.etree.ElementTree as ET

from .EnumTypes import FederalTaxStatusType
from .ImportHelper import ImportHelper


class FederalTax(ImportHelper):
    def __init__(self, FileStatus: FederalTaxStatusType, Year: int):
        self.FileStatus = FileStatus
        self.Year = Year

        self.Brackets = None
        self.StandardDeduction = None
        self.LongTermCapitalGains = None

        self._import_data()

        # if things were imported correctly from the xml, the vars below should be dicts..
        assert isinstance(self.Brackets, dict)
        assert isinstance(self.LongTermCapitalGains, dict)

        # sort the values by keys to guarantee that we know that the lowest brackets are first..
        self.Brackets = dict(sorted(self.Brackets.items()))
        self.LongTermCapitalGains = dict(sorted(self.LongTermCapitalGains.items()))

    def _import_data(self):
        _dir = os.path.dirname(__file__)
        # print(__file__)
        _xml = ET.parse(os.path.join(_dir, "data/FederalTaxBrackets.xml"))
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

        # tax brackets
        _b = self._root.findall("./TaxBrackets")
        assert len(_b) == 1
        _files = _b[0].findall("File")
        self.Brackets = self._import_file_tax_data(_files)

        # long term capital gains..
        _ltcg = self._root.findall("./LongTermCapitalGains")
        assert len(_ltcg) == 1
        _files = _ltcg[0].findall("File")
        self.LongTermCapitalGains = self._import_file_tax_data(_files)

    def _import_file_tax_data(self, _file_xml):
        _dict = {}
        for _file in _file_xml:
            _status = _file.attrib["Status"]
            if FederalTaxStatusType[_status] == self.FileStatus:
                _taxes = _file.findall("Tax")
                assert len(_taxes) > 1

                for _tax in _taxes:
                    _rate = _tax.attrib["Rate"]
                    _rate = self.strpct2int(_rate)
                    _begin = _tax.attrib["Begin"]
                    _begin = self.str2int(_begin)
                    _end = _tax.attrib["End"]
                    _end = self.str2int(_end)

                    _dict[_rate] = {"Begin": _begin, "End": _end}

        return _dict

    # long term capital gains..
    def calc_ltcg_taxes(self, capital_gains: int) -> int:
        _total = 0
        for _rate, _dict in self.LongTermCapitalGains.items():
            _begin = _dict["Begin"]
            if _begin is None:
                _begin = 0
            _end = _dict["End"]

            if capital_gains >= _begin:
                if _end is None or capital_gains <= _end:
                    _total += (capital_gains - _begin) * _rate / 100.0
                elif capital_gains > _end:
                    _total += (_end - _begin) * _rate / 100.0

        return int(_total)

    def calc_taxes(self, taxable_income: int) -> int:
        _total = 0
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

        return int(_total)

    def effective_tax_rate(self, taxes: int, total_income: int) -> float:
        if total_income == 0:
            return 0.0
        return 100.0 * taxes / total_income

    def marginal_tax_rate(self, taxable_income) -> int:
        for _rate, _dict in self.Brackets.items():
            _begin = _dict["Begin"]
            _end = _dict["End"]
            if _begin is None:
                _begin = 0
            if _end is None:
                _end = 999_999_999_999
            if taxable_income >= _begin and taxable_income <= _end:
                return float(_rate)

        return None  # we shouldn't get here..
