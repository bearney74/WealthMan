from .MiscLibs import PeriodValidator


class Expense:
    def __init__(
        self,
        Name: str,
        Amount: int,
        COLA: float = 0.0,
        Period: PeriodValidator = None,
    ):
        assert Period is None or isinstance(Period, PeriodValidator)
        self._period = Period

        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Amount, int)
        self.Amount = Amount

        assert isinstance(COLA, float) or COLA is None
        if COLA is None:
            COLA = 0.0
        self.COLA = COLA

        self._COLA_Flag = COLA != 0.0

        self._annual_balance = 0

    def set_COLA_Flag(self, flag: bool):
        self._COLA_Flag = flag

    def get_COLA_Flag(self):
        return self._COLA_Flag

    def calc_balance_by_year(self, year, inflation=0.0) -> int:
        # this income source is still in the future..  just return 0.
        if self._period is None:
            return 0

        if self._period.isa_valid_period(year):
            return self._calc_balance(inflation)

        return 0

    def _calc_annual_balance(self) -> int:
        return self.Amount

    def _calc_balance(self, inflation=0.0) -> int:
        if self._annual_balance == 0:
            self._annual_balance = self._calc_annual_balance()
            return self._annual_balance

        self._annual_balance = int(
            self._annual_balance * (1.0 + (self.COLA - inflation) / 100.0)
        )
        return self._annual_balance
