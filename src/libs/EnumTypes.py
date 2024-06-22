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


class Relationship(Enum):
    Spouse = 1
    Child = 2


class AccountType(Enum):
    Regular = 1  # Brokerage, Savings, Checking, Money Market, etc
    TaxDeferred = 2  # 401k, IRA, etc
    TaxFree = 3  # Roth IRA, Life Insurance Payout, etc


class IncomeType(Enum):
    Employment = 1
    Pension = 2
    SocialSecurity = 3


class FederalTaxStatusType(Enum):
    Single = 1
    MarriedJointly = 2
    MarriedSeparate = 3
    HeadOfHousehold = 4
