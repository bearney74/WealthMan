import unittest

from src.libs.MonteCarloSim import StdDevRandomNumberGenerator, MonteCarloSimulator


class MonteCarloSimTest(unittest.TestCase):
    def test_NumberGenerator(self):
        _gen = StdDevRandomNumberGenerator(1.0, 0.5)

        # is this okay?  should return values within 3 std dev (3x0.5=1.5)
        self.assertAlmostEqual(_gen.get_rate(), 1, delta=1.5)

    def test_MonteCarloSim_NoExpenses(self):
        _ror = StdDevRandomNumberGenerator(11.85, 19.40)  # rate of return
        _inf = StdDevRandomNumberGenerator(3.11, 3.90)  # inflation

        _sim = MonteCarloSimulator(1000, [0] * 10, _ror, _inf)
        _sim.process()

        # expenses is 0 so this should always be valid
        self.assertFalse(_sim.is_bankrupt())
        self.assertIsNone(_sim.bankrupt_step())
        self.assertEqual(_sim.percent_success(), 100.0)

        # should have 10 balances, one for each year..
        self.assertEqual(len(_sim.get_balances()), 10)

        # balances should also be greater than 0.
        for _balance in _sim.get_balances():
            self.assertGreater(_balance, 0)

    def test_MonteCarloSim_BigExpenses(self):
        _ror = StdDevRandomNumberGenerator(11.85, 19.40)  # rate of return
        _inf = StdDevRandomNumberGenerator(3.11, 3.90)  # inflation

        _sim = MonteCarloSimulator(1000, [500] * 10, _ror, _inf)
        _sim.process()

        # expenses is 0 so this should always be valid
        self.assertTrue(_sim.is_bankrupt())
        self.assertIsNotNone(_sim.bankrupt_step())

        self.assertGreater(_sim.bankrupt_step(), -1)
        self.assertLess(_sim.bankrupt_step(), 10)

        # success is < 100
        self.assertLess(_sim.percent_success(), 100.0)

        # should have 10 balances, one for each year..
        self.assertEqual(len(_sim.get_balances()), 10)

        # balances should also be greater than 0.
        # for _balance in _sim.get_balances():
        #    self.assertGreater(_balance, 0)


if __name__ == "__main__":
    unittest.main()
