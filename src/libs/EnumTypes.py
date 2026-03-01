from enum import Enum, StrEnum  # StrEnum requires python > 3.10


class RelationStatusType(StrEnum):
    SINGLE = "Single"
    MARRIED = "Married"


class PersonType(StrEnum):
    CLIENT = "Client"
    SPOUSE = "Spouse"


class AccountOwnerType(Enum):
    CLIENT = 0
    SPOUSE = 1
    BOTH = 2


class AccountType(Enum):
    REGULAR = 1  # Savings, Checking, Money Market, etc
    TAXDEFERRED = 2  # 401k, IRA, etc
    TAXFREE = 3  # Roth IRA, Life Insurance Payout, etc


#   Brokerage = 4  # for long term capital gains taxes...


class IncomeSourceType(Enum):
    EMPLOYMENT = 1
    PENSION = 2
    SOCIAL_SECURITY = 3


class FederalTaxStatusType(StrEnum):
    SINGLE = "Single"
    MARRIED_FILING_JOINTLY = "Married Filing Jointly"
    MARRIED_FILING_SEPARATELY = "Married Filing Separately"
    HEAD_OF_HOUSEHOLD = "Head Of Household"


class WithdrawOrderType(StrEnum):
    TAXDEFERRED_REGULAR_TAXFREE = "Tax Deferred, Regular, Tax Free"
    TAXDEFERRED_TAXFREE_REGULAR = "Tax Deferred, Tax Free, Regular"
    REGULAR_TAXFREE_TAXDEFERRED = "Regular, Tax Free, Tax Deferred"
    REGULAR_TAXDEFERRED_TAXFREE = "Regular, Tax Deferred, Tax Free"
    TAXFREE_TAXDEFERRED_REGULAR = "Tax Free, Tax Deferred, Regular"
    TAXFREE_REGULAR_TAXDEFERRED = "Tax Free, Regular, Tax Deferred"
