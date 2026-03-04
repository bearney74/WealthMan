import random

DEBUG = False


class StdDevRandomNumberGenerator:
    def __init__(self, avg: float, stddev: float):
        assert isinstance(avg, float)
        self._avg = avg

        assert isinstance(stddev, float)
        self._stddev = stddev

    def get_rate(self):
        _rand = random.normalvariate(self._avg, self._stddev)
        return _rand / 100.0


class MonteCarloSimulator:
    def __init__(
        self,
        balance: int,
        expenses: list[int],
        avgReturnGen: StdDevRandomNumberGenerator,
        avgInflationRateGen: StdDevRandomNumberGenerator,
    ):
        assert isinstance(balance, int)
        self._balance = balance

        self._expenses = expenses

        self._bankrupt = False
        self._bankrupt_step = None  # the iterator in which we went bankrupt.
        # self._values = {}

        assert isinstance(avgReturnGen, StdDevRandomNumberGenerator)
        self._avg_return_generator = avgReturnGen

        assert isinstance(avgInflationRateGen, StdDevRandomNumberGenerator)
        self._avg_inflation_rate_generator = avgInflationRateGen

        self._balances: list[int] = []

    def is_bankrupt(self):
        return self._bankrupt

    def bankrupt_step(self):
        return self._bankrupt_step

    def percent_success(self):
        if self._bankrupt_step is None:
            return 100.0

        return int(100.0 * self._bankrupt_step / len(self._expenses))

    def process(self):
        self._balances = []
        self._bankrupt = False

        # _balance = self._balance
        _purchase_power = 1.0  # start at 1.0
        for _step, _expense in enumerate(self._expenses):
            # get average return
            _avg_return = self._avg_return_generator.get_rate()
            _period_inflation_rate = self._avg_inflation_rate_generator.get_rate()

            # adjust purchase power by inflation rate
            # _purchase_power *= (1.0 + _period_inflation_rate)

            # _period_expense = int(_expense * _purchase_power)

            # if DEBUG:
            #    print(
            #        "%d, %4.2f%%, %4.2f%%, %5.2f, %d"
            #        % (
            #            self._balance,
            #            _avg_return * 100.0,
            #            _period_inflation_rate * 100.0,
            #            _purchase_power,
            #            _period_expense,
            #        )
            #    )

            # subtract the expense from the balance
            # don't know if we should subtract expense or the inflated expense value
            self._balance -= _expense * (1.0 + _period_inflation_rate)

            # check if we have a positive balance or not
            if self._balance > 0:
                # if we have a positive balance, adjust by average return
                self._balance *= 1.0 + (_avg_return - _period_inflation_rate)
            else:
                self._balance *= 1.0 + _period_inflation_rate
                self._bankrupt = True
                if self._bankrupt_step is None:
                    self._bankrupt_step = _step

            # add this balance for record keeping if we want it..
            self._balances.append(self._balance)

    def get_balances(self):
        return self._balances


def stats(data: list[int]):
    import statistics as st

    return {
        "min": min(data),
        "max": max(data),
        "mean": st.mean(data),
        "median": st.median(data),
        "std dev": st.stdev(data),
    }


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    ## needed inputs are:
    # total expenses for each year.
    # starting balance
    # average returns and std dev
    # average inflation rate and std dev

    # avg s&P500 returns from 1928 - 2025 is 11.85
    # st dev (s&P500) from 1928 - 2025 is 19.40
    # avg inflation for 1928 - 2025 = 3.11
    # std dev (s&P500) from 1928 - 2025 = 3.90
    def run_simulator(number_of_runs, balance, expenses):
        _success = 0
        _failure_step = []
        _results = []

        _avg_returns_generator = StdDevRandomNumberGenerator(11.85, 19.40)
        _inflation_generator = StdDevRandomNumberGenerator(3.11, 3.90)

        _balances = []
        for _i in range(number_of_runs):
            _sim = MonteCarloSimulator(
                1000, [40] * 35, _avg_returns_generator, _inflation_generator
            )
            _sim.process()
            _balances.append(_sim.get_balances())

            if not _sim.is_bankrupt():
                _success += 1
            else:  # keep track of which step we ran out of money??
                _failure_step.append(_sim.bankrupt_step())

        # _percent_success= 100.0 * _success/float(number_of_runs)
        # _failure_stats=stats(_failure_step)
        # return _percent_success, _failure_stats

        return _balances

    def create_fanchart(results):
        result = np.array(results).T
        # print(result)
        x = np.arange(result.shape[0])
        # x=list(range(len(results[0])))
        # for the median use `np.median` and change the legend below
        median = np.median(result, axis=1)
        offsets = (10, 20, 30, 40)
        fig, ax = plt.subplots()
        ax.plot(median, color="black", lw=2)
        for offset in offsets:
            low = np.percentile(result, 50 - offset, axis=1)
            high = np.percentile(result, 50 + offset, axis=1)
            # since `offset` will never be bigger than 50, do 55-offset so that
            # even for the whole range of the graph the fanchart is visible
            alpha = (55 - offset) / 100
            ax.fill_between(x, low, high, color="blue", alpha=alpha)
        ax.legend(["Median"] + [f"Pct{2 * o}" for o in offsets])
        ax.axhline(y=0, color="gray", linestyle="dashed")  # dashed line at 0
        return fig, ax

    _results = run_simulator(10_000, 1000, [40] * 35)

    fig, ax = create_fanchart(_results)
    plt.show()
