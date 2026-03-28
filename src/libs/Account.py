from .EnumTypes import AccountType, AccountOwnerType
from .MiscLibs import todays_dollar, PeriodValidator


class ContributionClass:
    def __init__(
        self, amount: int, birthYear: int, beginAge: int, endAge: int, COLA: float = 0.0
    ):
        self._amount = amount
        if COLA is None:
            COLA = 0.0
        self._COLA = COLA

        self._periodValidator = PeriodValidator(birthYear, beginAge, endAge)

    def get_COLA(self) -> float:
        return self._COLA

    def get_Contribution_by_year(self, year: int) -> int:
        if self._periodValidator.isa_valid_period(year):
            return self._amount

        # we are outside our time frame, so just return 0.
        return 0


class Account:
    def __init__(
        self,
        Name: str,
        Type: AccountType,
        Owner: AccountOwnerType,
        Balance: int = 0,
        ContributionObj: ContributionClass = None,
        InterestRate: float = 0.0,
    ):
        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Type, AccountType)
        self.Type = Type

        assert isinstance(Owner, AccountOwnerType)
        self.Owner = Owner

        if Balance is None:
            Balance = 0
        assert isinstance(Balance, int)
        self._balance = Balance

        if InterestRate is None:
            InterestRate = 0.0
        assert isinstance(InterestRate, float)
        self.InterestRate = InterestRate

        # variables that reset every year..
        self._BOY_balance: int = 0
        self._interest: int = 0
        self._deposits: int = 0
        self._withdraws: int = 0
        self._contributions: int = 0
        self._taxable_income: int = 0
        self._ltcg_taxable: int = 0

        # for now we will treat short term capital gains like taxable income (maybe they r the same?)

        assert ContributionObj is None or isinstance(ContributionObj, ContributionClass)
        self._ContributionObj = ContributionObj

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        self._balance = amount

    @property
    def ltcg_income(self):
        return self._ltcg_income

    @ltcg_income.setter
    def ltcg_income(self, value):
        self._ltcg_income = value

    @property
    def taxable_income(self):
        return self._taxable_income

    def beginning_of_year_balance(self):
        return self._BOY_balance

    def beginning_of_year_bookkeeping(self):
        """there could be multiple deposits/withdraws so setting vars to zero at beginning of year"""

        self._BOY_balance = self._balance  # (beginning of year balance)
        self._interest = 0
        self._deposits = 0
        self._withdraws = 0
        self._contributions = 0

        # set tax info to 0
        self._taxable_income = 0
        self._ltcg_income = 0

    def end_of_year_bookkeeping(self):
        """time to add in the interest and other things"""

        self._balance = int(self.balance + self._interest)

    # @taxable_income.setter
    # def taxable_income(self, value):
    #    self._taxable_income = value

    def deposit(self, amount: int):
        assert isinstance(amount, int)

        self._deposits += amount
        self._balance += amount

    def withdraw(self, amount: int):
        assert isinstance(amount, int)
        assert self._balance >= amount

        self._withdraws += amount
        self._balance -= amount

    @property
    def totalWithdraws(self):
        return self._withdraws

    @property
    def totalDeposits(self):
        return self._deposits

    @property
    def interest(self):
        return self._interest

    @property
    def contributions(self):
        return self._contributions

    def get_contribution(self, year: int) -> int:
        if self._ContributionObj is None:
            return 0

        return self._ContributionObj.get_Contribution_by_year(year)

    def do_contribution(
        self, year: int, number_of_years: int, inflation: float
    ) -> None:
        if self._ContributionObj is None:
            return 0

        _COLA = self._ContributionObj.get_COLA()
        _amount = self.get_contribution(year)

        if _amount is None:
            return 0

        # factor is somewhat equivalent to CPI   factor=pow(COLA - inflation, num_of_years)
        _contrib = todays_dollar(_amount, _COLA, inflation, number_of_years)
        self.deposit(_contrib)
        self._contributions += _contrib

        return _contrib

    def calc_interest(self, inflation: float = 0.0) -> int:
        self._interest = 0
        if self._balance > 0:
            self._interest = int(
                self._balance * (self.InterestRate - inflation) / 100.0
            )

        return self._interest


class TraditionalIRA(Account):
    def __init__(
        self,
        Name: str,
        Owner: AccountOwnerType,
        Balance: int = 0,
        InterestRate: float = 0.0,
        ContributionObj: ContributionClass = None,
    ):
        super(TraditionalIRA, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.TAXDEFERRED,
            Balance=Balance,
            InterestRate=InterestRate,
            ContributionObj=ContributionObj,
        )
        self.ltcg_income = 0  # assuming this is always 0 for Traditional IRA

    def withdraw(self, amount: int):
        super().withdraw(amount)

        self._taxable_income += amount


class RothIRA(Account):
    def __init__(
        self,
        Name: str,
        Owner: AccountOwnerType,
        Balance: int = 0,
        InterestRate: float = 0.0,
        ContributionObj: ContributionClass = None,
    ):
        super(RothIRA, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.TAXFREE,
            Balance=Balance,
            InterestRate=InterestRate,
            ContributionObj=ContributionObj,
        )
        self._ltcg_income = 0  # assuming this is always 0
        self._taxable_income = 0  # assuming this is always 0


# Regular Brokerage Account
class Brokerage(Account):
    def __init__(
        self,
        Name: str,
        Owner: AccountOwnerType,
        Balance: int = 0,
        InterestRate: float = 0.0,
        ContributionObj: ContributionClass = None,
    ):
        super(Brokerage, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.REGULAR,
            Balance=Balance,
            InterestRate=InterestRate,
            ContributionObj=ContributionObj,
        )
        self._ltcg_income = 0  # will be interest on balance?
        self._taxable_income = 0  # assuming this is always 0

    def withdraw(self, amount):
        super().withdraw(amount)

        # assume the worst.. assume all withdrawn has to be long term capital gains
        # maybe find a way to change this so it doesn't have to be the full amount?
        self._ltcg_income += amount
        # self.taxable_income = 0

    def calc_interest(self, inflation):
        self._interest = int(self._balance * ((self.InterestRate - inflation) / 100.0))

        self._taxable_income = self._interest

        return self._interest
