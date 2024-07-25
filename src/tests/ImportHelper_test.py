import unittest
from datetime import date

from libs.ImportHelper import ImportHelper


class ImportHelperTest(unittest.TestCase):

    def test_str2float(self):
        _i=ImportHelper()
        self.assertEqual(_i.str2float("2"), 2.0)
        self.assertEqual(_i.str2float("2.0"), 2.0)
        self.assertEqual(_i.str2float("2.0  "), 2.0)
        self.assertEqual(_i.str2float("  2.0  "), 2.0)
        self.assertIsNone(_i.str2float(""))
        
    def test_strpct2float(self):
        _i=ImportHelper()
        self.assertEqual(_i.strpct2float("2%"), 2.0)
        self.assertEqual(_i.strpct2float("2.0%"), 2.0)
        self.assertEqual(_i.strpct2float("2.0%  "), 2.0)
        self.assertEqual(_i.strpct2float("  2.0%  "), 2.0)
        self.assertIsNone(_i.strpct2float(""))
        
    def test_strpct2int(self):
        _i=ImportHelper()
        self.assertEqual(_i.strpct2int("2%"), 2)
        self.assertEqual(_i.strpct2int("2%  "), 2)
        self.assertEqual(_i.strpct2int("  2%  "), 2)
        self.assertIsNone(_i.strpct2int(""))
        
    def test_str2int(self):
        _i=ImportHelper()
        self.assertEqual(_i.str2int("2"), 2)
        self.assertEqual(_i.str2int("2  "), 2)
        self.assertEqual(_i.str2int("  2  "), 2)
        self.assertIsNone(_i.str2int(""))
        
    def test_str2date(self):
        _i=ImportHelper()
        self.assertEqual(_i.str2date("01/01/2000"), date(2000, 1, 1))
        self.assertEqual(_i.str2date("09/10/2010"), date(2010, 9, 10))
        
        
        
if __name__ == "__main__":
    unittest.main()
