import unittest

from src.libs.SurplusAccount import SurplusAccount


class SurplusAccountTest(unittest.TestCase):
    def test_Surplus(self):
        _a = SurplusAccount(0, 10.0)
        # see that initial values are correct...
        self.assertEqual(_a.totalDeposits, 0)
        self.assertEqual(_a.totalWithdraws, 0)
        self.assertEqual(_a.balance, 0)

        # deposit 500, and make sure that the balance is 500 and amount deposited is 500
        _a.deposit(500)
        self.assertEqual(_a.totalDeposits, 500)
        self.assertEqual(_a.balance, 500)
        self.assertEqual(_a.totalWithdraws, 0)

        _a.withdraw(400)
        self.assertEqual(_a.totalWithdraws, 400)
        self.assertEqual(_a.totalDeposits, 500)
        self.assertEqual(_a.balance, 100)

        self.assertEqual(_a.calc_interest(), 10)  # at 10% on 100 balance, should be 10
        self.assertEqual(_a.balance, 100)
        self.assertEqual(_a.interest, 10)

        # deposits and withdraws should not change..
        self.assertEqual(_a.totalWithdraws, 400)
        self.assertEqual(_a.totalDeposits, 500)

        # do year end bookkeeping... (should add interest to balance)
        _a.end_of_year_bookkeeping()

        self.assertEqual(_a.totalWithdraws, 400)
        self.assertEqual(
            _a.balance, 110
        )  # now balance is $10 more! (interest added in)
        self.assertEqual(_a.totalDeposits, 500)

        # we only have 110, but lets try to withdraw 250
        with self.assertRaises(AssertionError):
            _a.withdraw(250)


if __name__ == "__main__":
    unittest.main()
