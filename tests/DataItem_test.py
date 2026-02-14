import unittest

from src.libs.Projections import DataItem


class DataItemTest(unittest.TestCase):
    def test_DataItem(self):
        _a = DataItem("My header")
        self.assertEqual(str(_a), "$0")
        self.assertEqual(_a.header, "My header")
        self.assertEqual(_a.data, 0)

        _a = DataItem("abc", "{:.1f}%", 123.123)
        self.assertEqual(str(_a), "123.1%")
        self.assertEqual(_a.data, 123.123)


if __name__ == "__main__":
    unittest.main()
