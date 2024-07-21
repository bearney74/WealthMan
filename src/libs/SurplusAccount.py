class SurplusAccount:
    def __init__(self, balance, interest_rate):
        self.balance = balance
        if interest_rate >= 1:
            interest_rate /= 100.0

        self.interest_rate = 1.0 + interest_rate

    def add_interest(self):
        if self.balance > 0:
            self.balance = int(self.balance * self.interest_rate)

    def withdraw(self, amount):  # returns withdraw, deficit
        if self.balance >= amount:
            self.balance -= amount
            return amount, 0

        # amount is greater than our balance (we have a deficit)
        _withdraw = self.balance
        self.balance = 0
        return _withdraw, _withdraw - amount

    def deposit(self, amount):
        self.balance += amount
