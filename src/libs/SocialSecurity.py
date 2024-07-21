from datetime import date

from libs.Person import Person

# FRA <= means Full Retirement Age


class SocialSecurity:
    def __init__(
        self, FRAAmount: int, person: Person, start_date: date = None, COLA: float = 0.0
    ):
        assert isinstance(FRAAmount, int)
        self.FRAAmount = FRAAmount

        assert isinstance(person, Person)
        self.person: Person = person

        self.start_date: date = start_date

        self.COLA: float = COLA

        # birthdate after 1960  FRA=67
        self._table: dict[int, float] = {
            62: 0.7,
            63: 0.75,
            64: 0.80,
            65: 0.866667,
            66: 0.933333,
            67: 1.0,
            68: 1.08,
            69: 1.16,
            70: 1.24,
        }

    def calc_benefit_amount_by_age(self, age: int):
        assert isinstance(age, int)

        if self.calc_full_retirement_age() == 67:
            if age in self._table:
                _ratio = self._table[age]
                return round(self.FRAAmount * _ratio)
            if age < 62:
                return 0
            if age > 70:
                return round(self.FRAAmount * self._table[70])

    def calc_full_retirement_age(self):
        if self.person.birthDate >= date(1960, 1, 1):
            return 67
        return 66

    def calc_end_date(self, person: Person):
        self.end_date = date(
            person.birthdate.year + person.lifeExpectancy,
            person.birthDate.month,
            person.birthDate.day,
        )
