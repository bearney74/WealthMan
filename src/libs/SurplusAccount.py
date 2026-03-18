from .Account import Account
from .EnumTypes import AccountOwnerType, AccountType


class SurplusAccount(Account):
    def __init__(self, balance, interest_rate):
        super(SurplusAccount, self).__init__(
            Name="Surplus Account",
            Owner=AccountOwnerType.CLIENT,  # maybe type both??
            Type=AccountType.REGULAR,
            Balance=balance,
            InterestRate=interest_rate,
        )
        self.ltcg_income = 0  # assuming this is always 0 for Traditional IRA
