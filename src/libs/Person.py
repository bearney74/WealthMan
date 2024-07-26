from datetime import date


class Person:
    def __init__(
        self,
        name: str,
        birthDate: date,
        retirementAge: int = None,
        lifeSpanAge: int = None,
        relationship=None,
    ):
        assert isinstance(name, str)
        self.name = name

        assert isinstance(birthDate, date)
        self.birthDate = birthDate  # date of birth

        assert retirementAge is None or isinstance(retirementAge, int)
        self.retirementAge = retirementAge

        assert lifeSpanAge is None or isinstance(lifeSpanAge, int)
        self.lifeSpanAge = lifeSpanAge  # date of death (Dec 31st of year)
        # todo..
        self.relationship = relationship

    def calc_date_by_age(self, age: int) -> date:
        return date(self.birthDate.year + age, self.birthDate.month, self.birthDate.day)

    def calc_age_by_date(self, dt: date) -> int:
        """returns the number of years between two dates"""
        assert isinstance(self.birthDate, date)
        return (
            dt.year
            - self.birthDate.year
            - ((dt.month, dt.day) < (self.birthDate.month, self.birthDate.day))
        )

    def calc_age_by_year(self, year: int) -> int:
        """returns the age of person on Dec 31st of year"""
        return self.calc_age_by_date(dt=date(year, 12, 31))
