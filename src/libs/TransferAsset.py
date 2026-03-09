from .Person import Person
from .Account import Account


class TransferAssets:
    def __init__(
        self,
        descr,
        sourceAccount,
        targetAccount,
        amount,
        COLA,
        person,
        beginAge,
        endAge,
    ):
        self._descr = descr

        assert isinstance(sourceAccount, Account)
        self.sourceAccount = sourceAccount

        assert isinstance(targetAccount, Account)
        self.targetAccount = targetAccount

        self.amount = amount

        assert isinstance(COLA, float)
        if abs(COLA) >= 1:
            self.COLA = 1.0 + COLA / 100.0
        else:
            self.COLA = 1.0 + COLA

        assert isinstance(person, Person)
        self.person = person

        if beginAge is None:
            beginAge = 0
        assert isinstance(beginAge, int)
        self.beginAge = beginAge

        if endAge is None:
            endAge = 99
        assert isinstance(endAge, int)
        self.endAge = endAge

        assert self.beginAge <= self.endAge

    def do_transfer(self, year=None):
        self.transferred_amount = 0

        _age = self.person.calc_age_by_year(year)
        if _age < self.beginAge or _age > self.endAge:
            return

        # if we got here we should do the transfer
        # take amount from source and put it in target

        # if source contains the amount, let use that amount, if not use the lesser amount in the source acct.
        if self.sourceAccount.Balance >= self.amount:
            self.transferred_amount = self.amount
        else:
            self.transferred_amount = self.sourceAccount.Balance

        self.targetAccount.deposit(self.transferred_amount)
        self.sourceAccount.withdraw(self.transferred_amount)

        # adjust amount by cola for next time (ie, next year)
        self.amount = int(self.amount * self.COLA)

    @property
    def taxable_income(self):
        return self.sourceAccount.taxable_income

    @property
    def ltcg_income(self):
        return self.sourceAccount.ltcg_income
