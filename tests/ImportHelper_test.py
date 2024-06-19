import unittest
from datetime import date

import sys

sys.path.append("../src")
from imports.ImportHelper import ImportHelper


class ImportHelperTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_string_to_integer(self):
        _i = ImportHelper()
        self.assertEqual(_i.str2int("3"), 3)
        self.assertIsNone(_i.str2int(""))

        # now try percents
        self.assertEqual(_i.strpct2int("3%"), 3)

    def test_string_to_float(self):
        _i = ImportHelper()
        self.assertEqual(_i.str2float("3.0"), 3.0)
        self.assertIsNone(_i.str2float(""), None)

        self.assertEqual(_i.strpct2float("3.0%"), 3.0)

    def test_string_to_date(self):
        _i = ImportHelper({"RetireDate": date(2001, 9, 11)})

        self.assertEqual(_i.str2date("09/11/2001"), date(2001, 9, 11))
        self.assertIsNone(_i.str2date(""))

        self.assertEqual(_i.str2date("Retirement"), date(2001, 9, 11))


if __name__ == "__main__":
    unittest.main()
