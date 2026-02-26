import unittest

from src.libs.Projections import todays_amount


class ProjectionsTest(unittest.TestCase):
    def test_todays_amount(self):
        self.assertEqual(todays_amount(100, 3, 5), 116)
        self.assertEqual(todays_amount(100, -3, 5), 86)


if __name__ == "__main__":
    unittest.main()
