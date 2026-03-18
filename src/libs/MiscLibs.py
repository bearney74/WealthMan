def todays_dollar(
    amount: int, COLA: float, inflation: float, number_of_years: int
) -> int:
    return int(amount * pow(1.0 + (COLA - inflation) / 100.0, number_of_years))


class PeriodValidator:
    """Are we in a valid period (ie, a year between beginAge and endAge?)
    This is useful for class instances that are only "valid" during a certain age frame.
    Good examples are income, when SS starts, or certain expenses that may occur
    only during a certain timeframe.
    """

    def __init__(self, birthYear: int, beginAge: int = None, endAge: int = None):
        assert isinstance(birthYear, int)

        if beginAge is None:
            beginAge = 0
        self._beginAge = beginAge

        if endAge is None:
            endAge = 99
        self._endAge = endAge

        self._beginYear = birthYear + beginAge
        self._endYear = birthYear + endAge

    @property
    def beginAge(self):
        return self._beginAge

    def isa_valid_period(self, year: int) -> bool:
        return self._beginYear <= year <= self._endYear
