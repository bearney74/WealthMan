from enum import Enum


class AmountPeriodType(Enum):
    Annual = 1
    Monthly = 2
    BiWeekly = 3
    Weekly = 4


class RelationStatus(Enum):
    Single = 1
    Married = 2


class PersonType(Enum):
    Client = 0
    Spouse = 1


class AccountOwnerType(Enum):
    Client = 0
    Spouse = 1
    Both = 2


class Relationship(Enum):
    Spouse = 1
    Child = 2


class AccountType(Enum):
    Regular = 1  # Savings, Checking, Money Market, etc
    TaxDeferred = 2  # 401k, IRA, etc
    TaxFree = 3  # Roth IRA, Life Insurance Payout, etc
    Brokerage = 4  # for long term capital gains taxes...


class IncomeSourceType(Enum):
    Employment = 1
    Pension = 2
    SocialSecurity = 3


class FederalTaxStatusType(Enum):
    Single = 1
    MarriedFilingJointly = 2
    MarriedFilingSeparately = 3
    HeadOfHousehold = 4

    @classmethod
    def has_member(cls, s):
        return s in cls.__members__
