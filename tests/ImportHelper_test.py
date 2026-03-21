import unittest
from datetime import date

from src.libs.ImportHelper import ImportHelper


class ImportHelperTest(unittest.TestCase):
    def setUp(self):
        self._i = ImportHelper()

    def tearDown(self):
        del self._i

    def test_str2float(self):
        self.assertEqual(self._i.str2float("2"), 2.0)
        self.assertEqual(self._i.str2float("2.0"), 2.0)
        self.assertEqual(self._i.str2float("2.0  "), 2.0)
        self.assertEqual(self._i.str2float("  2.0  "), 2.0)

        with self.assertRaises(ValueError):
            self._i.str2float("a")

    def test_strpct2float(self):
        self.assertEqual(self._i.strpct2float("2%"), 2.0)
        self.assertEqual(self._i.strpct2float("2.0%"), 2.0)
        self.assertEqual(self._i.strpct2float("2.0%  "), 2.0)
        self.assertEqual(self._i.strpct2float("  2.0%  "), 2.0)
        self.assertEqual(self._i.strpct2float("2.0"), 2.0)
        self.assertEqual(self._i.strpct2float("2"), 2.0)
        self.assertIsNone(self._i.strpct2float(""))

    def test_strpct2int(self):
        self.assertEqual(self._i.strpct2int("2%"), 2)
        self.assertEqual(self._i.strpct2int("2%  "), 2)
        self.assertEqual(self._i.strpct2int("  2%  "), 2)
        self.assertEqual(self._i.strpct2int("2"), 2)
        self.assertIsNone(self._i.strpct2int(""))

    def test_str2int(self):
        self.assertEqual(self._i.str2int("2"), 2)
        self.assertEqual(self._i.str2int("2  "), 2)
        self.assertEqual(self._i.str2int("  2  "), 2)
        self.assertIsNone(self._i.str2int(""))

        with self.assertRaises(ValueError):
            self._i.str2int("2.0")

    def test_str2date(self):
        self.assertEqual(self._i.str2date("01/01/2000"), date(2000, 1, 1))
        self.assertEqual(self._i.str2date("09/10/2010"), date(2010, 9, 10))

        with self.assertRaises(ValueError):
            self._i.str2date("13/12/2010")


if __name__ == "__main__":
    unittest.main()
