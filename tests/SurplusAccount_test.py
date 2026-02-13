import unittest

from libs.SurplusAccount import SurplusAccount


class SurplusAccountTest(unittest.TestCase):
    """tests to verify that basic calcs from Federal Tax Brackets are correct..."""

    def test_Surplus(self):
        _a = SurplusAccount(0, 10.0)
        _a.deposit(500)
        self.assertEqual(_a.balance, 500)

        _withdraw, _deficit = _a.withdraw(400)
        self.assertEqual(
            _deficit, 0
        )  # we had enough to cover the withdraw so deficit is 0
        self.assertEqual(_a.balance, 100)
        self.assertEqual(_withdraw, 400)

        _a.add_interest()  # no year set.. no Contribution set, Cola=0 etc..  should return unmodified balance
        self.assertEqual(_a.balance, 110)

        # we only have 110, but lets try to withdraw 250
        _withdraw, _deficit = _a.withdraw(250)
        self.assertEqual(_deficit, -140)
        self.assertEqual(_withdraw, 110)
        self.assertEqual(_a.balance, 0)


if __name__ == "__main__":
    unittest.main()
