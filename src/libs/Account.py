from datetime import date

from .EnumTypes import AccountType, AccountOwnerType


class Account:
    def __init__(
        self,
        Name: str,
        Type: AccountType,
        Owner: AccountOwnerType,
        BirthDate: date = None,
        Balance: int = 0,
        Contribution: int = 0,
        ContributionBeginAge: int = None,
        ContributionEndAge: int = None,
        InterestRate: float = 0.0,
    ):
        assert isinstance(Name, str)
        self.Name = Name

        assert isinstance(Type, AccountType)
        self.Type = Type

        assert isinstance(Owner, AccountOwnerType)
        self.Owner = Owner

        assert isinstance(Balance, int) or Balance is None
        if Balance is None:
            self._balance = 0
        else:
            self._balance = Balance

        assert isinstance(InterestRate, float)
        if abs(InterestRate) >= 1:
            self.InterestRate = 1.0 + InterestRate / 100.0
        else:
            self.InterestRate = 1.0 + InterestRate

        self._taxable_income: int = 0
        self._ltcg_taxable: int = 0
        # for now we will treat short term capital gains like taxable income (maybe they r the same?)

        if Contribution is None:
            Contribution = 0
        self.Contribution = Contribution
        if ContributionBeginAge is None:
            ContributionBeginAge = 0
        if ContributionEndAge is None:
            ContributionEndAge = 99

        if BirthDate is not None:
            assert isinstance(BirthDate, date)
            self.ContributionBeginDate = date(
                BirthDate.year + ContributionBeginAge, BirthDate.month, BirthDate.day
            )
            self.ContributionEndDate = date(
                BirthDate.year + ContributionEndAge, BirthDate.month, BirthDate.day
            )
        else:
            self.ContributionBeginDate = None
            self.ContributionEndDate = None

    @property
    def Balance(self):
        return self._balance

    @Balance.setter
    def Balance(self, amount):
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

    @taxable_income.setter
    def taxable_income(self, value):
        self._taxable_income = value

    def deposit(self, amount: int):
        assert isinstance(amount, int)
        self._balance += amount

    def withdraw(self, amount: int):
        assert isinstance(amount, int)
        assert self._balance >= amount

        self._balance -= amount

    def calc_balance(self, year=None):
        if self._balance > 0:
            self._balance = int(self._balance * self.InterestRate)

        if (
            self.Contribution > 0
            and year is not None
            and year >= self.ContributionBeginDate.year
            and year <= self.ContributionEndDate.year
        ):
            self._balance += self.Contribution
            return self._balance, self.Contribution

        return self._balance, 0


class TraditionalIRA(Account):
    def __init__(self,
                 Name: str,
                 Owner: AccountOwnerType,
                 BirthDate: date = None,
                 Balance: int = 0,
                 InterestRate: float = 0.0,
                 Contribution: int = 0,
                 ContributionBeginAge: int = None,
                 ContributionEndAge: int = None):
        super(TraditionalIRA, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.TaxDeferred,
            BirthDate=BirthDate,
            Balance=Balance,
            InterestRate=InterestRate,
            Contribution=Contribution,
            ContributionBeginAge=ContributionBeginAge,
            ContributionEndAge=ContributionEndAge
        )
        self.ltcg_income = 0  # assuming this is always 0 for Traditional IRA

    def withdraw(self, amount: int):
        super().withdraw(amount)

        self._taxable_income = amount

    def calc_balance(self, year=None):
        self._taxable_income = 0

        return super().calc_balance(year)


class RothIRA(Account):
    def __init__(self,
                 Name: str,
                 Owner: AccountOwnerType,
                 BirthDate: date = None,
                 Balance: int = 0,
                 InterestRate: float = 0.0,
                 Contribution: int = 0,
                 ContributionBeginAge: int = None,
                 ContributionEndAge: int = None
        ):
        super(RothIRA, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.TaxFree,
            BirthDate=BirthDate,
            Balance=Balance,
            InterestRate=InterestRate,
            Contribution=Contribution,
            ContributionBeginAge=ContributionBeginAge,
            ContributionEndAge=ContributionEndAge
        )
        self.ltcg_income = 0  # assuming this is always 0
        self.taxable_income = 0  # assuming this is always 0


# Regular Brokerage Account
class Brokerage(Account):
    def __init__(
        self,
        Name: str,
                 Owner: AccountOwnerType,
                 BirthDate: date = None,
                 Balance: int = 0,
                 InterestRate: float = 0.0,
                 Contribution: int = 0,
                 ContributionBeginAge: int = None,
                 ContributionEndAge: int = None
        ):
        super(Brokerage, self).__init__(
            Name=Name,
            Owner=Owner,
            Type=AccountType.Regular,
            BirthDate=BirthDate,
            Balance=Balance,
            InterestRate=InterestRate,
            Contribution=Contribution,
            ContributionBeginAge=ContributionBeginAge,
            ContributionEndAge=ContributionEndAge
        )
        self.ltcg_income = 0  # will be interest on balance?
        self.taxable_income = 0  # assuming this is always 0

    def withdraw(self, amount):
        super().withdraw(amount)

        # assume the worst.. assume all withdrawn has to be long term capital gains
        # maybe find a way to change this so it doesn't have to be the full amount?
        self.ltcg_income = amount
        self.taxable_income = 0

    def calc_balance(self, year=None):
        # calculate the interest.. (ie, taxable income)
        self.ltcg_income = 0
        self.taxable_income = int(self._balance * (self.InterestRate - 1.0))

        return super().calc_balance(year)
